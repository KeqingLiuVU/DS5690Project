# Overview

**Challenge:** Applying for more than 50 jobs to secure interviews is time-consuming, requiring at least one minute per application. This represents a significant time investment with limited personal development benefits. 

**Goal:** The goal of this project is to create an application that automates the process of applying for easy-apply jobs on LinkedIn using my personal information, saving valuable time.

**Approach**: The project integrates two key components:

1. A workflow to interact with the LinkedIn website and automate the job application process.
   
2. An AI-powered system to generate and fill answers for application questions during the process.

# Presentation materials

The project features a Streamlit App for demonstration.

<img width="885" alt="Screenshot 2024-11-27 at 7 40 05 PM" src="https://github.com/user-attachments/assets/76f6b837-b858-4945-b06b-fbe71e10cff7">

# Model card/dataset card

**Model Name:** Claude-3.5-Sonnet

**Uses:** The model is employed to automate job applications on LinkedIn's easy-apply feature. It generates and fills answers to application questions using predefined personal information, streamlining the process and reducing time investment for job seekers.

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

**Limitations:**

The model's responses are based on the input provided, and it may occasionally generate inaccurate or irrelevant answers, which could impact the application quality.


# Resource links

**Referenced Code:**

https://github.com/nicolomantini/LinkedIn-Easy-Apply-Bot

https://github.com/madingess/EasyApplyBot

**AI Model:**

https://www.anthropic.com/claude/sonnet


