from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from ai_helper import query_claude,match_options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from difflib import get_close_matches
# Automatically install and set up the correct ChromeDriver version
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
########


class EasyApplyLinkedin:

    
    def __init__(self, data):
        """Parameter initialization"""

        self.email = predefined_answers['email']
        self.password = credentials['password']
        self.keywords = search_params['keywords']
        self.location = search_params['location']
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def login_linkedin(self):
        """This function logs into your personal LinkedIn profile"""

        # go to the LinkedIn login url
        self.driver.get("https://www.linkedin.com/login")

        # introduce email and password and hit enter
        login_email = self.driver.find_element(By.NAME, 'session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element(By.NAME, 'session_password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)
    
    def job_search(self):
        """This function goes to the 'Jobs' section a looks for all the jobs that matches the keywords and location"""

        # go to Jobs
         # Alternative selector for the Jobs tab using its URL
        jobs_link = WebDriverWait(self.driver, 40).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Jobs'))
    )
        # Use JavaScript to click on the "Jobs" link
        self.driver.execute_script("arguments[0].click();", jobs_link)

    # Add a short delay to allow the page to transition to the Jobs section
        time.sleep(1)

        # search based on keywords and location and hit enter
        search_keywords = WebDriverWait(self.driver, 40).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']"))
        )
        search_keywords.click()
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_location = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']"))
        )
        search_location.click()
        search_location.clear()
        search_location.send_keys(self.location)
        
        search_location.click()
        time.sleep(1)  # Brief pause
    
        search_location.send_keys(Keys.RETURN)

        
    def filter(self):
        """This function filters all the job results by 'Easy Apply'"""

        # select all filters, click on Easy Apply and apply the filter
    
        all_filters_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Show all filters. Clicking this button displays all available filter options.']"))
        )
        
        self.driver.execute_script("arguments[0].setAttribute('aria-expanded', 'true')", all_filters_button)
        all_filters_button.click()
        time.sleep(1)  # Allow some time for scrolling

        easy_apply_switch = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox' and @role='switch' and contains(@id, 'adToggle')]"))
        )
            # Click the "Easy Apply" switch if it’s not already enabled
        if easy_apply_switch.get_attribute("aria-checked") == "false":
            self.driver.execute_script("arguments[0].click();", easy_apply_switch)
            print("Enabled 'Easy Apply' filter.")

        time.sleep(5)  # Allow some time for scrolling

         # Enable "Entry level" filter
        entry_level_checkbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='experience-level-filter-value' and @id='advanced-filter-experience-2']"))
        )
        if not entry_level_checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", entry_level_checkbox)
        print("Enabled 'Entry level' filter.")

        time.sleep(5)  # Allow some time for scrolling
        
            # Click on the "Show results" button
        show_results_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'search-reusables__secondary-filters-show-results-button') and @data-test-reusables-filters-modal-show-results-button='true']"))
        )
        show_results_button.click()

    def find_offers(self):
        """This function finds all the offers through all the pages result of the search and filter"""

        # find the total amount of results (if the results are above 24-more than one page-, we will scroll trhough all available pages)
        total_results_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "display-flex.t-12.t-black--light.t-normal"))
        )
        total_results_int = int(total_results_element.text.split(' ', 1)[0].replace(",", ""))
        print(f"Total number of results: {total_results_int}")

        time.sleep(2)

        # get results for the first page
        results = self.driver.find_elements(By.CSS_SELECTOR, ".job-card-container")  
        print(f"URL after filter applied: {self.driver.current_url}")
        print(f"Page Source: {self.driver.page_source[:500]}")

        if not results:
            print("No job results found on the first page.")
        else:
            print(f"Found {len(results)} job listings on the first page.")
            
        # for each job add, submits application if no questions asked
        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            #title_element = result.find_element(By.CSS_SELECTOR, ".job-card-list__title")
            title_element = result.find_element(By.CSS_SELECTOR, "span[aria-hidden='true'] strong")
            print(f"Attempting to apply to job: {title_element.text}")  # Debug statement
            self.submit_apply(title_element)

        # if there is more than one page, find the pages and apply to the results of each page
        if total_results_int > 24:
            time.sleep(2)

            # find the last page and construct url of each page based on the total amount of pages
            find_pages = self.driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator.artdeco-pagination__indicator--number")
            if find_pages:  # NEW CODE
                print(f"Total pages to navigate: {len(find_pages)}")

            else:
                print("Only one page of results, no pagination required.")  # Debug statement
                self.close_session()
    
    

    def fill_question(self, question_text, question_type, field_element):
        # Try getting the answer from predefined answers first
        answer = predefined_answers.get(question_text.lower())
        dropdown_options = None

        if not answer and question_type == 'dropdown':
            dropdown_options = [option.text.strip() for option in field_element.find_elements(By.TAG_NAME, "option") if option.text.strip()]
            answer = query_claude(question_text, dropdown_options=dropdown_options)
        elif not answer:
            answer = query_claude(question_text)
        
        if question_type == 'text':
            try:
                field_element.click()
                field_element.clear()
                field_element.send_keys(answer)
                print(f"Entered text '{answer}' for question: {question_text}")
            except Exception as e:
                print(f"Failed to enter text for '{question_text}': {e}")

        elif question_type == 'dropdown':
            #try:
                #if dropdown_options is None:  # Ensure dropdown options are populated
             #       dropdown_options = [option.text.strip() for option in field_element.find_elements(By.TAG_NAME, "option") if option.text.strip()]
             #   print(f"Dropdown options for '{question_text}': {dropdown_options}")


             #   if answer not in dropdown_options:
              #      print(f"Answer '{answer}' not in dropdown options for '{question_text}'. Defaulting to the first option.")
             #       answer = dropdown_options[0]  # Fallback to the first option if necessary

              #  select = Select(field_element)
              #  select.select_by_visible_text(answer)
              #  print(f"Selected '{answer}' for dropdown question: {question_text}")
          #  except Exception as e:
            #    print(f"Failed to select dropdown option for '{question_text}': {e}")

            try:
                select = Select(field_element)
                dropdown_options = [option.text.strip() for option in select.options if option.text.strip()]
                match = match_options(answer, dropdown_options)  # Match the generated answer to the closest option
                select.select_by_visible_text(match)
                print(f"Selected dropdown option: '{match}' for question: {question_text}")
            except Exception as e:
                print(f"Failed to select dropdown for '{question_text}': {e}")
        elif question_type == 'radio':
            try:
                options = field_element.find_elements(By.XPATH, ".//label[@data-test-text-selectable-option__label]")
                matched = False
                for option in options:
                    option_text = option.text.strip()
                    if option_text.lower() == answer.lower():
                        option.click()
                        matched = False
                        print(f"Selected radio option: '{option_text}' for question: {question_text}")
                        break
                if not matched:
                    print(f"No matching radio option found for '{question_text}' with answer '{answer}'.")
            except Exception as e:
                print(f"Failed to select radio option for '{question_text}': {e}")
    
    def answer_application_questions(self):
        """Go through each question and fill in the response."""
        #questions = self.driver.find_elements(By.XPATH, "//label")
        questions = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'fb-dash-form-element__label-title')] | //label")
        for question in questions:
            question_text = question.text.strip()
            if not question_text:
                print("Skipped an empty or unsupported question element.")
                continue
            print(f"Processing question: {question_text}")  # Debug print
            # Scroll into view for each question
            self.driver.execute_script("arguments[0].scrollIntoView(true);", question)
            field_element, question_type = None, None
            # Determine question type (text, dropdown, radio) based on associated input
            try:
            # For multiple-choice questions (e.g., Yes/No)
                parent_div = question.find_element(By.XPATH, "ancestor::div[contains(@class, 'fb-dash-form-element')]")
                field_element = parent_div.find_element(By.XPATH, ".//input[@type='radio']")
                question_type = "radio"
                print(f"Identified multiple-choice question for '{question_text}'")
            except Exception:
                try:
                # For dropdowns
                    field_element = question.find_element(By.XPATH, "following-sibling::select[1]")
                    question_type = "dropdown"
                    print(f"Identified dropdown for '{question_text}'")
                except Exception as e_radio:
                    print(f"Failed to identify radio button for '{question_text}': {e_radio}")
                    try:
                    # For text inputs
                        field_element = question.find_element(By.XPATH, "following-sibling::input[1]")
                        question_type = "text"
                        print(f"Identified text input for '{question_text}'")
                    except Exception as e:
                        print(f"Skipped question '{question_text}' - unsupported field or element not found: {e}")
                        continue
            try:
                self.fill_question(question_text, question_type, field_element)
            except Exception as e_fill:
                print(f"Could not fill question '{question_text}': {e_fill}")


    def submit_apply(self,job_add):
        """This function submits the application for the job add found"""

        print('You are applying to the position of: ', job_add.text)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", job_add)
        job_add.click()
        time.sleep(2)

        possible_labels = ['Easy Apply', 'Continue applying']
        try: 
            in_apply = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'jobs-apply-button') and " +
                               " or ".join([f"contains(@aria-label, '{label}')" for label in possible_labels]) +
                               "]"))
            )
            self.driver.execute_script("arguments[0].click();", in_apply)
            print("Clicked Easy Apply or Continue button.")  # Debug line to verify the button label
            #in_apply.click()
            self.driver.execute_script("arguments[0].click();", in_apply)  # Using JavaScript click to avoid interception
            print("Clicked Easy Apply or Continue button.")
            time.sleep(2)
            
        except TimeoutException:
            print('Easy Apply or Continue button not found or already applied. Moving to next job....')
            return
        time.sleep(1)

        # try to submit if submit application is available...
        while True:
            # Answer application questions if there are any
            self.answer_application_questions()
            try:
            # Check for "Next" or "Review" buttons to proceed
                next_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Next') or contains(@aria-label, 'Review')or contains(@aria-label, 'Continue')]"))
                )
                #next_button.click()
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                time.sleep(1)  # Ensure the page stabilizes
                self.driver.execute_script("arguments[0].click();", next_button)  # Use JS click to avoid interception
                print("Clicked 'Next' or 'Review' button using JavaScript.")
        
                time.sleep(2)
            except TimeoutException:
                print("Reached final application step or no further steps required.")
                break

        # Unselect 'Follow company' checkbox if selected
       # try:
            # Locate the follow company checkbox by its ID or label
            #follow_checkbox = self.driver.find_element(By.ID, "follow-company-checkbox")
           # follow_checkbox = self.driver.find_element(By.ID, "follow-company-checkbox")
            # Unselect the checkbox if it's selected
          #  if follow_checkbox.is_selected():
             #   follow_checkbox.click()
          #  #    print("Unselected 'Follow company' checkbox.")
           # else:
         #       print("'Follow company' checkbox is already unselected.")
       # except NoSuchElementException:
           # print("'Follow company' checkbox not found.")

        try:
            submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Submit application']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(0.5)  # Allow time for any animations

            self.driver.execute_script("arguments[0].click();", submit_button)  # JavaScript click for final submit
            print("Application submitted successfully.")
        except TimeoutException:
            print("Final submit button not found. Discarding application.")
        except Exception as e:
            print(f"Error clicking submit button: {e}")
        time.sleep(2)  # Brief pause after submission
        # Handle the post-submission pop-up by clicking "Not now"
        try:
            dismiss_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Dismiss']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", dismiss_button)
            dismiss_button.click()
            print("Dismissed the application pop-up.")
        except TimeoutException:
            print("Dismiss button not found. Continuing...")
        except Exception as e:
            print(f"Error clicking Dismiss button: {e}")
        time.sleep(1) 


            


    def close_session(self):
        """This function closes the actual session"""
        
        print('End of the session, see you later!')
        self.driver.quit()

    def apply(self):
        """Apply to job offers"""

        self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(5)
        self.job_search()
        time.sleep(5)
        self.filter()
        time.sleep(2)
        self.find_offers()
        time.sleep(2)
        self.close_session()


if __name__ == '__main__':

    with open('config.json') as config_file:
        data = json.load(config_file)
    credentials = data['credentials']
    search_params = data['search']
    predefined_answers = data['answers']

    bot = EasyApplyLinkedin(data)
    bot.apply()