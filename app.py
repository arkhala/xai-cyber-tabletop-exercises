import streamlit as st
import os
from datetime import datetime
import json

# Placeholder for xAI integration
# from openai import OpenAI

st.set_page_config(page_title="xAI Cyber TTX Simulator", layout="wide")
st.title("🛡️ xAI Cybersecurity Tabletop Exercise Simulator")
st.markdown("**Choose Your Own Adventure** for Incident Response Training")

# Session state initialization
if 'session_log' not in st.session_state:
    st.session_state.session_log = []
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None
if 'choices' not in st.session_state:
    st.session_state.choices = []

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    theme = st.selectbox("Select Theme", ["Ransomware Attack", "Data Breach", "Supply Chain Compromise", "DDoS", "Insider Threat"])
    industry = st.selectbox("Industry", ["Finance", "Healthcare", "Manufacturing", "Tech", "Government"])
    vulnerabilities = st.multiselect("Specific Vulnerabilities", ["CVE-2023-XXXX", "Phishing", "Zero-Day", "Misconfiguration"])
    participants = st.number_input("Number of Participants", min_value=1, value=5)
    
    if st.button("Start New Exercise"):
        st.session_state.current_scenario = theme
        st.session_state.session_log.append({
            "timestamp": datetime.now().isoformat(),
            "event": f"Exercise started: {theme} in {industry}"
        })
        st.rerun()

# Main area
if st.session_state.current_scenario:
    st.subheader(f"Current Scenario: {st.session_state.current_scenario}")
    
    # Example situation
    st.write("**Situation:** A critical system alert indicates potential ransomware encryption in progress.")
    
    action = st.radio("What is your next action?", [
        "Isolate affected systems",
        "Notify CSIRT and initiate stand-up",
        "Investigate logs first",
        "Communicate with executives",
        "Other (specify)"
    ])
    
    comments = st.text_area("Notes/Comments")
    
    if st.button("Submit Action"):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "comments": comments,
            "scenario": st.session_state.current_scenario
        }
        st.session_state.session_log.append(log_entry)
        st.session_state.choices.append(action)
        st.success("Action logged!")
        st.rerun()

    # Display log
    st.subheader("Session Log")
    for entry in st.session_state.session_log:
        st.write(entry)

    if st.button("End Exercise & Generate Artifacts"):
        st.write("Generating reports...")
        # TODO: Implement artifact generation
        st.json(st.session_state.session_log)
        st.download_button("Download Log", json.dumps(st.session_state.session_log, indent=2), "session_log.json")
else:
    st.info("Configure settings in the sidebar and start the exercise.")

# TODO: Integrate xAI API for dynamic responses
# def get_ai_response(prompt):
#     client = OpenAI(api_key=os.getenv('XAI_API_KEY'), base_url="https://api.x.ai/v1")
#     ...
