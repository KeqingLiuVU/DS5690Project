# **Linkedin Jobs Easy Application**
# Overview

**Challenge:** Applying for over 50 jobs to secure an interview is a highly time-consuming process, with each application requiring at least one minute. This results in a significant time investment with minimal personal growth opportunities.

**Goal:** This project aims to automate the process of applying for LinkedIn's easy-apply jobs using my personal information, saving valuable time and improving efficiency.

**Approach**: The project integrates two key components:

1. **Automation Workflow:** Interacts with LinkedIn's website to apply for jobs automatically.
   
2. **AI-Powered Answer Generation:** Utilizes an AI model to generate and fill answers for application questions during the process.

# Presentation materials

The project features a Streamlit App for demonstration.

<img width="885" alt="Screenshot 2024-11-27 at 7 40 05 PM" src="https://github.com/user-attachments/assets/76f6b837-b858-4945-b06b-fbe71e10cff7">

# Model card/dataset card

**Model Name:**

Claude-3.5-Sonnet

**Uses:** 

The model is employed to automate job applications on LinkedIn's easy-apply feature. It generates and fills answers to application questions using predefined personal information, streamlining the process and reducing time investment for job seekers.

**Sources:** 

- **Model Source:** The Claude-3.5-Sonnet model is accessed via its API provided by Anthropic.

- **Dataset:** The input dataset consists of sensitive personal information, including:

  - LinkedIn credentials (username and password)
  - Personal details (name, email address, phone number, school, address, skills, work experience, etc.)
  - Predefined answers to frequently asked job application questions. 
  
  Due to the private nature of this information, the dataset is not uploaded to GitHub and is securely stored locally during project execution.

**Permissions:**

- **Model Permissions:** The model usage complies with Anthropic's terms and conditions.
  
- **Dataset Permissions:** The dataset includes sensitive personal information such as LinkedIn credentials (username and password), personal details (name, email, phone number, etc.), and predefined answers to frequently asked application questions. This information is privately owned and securely stored locally, ensuring no unauthorized access or sharing.

**Training Parameters and Experimental Info:**

This project does not involve training the Claude-3.5-Sonnet model directly. Instead, the model is accessed through its API for inference. The automation workflow integrates this model to enhance job application efficiency.

# Critical Analysis

**Impact:** The project addresses a major pain point for me by automating repetitive application tasks, saving significant time, and enabling focus on more personalized application strategies.

**Limitations:** The model's responses depend on the input provided and may occasionally generate inaccurate or irrelevant answers, potentially affecting application quality. This reliance on AI for generating responses can sometimes lead to inconsistencies or errors.

**Next Steps:** Future improvements could involve integrating additional error-checking mechanisms and expanding automation capabilities to cover non-easy-apply job applications.


# User Interface

I have demonstrated how to use the user interface in the video recording. However, due to the sensitive nature of this project, deploying the UI on Streamlit would require uploading sensitive information to a public platform. Therefore, I am unable to share a public Streamlit link.

You can still access the UI locally on your computer by running the following command in your terminal: streamlit run app.py


# Resource links

**Referenced Code:**

https://github.com/nicolomantini/LinkedIn-Easy-Apply-Bot

https://github.com/madingess/EasyApplyBot

**AI Model:**

https://www.anthropic.com/claude/sonnet


