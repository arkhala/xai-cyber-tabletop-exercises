import streamlit as st
import os
from datetime import datetime
import json
from openai import OpenAI

st.set_page_config(page_title="xAI Cyber TTX Simulator", layout="wide")
st.title("🛡️ xAI Cybersecurity Tabletop Exercise Simulator")
st.markdown("**Dynamic Choose-Your-Own-Adventure** powered by xAI Grok · Real-time scenario generation")

# Session state
for key in ['session_log', 'game_history', 'current_situation', 'scenario_description', 'exercise_started', 'xai_key']:
    if key not in st.session_state:
        st.session_state[key] = [] if key == 'session_log' or key == 'game_history' else None if key != 'exercise_started' else False

# xAI client
def get_client():
    api_key = os.getenv("XAI_API_KEY") or st.session_state.get("xai_key")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

def call_xai(prompt: str, temperature: float = 0.7) -> str:
    client = get_client()
    if not client:
        st.warning("xAI API key not configured. Add it in sidebar or as XAI_API_KEY env var.")
        return "[API not available]"
    try:
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[
                {"role": "system", "content": "You are a highly skilled cybersecurity incident response tabletop exercise Game Master. Generate realistic, time-pressured injects, evaluate decisions fairly, and advance the scenario dynamically."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"xAI API error: {str(e)}")
        return f"Error: {str(e)}"

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    if not os.getenv("XAI_API_KEY"):
        st.session_state.xai_key = st.text_input("xAI API Key", type="password")
    
    industry = st.selectbox("Industry", ["Finance", "Healthcare", "Manufacturing", "Tech", "Government", "Critical Infrastructure"])
    theme = st.selectbox("Primary Threat Theme", ["Ransomware Attack", "Supply Chain Compromise", "Data Breach", "Insider Threat", "Cloud Security Incident", "APT / Nation-State", "Zero-Day + Social Engineering"])
    
    st.checkbox("Base on recent vulnerabilities & news", value=True, key="use_recent")
    
    extra_vulns = st.text_input("Additional TTPs / CVEs (optional)", placeholder="Log4Shell, MOVEit, phishing kit, etc.")
    
    st.divider()
    
    if st.button("🎲 Generate New Scenario with xAI", type="primary", use_container_width=True):
        with st.spinner("Consulting Grok for a fresh, realistic scenario..."):
            prompt = f"""Create a detailed, realistic cybersecurity tabletop exercise scenario.
- Industry: {industry}
- Theme: {theme}
- Additional details: {extra_vulns}
- Make it current and believable. Include initial situation, key stakeholders, and first major inject."""
            generated = call_xai(prompt)
            st.session_state.scenario_description = generated
            st.session_state.current_situation = generated
            st.success("✅ Scenario ready!")
            st.rerun()

# Main UI
st.subheader("Scenario Setup")

if not st.session_state.scenario_description:
    st.info("Generate a scenario using the sidebar or enter a custom one below.")
    manual = st.text_area("Or describe your own scenario seed (AI will expand it)", height=120)
    if st.button("Flesh Out with xAI") and manual.strip():
        with st.spinner("Expanding your idea into a full scenario..."):
            prompt = f"Turn this into a rich, detailed tabletop exercise starting scenario:\n{manual}\nContext - Industry: {industry}, Theme: {theme}"
            expanded = call_xai(prompt)
            st.session_state.scenario_description = expanded
            st.session_state.current_situation = expanded
            st.rerun()
else:
    with st.expander("Full Scenario Background", expanded=False):
        st.markdown(st.session_state.scenario_description)

    if st.button("🚀 Start / Continue Exercise", type="primary"):
        st.session_state.exercise_started = True
        if not st.session_state.session_log:
            st.session_state.session_log.append({
                "timestamp": datetime.now().isoformat(),
                "type": "system",
                "content": "Exercise started"
            })

if st.session_state.exercise_started and st.session_state.current_situation:
    st.divider()
    st.subheader("📢 Current Situation")
    st.info(st.session_state.current_situation)
    
    st.subheader("Your Team's Decision")
    
    action_mode = st.radio("Input mode", ["Quick options", "Detailed free response"], horizontal=True)
    
    if action_mode == "Quick options":
        action = st.selectbox("Select primary action", [
            "Call CSIRT stand-up meeting",
            "Isolate / contain the incident",
            "Collect evidence & start forensics",
            "Notify CISO / senior leadership",
            "Determine if this is a reportable incident",
            "Engage external partners (MSP, law enforcement, PR)",
            "Custom action"
        ])
    else:
        action = st.text_area("Describe your decision and rationale", height=110)
    
    notes = st.text_area("Team discussion notes / questions", height=80)
    
    if st.button("Submit Action → Get Next Inject", type="primary", use_container_width=True):
        # Log player action
        st.session_state.session_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "decision",
            "action": action,
            "notes": notes
        })
        
        # Build context for AI
        recent_log = "\n".join([f"{e.get('timestamp','')} | {e.get('action') or e.get('content','')}" for e in st.session_state.session_log[-6:]])
        
        next_prompt = f"""Exercise context: {st.session_state.scenario_description[:400]}...

Recent timeline:
{recent_log}

Team decision: {action}
Notes: {notes}

Respond as Game Master:
- Describe immediate consequences (good and bad)
- Introduce the next realistic inject or complication
- Keep pressure on the team"""
        
        with st.spinner("Generating next scenario inject..."):
            next_inject = call_xai(next_prompt)
            st.session_state.current_situation = next_inject
            # Log AI inject
            st.session_state.session_log.append({
                "timestamp": datetime.now().isoformat(),
                "type": "inject",
                "content": next_inject[:500] + "..." if len(next_inject) > 500 else next_inject
            })
        st.rerun()

    # Show recent log
    st.subheader("📜 Live Exercise Log")
    for entry in reversed(st.session_state.session_log[-8:]):
        ts = entry.get('timestamp', '')[:19]
        if entry.get('type') == 'decision':
            st.success(f"**{ts} Decision:** {entry.get('action')}")
        elif entry.get('type') == 'inject':
            st.info(f"**{ts} Inject:** {entry.get('content')}")
        else:
            st.write(f"**{ts}** {entry.get('content','')}")

# End exercise & artifacts
if st.session_state.exercise_started and st.button("🏁 End Exercise and Generate Reports"):
    st.session_state.exercise_started = False
    st.rerun()

if not st.session_state.exercise_started and len(st.session_state.session_log) > 2:
    st.divider()
    st.subheader("📋 Generate Professional Artifacts")
    if st.button("Create After-Action Package", type="primary"):
        with st.spinner("AI analyzing full exercise and drafting reports..."):
            full_log = json.dumps(st.session_state.session_log, indent=2, ensure_ascii=False)
            report_prompt = f"""You are a senior incident response consultant. Review this complete tabletop exercise log and produce:
1. Executive Summary
2. Detailed After Action Report (AAR)
3. Incident Memo to CISO (key facts, impact, recommendations)
4. Timeline of decisions
5. Strengths observed & areas for improvement
6. Lessons learned

Full log:
{full_log}"""
            
            reports = call_xai(report_prompt, temperature=0.65)
            st.markdown(reports)
            
            st.download_button("Download Session Log JSON", data=json.dumps(st.session_state.session_log, indent=2), file_name="ttx_full_log.json", mime="application/json")
            st.download_button("Download Artifacts Markdown", data=reports, file_name="ttx_after_action_reports.md", mime="text/markdown")

st.caption("✅ Scenarios & injects generated live by xAI Grok · Perfect for CSIRT training")
