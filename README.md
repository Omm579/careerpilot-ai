# 🚀 CareerPilot AI

**CareerPilot AI** is a cutting-edge, Multi-Agent AI Career Intelligence System powered by Gemini 2.5 Flash, Streamlit, and Python. It transforms the job hunt by converting raw resumes into highly strategic, personalized career roadmaps through a coordinated network of specialized AI agents.
 
---

## ✨ Key Features

### 📄 Resume Analysis Agent
* **ATS Optimization**: Calculates precise applicant tracking system scores.
* **Core Strengths**: Pinpoints standout professional achievements automatically.
* **Flaw Detection**: Flags gaps, formatting issues, or weak phrasing.
* **Actionable Fixes**: Provides concrete rewrite suggestions instantly.

### 🧠 Skill Gap Agent
* **Role Alignment**: Matches current user profiles against target jobs.
* **Deficit Mapping**: Highlights missing technical and soft skills.
* **Curated Learning**: Recommends exact technologies to master next.
* **Dynamic Roadmaps**: Generates step-by-step learning schedules.

### 🎯 Interview Preparation Agent
* **Technical Drills**: Customizes coding, system design, or domain questions.
* **Behavioral Prep**: Generates tailored HR and situational interview prompts.
* **Core Concepts**: Identifies high-yield topics to study first.

### 🤖 Coordinator Agent
* **Smart Orchestration**: Directs specialized agents like a digital conductor.
* **Unified Synthesis**: Blends separate insights into one seamless report.
* **Strategic Blueprint**: Outputs final high-level career growth recommendations.

### 🧰 Power Features
* **PDF Ingestion**: Fast, automatic text extraction via `PyPDF`.
* **Exportable Intelligence**: Downloadable PDFs for offline preparation.
* **Session Memory**: Remembers past analyses during active sessions.

---

## 🏗️ Architecture

```text
       ┌────────────────────────┐
       │ User Resume & Target   │
       └───────────┬────────────┘
                   ▼
       ┌────────────────────────┐
       │   Coordinator Agent    │
       └───────────┬────────────┘
                   ▼
   ┌───────────────┼───────────────┐
   ▼               ▼               ▼
┌──────────────┐┌──────────────┐┌──────────────┐
│ Resume Agent ││  Skill Gap   ││  Interview   │
│              ││    Agent     ││    Agent     │
└──────────────┘└──────────────┘└──────────────┘
   │               │               │
   └───────────────┼───────────────┘
                   ▼
       ┌────────────────────────┐
       │ Final Career Strategy  │
       └────────────────────────┘
```

---

## 🛠️ Tech Stack

* **Frontend UI**: Streamlit
* **Core Backend**: Python
* **AI Core**: Gemini 2.5 Flash
* **Libraries**: `google-genai`, `streamlit`, `python-dotenv`, `pypdf`

---

## 📁 Project Structure

```text
CareerPilot-AI/
├── agents/
│   ├── resume_agent.py
│   ├── skill_gap_agent.py
│   ├── interview_agent.py
│   └── coordinator_agent.py
├── utils/
│   ├── prompts.py
│   ├── pdf_handler.py
│   └── gemini_helper.py
├── data/
│   ├── sample_resume.txt
│   └── demo_resumes/
│       ├── ai_resume.txt
│       ├── data_analyst_resume.txt
│       └── frontend_resume.txt
├── app.py
├── requirements.txt
├── README.md
└── .env
```

---

## ⚙️ Quick Start

### 1. Clone & Navigate
```bash
git clone https://github.com/Omm579/careerpilot-ai
cd careerpilot-ai
```

### 2. Install Packages
```bash
pip install -r requirements.txt
```

### 3. Add API Keys
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_api_key_here
```

### 4. Launch Application
```bash
streamlit run app.py
```

---

## 🧪 Experience the Workflow

1. **Upload**: Drop your resume PDF into the secure portal.
2. **Target**: Type in your dream professional role.
3. **Analyze**: Watch the Multi-Agent ecosystem collaborate.
4. **Review**: Explore deep-dive tabs for Resume, Skills, and Interviews.
5. **Export**: Grab your structured career strategy report instantly.

---

## 🔮 Future Horizons

* Live web search for active job market trends.
* Direct LinkedIn profile scraping and comparison.
* Personalized job recommendation matchmaker engines.
* Real-time AI voice interview simulation booths.
* Persistent databases for long-term user profiles.
* Instant Cloud deployments via Streamlit Cloud.

---

## 🎯 Hackathon Vision

**CareerPilot AI** bridges technical execution and real-world utility. It showcases multi-agent orchestration, complex reasoning pipelines, structured prompt engineering, and elegant human-centric software design.

---

## 📌 Disclaimer
*This project is built for educational and hackathon purposes. AI insights provide directional guidance and should be evaluated alongside professional human judgment.*
