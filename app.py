"""Streamlit app to generate Tweets."""

import streamlit as st
import json
import os 
def start():
    """Generate Tweet text and apply for jobs."""
    config_file = "config.json"

    # Check if all inputs are provided
    if not claude_api_key or not keywords or not location:
        st.error("Please fill in all the required fields.")
        return

    # Update config.json with user inputs
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config_data = json.load(f)
    else:
        st.error("Config file not found!")
        return

    config_data["credentials"]["claude_api_key"] = claude_api_key
    config_data["search"]["keywords"] = keywords
    config_data["search"]["location"] = location

    with open(config_file, "w") as f:
        json.dump(config_data, f, indent=4)

    st.success("Configuration updated successfully!")
    st.info("Running main.py to start applying for jobs...")

    # Run the main.py script
    os.system("python main.py")


st.title('Linkedin Jobs Easy Application')
st.markdown(
    "This mini-app generates texts using Claude and applies for jobs on LinkedIn."
)

claude_api_key = st.text_input(label="Claude API key", placeholder="Claude API key")
keywords = st.text_input(label="Keywords", placeholder="Title, skill, or company")
location = st.text_input(label="Location", placeholder="City, state, or zip code")

if st.button(label="Generate Text and Apply"):
    start()