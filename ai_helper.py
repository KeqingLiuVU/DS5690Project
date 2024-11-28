import json
import anthropic
import os
from difflib import get_close_matches

# Load config data from config.json
with open('config.json') as f:
    config_data = json.load(f)


# Extract predefined answers and Claude API key
predefined_answers = config_data["answers"]
CLAUDE_API_KEY = config_data["credentials"]["claude_api_key"]

def match_options(answer, options):
    """
    Matches the generated answer with the most similar option from the provided options.

    Parameters:
    - answer (str): The generated answer from Claude.
    - options (list): List of dropdown options to match against.

    Returns:
    - str: The exact matched option from the dropdown options.
    """
    if not options:
        print("No options provided for matching.")
        return None

    # Use difflib to find the closest match
    matches = get_close_matches(answer, options, n=1, cutoff=0.5)  # cutoff defines the similarity threshold
    if matches:
        print(f"Matched '{answer}' with dropdown option: '{matches[0]}'")
        return matches[0]
    else:
        print(f"No close match found for '{answer}'. Returning the first available option: '{options[0]}'")
        return options[0]  
    
# Initialize the Anthropic client
client = anthropic.Client(api_key=CLAUDE_API_KEY)

def query_claude(question_text,dropdown_options=None):
    if dropdown_options:
        # For dropdown questions, ask Claude to choose the best option
        dropdown_options_str = "\n".join(f"- {option}" for option in dropdown_options)
        prompt = f"""
        You are completing a job application. Select the best option from the following list for this question:
        Question: "{question_text}"
        Options:
        {dropdown_options_str}
        Respond with only the exact wording from the options provided, without any additional explanation. Reference predefined answers when appropriate:
        {json.dumps(predefined_answers, indent=2)}

        """
    else: 

        prompt = f"""
        You are completing a job application. Answer the following question as a real applicant would:
        Question: "{question_text}"
        If the question is about "years of experience," respond with a whole number. Use predefined answers for guidance when possible:
        {json.dumps(predefined_answers, indent=2)}
        Keep your response concise and relevant (under 50 tokens).
        """

    # Send the request to Claude
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",  # Use the actual Claude model available to you
        max_tokens=100,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )


    # Extract the generated text response from Claude
    raw_answer = response.content[0].text.strip()
    print(f"Raw answer from Claude: {raw_answer}")  # Debug log

    # Validate and sanitize the response for whole number questions
    if "years of" in question_text.lower():
        try:
            # Extract the first valid whole number from the response
            sanitized_answer = int(float(raw_answer))  # Ensure conversion to whole number
            print(f"Sanitized whole number answer: {sanitized_answer}")
            return str(sanitized_answer)  # Return as a string to be compatible with form inputs
        except ValueError:
            # Fallback to a default if parsing fails
            print(f"Failed to parse whole number from response: {raw_answer}. Defaulting to 2.")
            return "2"

    # Extract the generated text response from Claude
    return raw_answer

