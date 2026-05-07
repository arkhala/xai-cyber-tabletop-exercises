# xAI Cyber Tabletop Exercises (TTX) Simulator

**A interactive GUI "choose your own adventure" style cybersecurity tabletop exercise simulator powered by the xAI API (Grok).**

## Overview

This tool helps security teams conduct realistic, engaging tabletop exercises by simulating incident response scenarios. Participants make choices, the system (with AI assistance) responds dynamically, logs everything, and generates professional artifacts at the end.

## Key Features
- **Graphical User Interface** (Streamlit-based)
- **Scenario Configuration**: Select theme (e.g., ransomware, data breach, supply chain), specific vulnerabilities, industry, team size, etc.
- **Choose-Your-Own-Adventure Gameplay**: Present situations, options for actions/decisions. AI can generate realistic injects or consequences.
- **Logging & Recording**: Automatic log of choices, timestamps, user comments/notes.
- **Key Prompts**: CSIRT stand-up, incident declaration, escalation points.
- **Artifact Generation**:
  - Detailed session log/transcript
  - After Action Report (AAR)
  - Incident Memorandum to CISO
  - Attendance/Participant report
  - Lessons learned summary
  - Optional: Timeline visualization, risk assessment
- **xAI Integration**: Use Grok to power dynamic narrative, evaluate decisions, generate new injects, or facilitate debrief.

## Quick Start

1. Clone: `git clone https://github.com/arkhala/xai-cyber-tabletop-exercises.git`
2. `cd xai-cyber-tabletop-exercises`
3. `pip install -r requirements.txt`
4. Set environment variable: `export XAI_API_KEY=your_key_here` (get from x.ai)
5. `streamlit run app.py`

## Tech Stack
- **Frontend/GUI**: Streamlit
- **AI**: xAI Grok API (via OpenAI-compatible client or official SDK)
- **Data/Logging**: Pandas, JSON, Markdown/PDF generation (ReportLab or WeasyPrint)
- **State Management**: Streamlit session state

## Project Structure

```
.
├── app.py                 # Main application
├── scenarios/             # YAML/JSON scenario templates
├── core/                  # Game engine, logging, AI integration
├── artifacts/             # Templates and generators for reports
├── utils/                 # Helpers
├── requirements.txt
├── .env.example
└── README.md
```

## Contributing
Feel free to add new scenarios, improve AI prompts, enhance artifact generation, or add features like multi-player mode.

## License
MIT
