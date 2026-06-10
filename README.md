# EduMind AI 🎓

**A smart student companion web app for Sri Lankan A/L and university students.**

EduMind AI helps students track their studies, manage tasks, monitor wellness, and get AI-powered support — all in one place.

---

## 🌐 Live Demo

[edumindai.streamlit.app](https://edumindai.streamlit.app)

---

## ✨ Features

### 🏠 Home
- Personalized greeting based on time of day
- Daily mood check-in
- Today's tasks with completion tracking
- Today's recurring classes
- Upcoming exam countdown

### 💊 Wellness Tracker
- Daily health logging — sleep, water, food, phone usage, exercise, stress
- Wellness score out of 100 with SVG progress ring
- Personalized feedback based on logged data
- 7-day wellness history
- High stress detection with AI Chatbot redirect

### 💬 AI Chatbot
- Powered by Groq LLaMA 3.3 70B
- Understands Sri Lankan student context
- Responds in English, Tamil, or Sinhala
- Wellness-aware — knows if student is stressed or sleep-deprived
- Chat history saved per user session
- Starter prompts for common student struggles

### 📅 Day Tracker
- **Exams** — add exams with countdown
- **Tasks** — add, complete, delete tasks with priority levels
- **Recurring** — weekly class schedule
- **End of Day** — daily check-in with study hours, mood, tomorrow's plan

### 🎁 Rewards
- Duolingo-style flame streak system
- SVG progress ring showing streak to next milestone
- Motivational messages based on streak level
- Weekly tracker showing daily check-ins
- 11 badges — First Task, Task Master, Streak badges, Exam Warrior, Night Owl, Early Bird, Subject Master

### 📈 Dashboard
- Weekly summary — total study hours, tasks completed, mood
- Wellness this week — avg sleep, stress, focus
- GitHub-style activity heatmap (12 weeks)
- Study hours bar chart (last 7 days)
- AI-generated study tips based on performance
- Task completion tracker
- Auto risk score based on study habits and mood

---

## 🛠 Tech Stack

| Layer | Tech |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| AI | Groq LLaMA 3.3 70B |
| Database | SQLite |
| Charts | Plotly |
| Deployment | Streamlit Cloud |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Groq API key — get one at [console.groq.com](https://console.groq.com)

### Local Setup

```bash
# Clone the repo
git clone https://github.com/Amshavarthana-S/EduMindAI.git
cd EduMindAI

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
# Create .streamlit/secrets.toml and add:
# GROQ_API_KEY = "your_key_here"

# Run the app
cd app
streamlit run main.py
```

---

## 📁 Project Structure

```
EduMindAI/
├── .streamlit/
│   ├── config.toml       ← Theme config (purple #8B5CF6)
│   └── secrets.toml      ← API keys (not in git)
├── app/
│   ├── main.py           ← Main Streamlit app
│   ├── planner_db.py     ← SQLite DB functions
│   └── chat_db.py        ← Chat history DB functions
├── data/                 ← SQLite databases (not in git)
├── requirements.txt
└── README.md
```

---

## 🔐 Multi-User Support

Each student creates a unique username on first login. All data (tasks, mood, wellness, chat history, streaks) is stored separately per username. No passwords required — designed for classroom/demo use.

---

## 📦 Requirements

```
streamlit
groq
plotly
pandas
```

---

## 🎯 Built For

- Sri Lankan A/L students
- University undergraduates
- Students who need a study buddy that actually understands their context

---

## 👨‍💻 Developer

Built by **amshavarthana-S** 
