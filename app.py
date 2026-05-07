# Main Streamlit app with dynamic scenario generation

import streamlit as st
from xai import client  # assuming xAI client setup

# Scenario generation functions

def generate_scenario(theme, use_recent_news=False, custom_prompt=''):
    # Call xAI API to create rich scenario
    prompt = f'Generate a detailed cybersecurity tabletop exercise scenario around: {theme}'
    if use_recent_news:
        prompt += ' Incorporate recent news and current vulnerabilities.'
    if custom_prompt:
        prompt += f' Custom idea: {custom_prompt}'
    # ... call API and return structured scenario ...
    return scenario

st.title('xAI Cyber TTX')

# Configuration screen with new options
if 'scenario' not in st.session_state:
    st.header('Configure Exercise')
    mode = st.radio('Scenario Mode', ['Auto-Generate', 'Custom'])
    if mode == 'Auto-Generate':
        theme = st.selectbox('Theme', ['Ransomware', 'Supply Chain Attack', 'Insider Threat', 'Cloud Breach', 'AI-Powered Attack', 'Recent Threats'])
        use_recent = st.checkbox('Incorporate recent news and vulnerabilities', value=True)
        if st.button('Generate Scenario'):
            scenario = generate_scenario(theme, use_recent)
            st.session_state.scenario = scenario
    else:
        custom = st.text_area('Describe your scenario idea')
        if st.button('Flesh Out Scenario'):
            scenario = generate_scenario('custom', False, custom)
            st.session_state.scenario = scenario

# Gameplay loop if scenario exists
else:
    # Display narrative, choices, log, etc.
    pass
