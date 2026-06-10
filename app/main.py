import streamlit as st
import os
import sys
import pickle
import pandas as pd
import uuid

try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except:
    os.environ["GROQ_API_KEY"] = "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"

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from chat_db import init_db, save_message, save_session, get_all_sessions, get_session_messages, delete_session
from planner_db import (init_planner_db, add_exam, get_all_exams, delete_exam,
                        add_task, get_tasks, get_today_tasks, complete_task,
                        delete_task, save_mood, get_today_mood, get_mood_last_7_days,
                        save_student_name, get_student_name, add_recurring_task,
                        get_recurring_tasks, delete_recurring_task,
                        save_day_checkin, get_day_checkin, get_checkin_last_7_days,get_xp, add_xp, get_streak, get_badges, award_badge,save_wellness, get_today_wellness, get_wellness_last_7_days, save_profile, get_profile)

init_db()
init_planner_db()

# ── USERNAME SESSION ──────────────────────────────────────
if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.username is None:
    st.set_page_config(page_title="EduMind AI", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")
    st.markdown("""
        <div style='text-align:center; padding:60px 20px;'>
            <h1 style='color:#8B5CF6;'>EduMind AI</h1>
            <p style='color:#888; font-size:1.1rem;'>Your study buddy is always here</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Enter your username to continue")
        st.caption("Use the same username every time to keep your data.")
        username_input = st.text_input("Username", placeholder="e.g. Tom29")
        if st.button("Continue", use_container_width=True):
            if username_input.strip():
                st.session_state.username = username_input.strip()
                st.rerun()
    st.stop()

username = st.session_state.username

st.set_page_config(
    page_title="EduMind AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #8B5CF6;
        padding: 20px;
    }
    .subtitle {
        font-size: 1rem;
        text-align: center;
        color: #888;
        margin-bottom: 30px;
    }
    div[data-baseweb="select"] { cursor: pointer !important; }
    div[data-baseweb="select"] * { cursor: pointer !important; }
    .stSelectbox div { cursor: pointer !important; }
    .stButton button { cursor: pointer !important; }
    .stSlider { cursor: pointer !important; }

    /* Force purple theme everywhere */
    div[data-baseweb="select"] > div {
        border-color: #8B5CF6 !important;
    }
    div[data-baseweb="select"] > div:focus-within {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 1px #8B5CF6 !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 1px #8B5CF6 !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #8B5CF6 !important;
    }
    div[data-baseweb="tab-border"] {
        background-color: #8B5CF6 !important;
    }
    .stProgress > div > div {
        background-color: #8B5CF6 !important;
    }
    div[data-baseweb="input"] {
        border-color: #8B5CF6 !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 1px #8B5CF6 !important;
    }
    
    section[data-testid="stSidebar"] button[kind="primary"] {
    background-color: #8B5CF6 !important;
    border-color: #8B5CF6 !important;
    color: white !important;
}
section[data-testid="stSidebar"] button[kind="primary"]:hover {
    background-color: #7c3aed !important;
    border-color: #7c3aed !important;
}
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <div style='padding: 10px 0 5px 0;'>
        <h2 style='color: var(--color-text-primary); font-weight: 700; margin: 0; font-size: 1.4rem;'>
        Edu<span style='color: #8B5CF6;'>Mind AI</span>
        </h2>
        <p style='color: #888; font-size: 0.85rem; margin: 4px 0 0 0;'>Your study buddy is always here</p>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

pages = [
    ("🏠", "Home"),
    ("💊", "Wellness"),
    ("💬", "AI Chatbot"),
    ("📅", "Day Tracker"),
    ("🎁", "Rewards"),
    ("📈", "Dashboard"),
    ("👤", "Profile"),
]

for icon, name in pages:
    full = f"{icon} {name}"
    is_active = st.session_state.page == full
    if st.sidebar.button(
        full,
        use_container_width=True,
        key=f"nav_{name}",
        type="primary" if is_active else "secondary"
    ):
        st.session_state.page = full
        st.rerun()

page = st.session_state.page

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.username = None
    st.session_state.page = "🏠 Home"
    st.rerun()

if page == "🏠 Home":
    from datetime import datetime, date, timedelta

    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    st.markdown(f"""
        <div style='padding: 30px 0 10px 0;'>
            <h1 style='font-size:2.5rem; font-weight:800; color: var(--color-text-primary); margin:0;'>
                {greeting}, {username} 👋
            </h1>
            <p style='color:#888; margin-top:6px;'>Your study buddy is always here</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    today_mood = get_today_mood(username)

    if today_mood is None:
        st.markdown("### How are you feeling today?")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("😊  Good", use_container_width=True):
                save_mood(username, "good")
                st.rerun()
        with col2:
            if st.button("😐  Okay", use_container_width=True):
                save_mood(username, "okay")
                st.rerun()
        with col3:
            if st.button("😔  Not great", use_container_width=True):
                save_mood(username, "not great")
                st.rerun()
    else:
        mood_map = {
            "good": ("😊", "Glad you're feeling good!", "#8B5CF6"),
            "okay": ("😐", "That's alright -- let's make today count.", "#8B5CF6"),
            "not great": ("😔", "Tough day? The AI Chatbot is here for you.", "#dc3545")
        }
        icon, message, color = mood_map.get(today_mood, ("😐", "", "#888"))
        st.markdown(f"""
            <div style='background:{color}11; border-left:4px solid {color};
                        padding:12px 16px; border-radius:8px; margin-bottom:8px;'>
                <strong style='color:{color};'>{icon} {message}</strong>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Change mood", key="change_mood"):
            save_mood(username, None)
            st.rerun()

    st.markdown("---")

    col_left, col_right = st.columns([3, 2])

    with col_left:
       
        st.markdown("### Today's Tasks")
        today_tasks = get_today_tasks(username)
        pending = [t for t in today_tasks if t[5] == "pending"]
        done = [t for t in today_tasks if t[5] == "done"]

        if not today_tasks:
            st.info("No tasks for today. Add some in the Planner.")
        else:
            for task in today_tasks:
                task_id, title, subject, due_date, priority, status = task
                priority_colors = {"High": "#dc3545", "Medium": "#8B5CF6", "Low": "#8B5CF6"}
                color = priority_colors.get(priority, "#888")
                done_style = "text-decoration:line-through; color:#888;" if status == "done" else ""
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"""
                        <div style='padding:10px 0; border-bottom:1px solid #f0f0f0;'>
                            <span style='{done_style} font-size:0.95rem;'>{title}</span>
                            <span style='color:{color}; font-size:0.75rem; margin-left:8px;'>{priority}</span>
                            <span style='color:#888; font-size:0.75rem; margin-left:6px;'>{subject}</span>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if status == "pending":
                        if st.button("Done", key=f"home_done_{task_id}"):
                            complete_task(task_id)
                            st.rerun()

            completed = len(done)
            total = len(today_tasks)
            st.markdown(f"**{completed}/{total} tasks completed today**")
            st.progress(completed / total if total > 0 else 0)

      
        with st.expander("+ Add a task for today"):
            t_title = st.text_input("What do you need to do?", placeholder="e.g. Solve past paper")
            t_subject = st.text_input("Subject", placeholder="e.g. Maths")
            t_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            if st.button("Add Task", use_container_width=True):
                if t_title.strip():
                    add_task(username, t_title.strip(), t_subject.strip(), str(date.today()), t_priority)
                    st.rerun()

    with col_right:
      
        st.markdown("### Upcoming Exams")
        exams = get_all_exams(username)
        upcoming = []
        for exam in exams:
            exam_id, subject, exam_date_str, hours_per_day = exam
            exam_date_obj = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
            days_left = (exam_date_obj - date.today()).days
            if days_left >= 0:
                upcoming.append((subject, exam_date_str, days_left))

        if not upcoming:
            st.info("No upcoming exams. Add exams in the Planner.")
        else:
            for subject, exam_date_str, days_left in upcoming[:5]:
                if days_left == 0:
                    color = "#dc3545"
                    label = "Today!"
                elif days_left <= 3:
                    color = "#dc3545"
                    label = f"{days_left}d left"
                elif days_left <= 7:
                    color = "#dc3545"
                    label = f"{days_left}d left"
                elif days_left <= 14:
                    color = "#dc3545"
                    label = f"{days_left}d left"
                else:
                    color = "#dc3545"
                    label = f"{days_left}d left"

                st.markdown(f"""
                    <div style='border-left:4px solid {color};
                                padding:10px 14px;
                                border-radius:8px;
                                background:{color}11;
                                margin-bottom:10px;
                                display:flex;
                                justify-content:space-between;
                                align-items:center;'>
                        <div>
                            <strong style='color:var(--color-text-primary);'>{subject}</strong>
                            <p style='color:#888; font-size:0.8rem; margin:2px 0 0 0;'>{exam_date_str}</p>
                        </div>
                        <span style='color:{color}; font-weight:700;'>{label}</span>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        total_tasks = len(get_tasks(username))
        done_tasks = len(get_tasks(username, status="done"))
        st.metric("Tasks Completed", f"{done_tasks}/{total_tasks}")
    with col2:
        total_exams = len([e for e in get_all_exams(username) if (datetime.strptime(e[2], "%Y-%m-%d").date() - date.today()).days >= 0])
        st.metric("Upcoming Exams", total_exams)
    with col3:
        st.metric("Mood Today", today_mood.capitalize() if today_mood else "Not checked in")
elif page == "💊 Wellness":
    from datetime import date

    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>💊 Wellness</h1>
            <p style='color: #888;'>Track your health. Study smarter.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    today_str = str(date.today())
    today_wellness = get_today_wellness(username, today_str)

    if "show_wellness_form" not in st.session_state:
        st.session_state.show_wellness_form = False

    if today_wellness and not st.session_state.show_wellness_form:
        sleep, ate, water, phone, exercise, stress, focus, note = today_wellness

        score = 0
        if 6 <= sleep <= 8: score += 20
        elif sleep >= 5: score += 10
        if ate == "Yes": score += 20
        elif ate == "Partially": score += 10
        if water >= 8: score += 20
        elif water >= 4: score += 10
        if phone <= 2: score += 20
        elif phone <= 4: score += 10
        if exercise == "Yes": score += 20
        stress_deduct = (stress - 1) * 3
        score = max(0, score - stress_deduct)

        if score >= 80:
            score_color = "#8B5CF6"
            score_label = "Excellent"
        elif score >= 60:
            score_color = "#10B981"
            score_label = "Good"
        elif score >= 40:
            score_color = "#ffc107"
            score_label = "Average"
        else:
            score_color = "#dc3545"
            score_label = "Needs Work"

        import math
        radius = 55
        circumference = 2 * 3.14159 * radius
        dash_offset = circumference * (1 - score / 100)

        st.markdown(f"""
            <div style='text-align:center; padding:20px 0;'>
                <svg width='140' height='140' viewBox='0 0 140 140'>
                    <circle cx='70' cy='70' r='{radius}' fill='none' stroke='#2d333b' stroke-width='10'/>
                    <circle cx='70' cy='70' r='{radius}' fill='none' stroke='{score_color}' stroke-width='10'
                        stroke-dasharray='{circumference}' stroke-dashoffset='{dash_offset}'
                        stroke-linecap='round' transform='rotate(-90 70 70)'/>
                    <text x='70' y='65' text-anchor='middle' font-size='24' font-weight='800' fill='{score_color}'>{score}</text>
                    <text x='70' y='82' text-anchor='middle' font-size='10' fill='#888'>out of 100</text>
                </svg>
                <div style='font-size:1.2rem; font-weight:700; color:{score_color};'>{score_label} Day</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Today's Health Report")
        col1, col2, col3 = st.columns(3)
        col1.metric("😴 Sleep", f"{sleep}h")
        col2.metric("💧 Water", f"{water} glasses")
        col3.metric("📱 Phone", f"{phone}h")

        col4, col5, col6 = st.columns(3)
        col4.metric("🥗 Food", ate)
        col5.metric("🏃 Exercise", exercise)
        col6.metric("😰 Stress", f"{stress}/5")

        st.markdown("---")
        st.markdown("#### Feedback")

        if sleep < 6:
            st.error("😴 Less than 6 hours sleep -- your memory and focus will suffer today. Sleep earlier tonight.")
        elif sleep <= 8:
            st.success("😴 Perfect sleep! 6-8 hours is ideal for students.")
        else:
            st.warning("😴 Too much sleep -- over 8 hours can make you feel groggy and slow.")

        if water < 4:
            st.error("💧 Less than 4 glasses -- dehydration reduces brain performance by up to 10%!")
        elif water < 8:
            st.warning("💧 Decent water intake. Try to reach 8 glasses daily.")
        else:
            st.success("💧 Great hydration! Your brain is well fueled.")

        if phone > 6:
            st.error("📱 6+ hours on phone -- seriously cutting into your study time. Set a daily limit!")
        elif phone > 3:
            st.warning("📱 3+ hours on phone -- try to keep under 2 hours on study days.")
        else:
            st.success("📱 Good phone discipline! Keep it up.")

        if ate == "Yes":
            st.success("🥗 Healthy eating today -- good nutrition improves brain function!")
        elif ate == "Partially":
            st.warning("🥗 Partially healthy -- try to add more vegetables and reduce junk food.")
        else:
            st.error("🥗 Unhealthy eating today -- poor nutrition affects energy and focus.")

        if exercise == "Yes":
            st.success("🏃 Exercised today -- even 20 minutes of exercise improves focus by 20%!")
        else:
            st.warning("🏃 No exercise today -- try a 15 minute walk tomorrow.")

        if stress >= 4:
            st.error("😰 High stress detected! Talk to the AI Chatbot for support.")
            if st.button("Talk to AI Chatbot", use_container_width=True):
                st.session_state.page = "💬 AI Chatbot"
                st.rerun()
        elif stress >= 3:
            st.warning("😰 Moderate stress -- take short breaks and breathe.")
        else:
            st.success("😰 Low stress -- great mental state for studying!")

        if note:
            st.markdown(f"""
                <div style='background:#8B5CF611; border-left:4px solid #8B5CF6;
                            padding:12px 16px; border-radius:8px; margin-top:8px;'>
                    <strong>Your note:</strong> {note}
                </div>
            """, unsafe_allow_html=True)

        if focus:
            st.markdown(f"**Focus rating today:** {'⭐' * focus}{'☆' * (5 - focus)}")

        st.markdown("---")
        if st.button("Update today's wellness", use_container_width=True):
            st.session_state.show_wellness_form = True
            st.rerun()

    else:
        st.markdown("### Log Today's Wellness")
        st.caption("Takes 1 minute -- helps you and the app understand your health.")

        col1, col2 = st.columns(2)
        with col1:
            sleep_hours = st.slider("😴 Sleep hours last night", 0.0, 12.0, 7.0, 0.5)
            water_glasses = st.slider("💧 Glasses of water today", 0, 15, 6)
            phone_hours = st.slider("📱 Phone usage hours", 0.0, 12.0, 2.0, 0.5)
        with col2:
            ate_healthy = st.selectbox("🥗 Did you eat healthy?", ["Yes", "Partially", "No"])
            exercised = st.selectbox("🏃 Did you exercise?", ["Yes", "No"])
            stress_level = st.slider("😰 Stress level (1=calm, 5=very stressed)", 1, 5, 2)
            focus_rating = st.slider("📖 Study focus today (1=poor, 5=excellent)", 1, 5, 3)

        mental_note = st.text_input("🧠 One line about your day (optional)", placeholder="e.g. Felt tired but managed to study")

        if st.button("Save Wellness", use_container_width=True):
            save_wellness(username, sleep_hours, ate_healthy, water_glasses, phone_hours,
                         exercised, stress_level, focus_rating, mental_note, today_str)
            st.session_state.show_wellness_form = False
            st.success("Wellness logged!")
            st.rerun()

    st.markdown("---")
    st.markdown("### Last 7 Days")
    wellness_history = get_wellness_last_7_days(username)
    if wellness_history:
        for w in wellness_history[::-1]:
            sleep, ate, water, phone, exercise, stress, focus, w_date = w
            w_score = 0
            if 6 <= sleep <= 8: w_score += 20
            elif sleep >= 5: w_score += 10
            if ate == "Yes": w_score += 20
            elif ate == "Partially": w_score += 10
            if water >= 8: w_score += 20
            elif water >= 4: w_score += 10
            if phone <= 2: w_score += 20
            elif phone <= 4: w_score += 10
            if exercise == "Yes": w_score += 20
            w_score = max(0, w_score - (stress - 1) * 3)

            if w_score >= 80: w_color = "#8B5CF6"
            elif w_score >= 60: w_color = "#10B981"
            elif w_score >= 40: w_color = "#ffc107"
            else: w_color = "#dc3545"

            st.markdown(f"""
                <div style='border-left:4px solid {w_color}; padding:10px 14px;
                            border-radius:8px; background:{w_color}11; margin-bottom:8px;
                            display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <strong style='color:var(--color-text-primary);'>{w_date}</strong>
                        <span style='color:#888; font-size:0.8rem; margin-left:8px;'>
                            😴{sleep}h · 💧{water}g · 📱{phone}h · 😰{stress}/5
                        </span>
                    </div>
                    <span style='color:{w_color}; font-weight:700;'>{w_score}/100</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No wellness data yet. Log today's wellness above!")
elif page == "💬 AI Chatbot":
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>🤖 EduMind AI</h1>
            <p style='color: #888;'>Your personal student companion -- always here 💙</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "groq_history" not in st.session_state:
        st.session_state.groq_history = []
    if "pending_options" not in st.session_state:
        st.session_state.pending_options = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "session_saved" not in st.session_state:
        st.session_state.session_saved = False

    if len(st.session_state.chat_history) == 0:
        st.markdown("""
    <div style='
                padding: 25px; 
                border-radius: 15px; 
                margin-bottom: 20px;
                border-left: 4px solid #8B5CF6;'>
        <h4 style='color: #ffffff !important; margin:0;'>🤖 hey! i'm EduMind 👋</h4>
        <p style='color: #cccccc !important; margin:8px 0;'>not a robot, not a teacher -- just your study buddy who actually gets it 😊</p>
        <p style='color: #cccccc !important; margin:0;'>tell me what's going on. no judgment, promise!</p>
    </div>
""", unsafe_allow_html=True)

        st.markdown("#### 👇 What's on your mind?")
        col1, col2, col3 = st.columns(3)
        starter = None
        with col1:
            if st.button("😞 having a bad day", use_container_width=True):
                starter = "I'm having a really bad day"
        with col2:
            if st.button("📚 can't focus on studies", use_container_width=True):
                starter = "I can't seem to focus on my studies at all"
        with col3:
            if st.button("😰 exams are killing me", use_container_width=True):
                starter = "Exams are stressing me out so much"

        col4, col5, col6 = st.columns(3)
        with col4:
            if st.button("🎯 no idea what to do with my life", use_container_width=True):
                starter = "I have no idea what to do with my life or career"
        with col5:
            if st.button("😤 so frustrated rn", use_container_width=True):
                starter = "I'm so frustrated right now"
        with col6:
            if st.button("💬 just wanna talk", use_container_width=True):
                starter = "I just want to talk to someone"

        if starter:
            st.session_state.chat_history.append({"role": "user", "content": starter})
            st.session_state.pending_options = []
            st.rerun()

    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])

        if st.session_state.pending_options:
            st.markdown("**What kind of help do you need?**")
            cols = st.columns(len(st.session_state.pending_options))
            for i, option in enumerate(st.session_state.pending_options):
                with cols[i]:
                    if st.button(option, use_container_width=True, key=f"opt_{i}"):
                        st.session_state.chat_history.append({"role": "user", "content": option})
                        st.session_state.pending_options = []
                        st.rerun()

        last_msg = st.session_state.chat_history[-1]
        if last_msg["role"] == "user" and (
            len(st.session_state.groq_history) == 0 or
            st.session_state.groq_history[-1]["content"] != last_msg["content"]):

            try:
                from groq import Groq
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                from datetime import date as dt, datetime as dtime
                today_w = get_today_wellness(username, str(dt.today()))
                student_checkins = get_checkin_last_7_days(username)
                student_tasks_done = get_tasks(username, status="done")
                student_tasks_all = get_tasks(username)
                student_exams = get_all_exams(username)
                student_streak = get_streak(username)
                student_moods = get_mood_last_7_days(username)
                avg_study = round(sum([c[2] for c in student_checkins]) / len(student_checkins), 1) if student_checkins else 0
                comp_rate = round(len(student_tasks_done) / len(student_tasks_all) * 100) if student_tasks_all else 0
                bad_moods_count = sum(1 for m, _ in student_moods if m == "not great")
                upcoming_count = len([e for e in student_exams if (dtime.strptime(e[2], "%Y-%m-%d").date() - dt.today()).days >= 0])
                wellness_context = f"""Student Data: streak={student_streak}d, study={avg_study}h/day, tasks={comp_rate}%, exams={upcoming_count}, bad_moods={bad_moods_count}/7"""
                if today_w:
                    sleep, ate, water, phone, exercise, stress, focus, note = today_w
                    wellness_context += f" | Today: sleep={sleep}h, stress={stress}/5, phone={phone}h"
                    if stress >= 4: wellness_context += " | IMPORTANT: highly stressed"
                    if sleep < 6: wellness_context += f" | IMPORTANT: only slept {sleep}h"
                    if phone > 4 and avg_study < 2:
                        wellness_context += " | IMPORTANT: High phone usage + low study hours detected. Likely phone is causing distraction. Gently ask if phone is getting in the way of studying."
                    if phone > 4:
                        wellness_context += f" | Phone usage is high ({phone}h today). Student may be distracted."
                    if avg_study < 1:
                        wellness_context += " | Student is barely studying this week. Don't lecture — ask what's stopping them."
                    if bad_moods_count >= 3:
                        wellness_context += " | Student has been in bad mood most of this week. Be extra gentle and check in emotionally first."
                    if comp_rate < 30:
                        wellness_context += " | Task completion is very low. Student may be overwhelmed or struggling."
                student_profile_data = get_profile(username)
                if student_profile_data:
                    wellness_context += f" | Profile: {student_profile_data[2]}, {student_profile_data[3]}, subjects={student_profile_data[4]}"

                system_prompt = f"""You are EduMind AI -- a friendly, calm study buddy for Sri Lankan A/L and university students.
{wellness_context}

Your personality:
-> Friendly but neutral tone -- NO slang like machan, bro, da, ya unless student uses it first
-> Warm and real, never robotic or formal
-> Always UNDERSTAND the situation first before helping

MOST IMPORTANT RULE -- gather info before helping:

If student mentions EXAM or SUBJECT:
-> First ask: when is your exam?
-> Then ask: which subject and what topics?
-> Then ask: what kind of help -- study plan, explanations, past papers?
-> Only give advice AFTER you know these -- never jump to tips immediately

If student mentions STRESS or BAD DAY:
-> First ask: what's making you stressed -- studies, personal life, or something else?
-> Then ask: how long have you been feeling this way?
-> Only then offer support or suggestions based on their answer

If student mentions CAN'T FOCUS:
-> First ask: what subject or task are you trying to focus on?
-> Then ask: what's distracting you -- phone, noise, thoughts?
-> Then give ONE specific tip based on their answer

If student mentions CAREER or FUTURE:
-> First ask: what stream or field are you in -- A/L science, commerce, arts or university?
-> Then ask: what are you interested in or good at?
-> Then give realistic local career suggestions based on that

If student mentions FRUSTRATED:
-> First ask: what happened -- studies, friends, family, or something else?
-> Listen and acknowledge before giving any advice

If student just wants to TALK:
-> Be casual and friendly
-> Ask what's on their mind
-> Follow their lead, don't push advice

How to read short replies:
-> "ok", "mm", "fine", "oh" = don't give another tip, just check in naturally
-> "yes/no" = respond directly and continue the flow
-> If they seem done with the topic -> don't force it, move on

Conversation flow:
-> MAX 1 question or tip per reply
-> Never give tips back to back
-> Never repeat the same advice twice
-> Build conversation naturally -- understand first, help second

Language:
-> Match the language student uses -- Sinhala, Tamil, or English
-> NEVER use slang unless student uses it first

Hard rules:
If you have student data showing high phone + low study:
-> Don't lecture or guilt them
-> Gently ask "I noticed you've been on your phone a lot — is it hard to put it down when studying?"
-> Follow their lead after that

If student data shows high stress + low sleep:
-> Acknowledge it first before anything else
-> "Sounds like you're running on empty — that's really hard."
-> Max 3 sentences per reply
-> Don't ask a question in every single message
-> Never sound like a therapist, teacher, or motivational poster
-> Be genuinely helpful, not just cheerful"""

                messages = [{"role": "system", "content": system_prompt}]
                for msg in st.session_state.groq_history:
                    messages.append(msg)
                messages.append({"role": "user", "content": last_msg["content"]})

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    max_tokens=150,
                    temperature=0.7)

                ai_response = response.choices[0].message.content

                options = []
                trigger_words = ["idk", "don't know", "dont know",
                                 "not sure", "stuck", "confused",
                                 "help", "what should i do", "no idea"]

                if any(word in last_msg["content"].lower() for word in trigger_words):
                    options = ["📚 Study tips", "😔 I'm stressed", "🎯 Career help", "💬 Just talk"]

                st.session_state.pending_options = options
                st.session_state.groq_history.append({"role": "user", "content": last_msg["content"]})
                st.session_state.groq_history.append({"role": "assistant", "content": ai_response})
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

                if not st.session_state.session_saved:
                    title = st.session_state.chat_history[0]["content"][:40]
                    save_session(username, st.session_state.session_id, title)
                    st.session_state.session_saved = True
                save_message(username, st.session_state.session_id, "user", last_msg["content"])
                save_message(username, st.session_state.session_id, "assistant", ai_response)

                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")

    user_input = st.chat_input("Type anything here... 💬")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.pending_options = []
        st.rerun()

    if len(st.session_state.chat_history) > 0:
        st.markdown("---")
        if st.button("🗑️ Start Fresh"):
            st.session_state.chat_history = []
            st.session_state.groq_history = []
            st.session_state.pending_options = []
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.session_saved = False
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💬 Chat History")
    sessions = get_all_sessions(username)
    if sessions:
        for session_id, title, created_at in sessions:
            col1, col2 = st.sidebar.columns([3, 1])
            with col1:
                if st.button(f"💬 {title[:25]}...", key=f"load_{session_id}"):
                    st.session_state.chat_history = get_session_messages(session_id)
                    st.session_state.groq_history = st.session_state.chat_history.copy()
                    st.session_state.session_id = session_id
                    st.session_state.session_saved = True
                    st.session_state.pending_options = []
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{session_id}"):
                    delete_session(session_id)
                    st.rerun()
    else:
        st.sidebar.info("No history yet!")
elif page == "📅 Day Tracker":
    from datetime import date, datetime, timedelta

    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>📅 Day Tracker</h1>
            <p style='color: #888;'>Plan your day. Track your progress.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["Exams", "Tasks", "Recurring", "End of Day"])

    with tab1:
        st.markdown("### Add an Exam")
        col1, col2, col3 = st.columns(3)
        with col1:
            subject = st.text_input("Subject", placeholder="e.g. Mathematics", key="exam_subject")
        with col2:
            exam_date = st.date_input("Exam date", min_value=date.today(), key="exam_date")
        with col3:
            hours_per_day = st.number_input("Study hours per day", min_value=0.5, max_value=12.0, value=2.0, step=0.5, key="exam_hours")

        if st.button("Add Exam", use_container_width=True, key="add_exam_btn"):
            if subject.strip() == "":
                st.error("Please enter a subject name.")
            else:
                add_exam(username, subject.strip(), str(exam_date), hours_per_day)
                st.success(f"{subject} added!")
                st.rerun()

        st.markdown("---")
        st.markdown("### My Exams")
        exams = get_all_exams(username)

        if not exams:
            st.info("No exams added yet.")
        else:
            for exam in exams:
                exam_id, subject, exam_date_str, hours_per_day = exam
                exam_date_obj = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
                days_left = (exam_date_obj - date.today()).days

                if days_left < 0:
                    color = "#888"; label = "Passed"
                elif days_left == 0:
                    color = "#dc3545"; label = "Today!"
                elif days_left <= 3:
                    color = "#dc3545"; label = f"{days_left}d left"
                elif days_left <= 7:
                    color = "#dc3545"; label = f"{days_left}d left"
                elif days_left <= 14:
                    color = "#dc3545"; label = f"{days_left}d left"
                else:
                    color = "#dc3545"; label = f"{days_left}d left"

                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"""
                        <div style='border-left:4px solid {color}; padding:10px 14px;
                                    border-radius:8px; background:{color}11; margin-bottom:8px;'>
                            <strong style='color:var(--color-text-primary);'>{subject}</strong>
                            <span style='color:{color}; font-weight:700; float:right;'>{label}</span>
                            <p style='color:#888; font-size:0.8rem; margin:4px 0 0 0;'>{exam_date_str} · {hours_per_day}h/day</p>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Delete", key=f"del_exam_{exam_id}"):
                        delete_exam(exam_id)
                        st.rerun()

    with tab2:
        st.markdown("### Add a Task")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            t_title = st.text_input("Task", placeholder="e.g. Solve past paper", key="task_title")
        with col2:
            t_subject = st.text_input("Subject", placeholder="e.g. Maths", key="task_subject")
        with col3:
            t_due = st.date_input("Due date", value=date.today(), key="task_due")
        with col4:
            t_priority = st.selectbox("Priority", ["High", "Medium", "Low"], key="task_priority")

        if st.button("Add Task", use_container_width=True, key="add_task_btn"):
            if t_title.strip() == "":
                st.error("Please enter a task.")
            else:
                add_task(username, t_title.strip(), t_subject.strip(), str(t_due), t_priority)
                st.success("Task added!")
                st.rerun()

        st.markdown("---")
        st.markdown("### All Tasks")

        filter_status = st.radio("Show", ["Pending", "Done", "All"], horizontal=True)
        status_filter = {"Pending": "pending", "Done": "done", "All": None}
        tasks = get_tasks(username, status=status_filter[filter_status])

        if not tasks:
            st.info("No tasks found.")
        else:
            for task in tasks:
                task_id, title, subject, due_date, priority, status = task
                priority_colors = {"High": "#dc3545", "Medium": "#8B5CF6", "Low": "#8B5CF6"}
                color = priority_colors.get(priority, "#888")
                done_style = "text-decoration:line-through; opacity:0.5;" if status == "done" else ""

                col1, col2, col3 = st.columns([4, 1, 1])
                with col1:
                    st.markdown(f"""
                        <div style='padding:10px; border-bottom:1px solid #f0f0f0; margin-bottom: 4px;'>
                            <span style='{done_style} font-weight:600;'>{title}</span>
                            <span style='color:{color}; font-size:0.75rem; background:{color}22; padding:2px 6px; border-radius:4px; margin-left:8px;'>{priority}</span>
                            <span style='color:#888; font-size:0.75rem; margin-left:6px;'>{subject}</span>
                            <span style='color:#888; font-size:0.75rem; margin-left:6px;'>📅 {due_date}</span>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if status == "pending":
                        if st.button("Done", key=f"done_task_{task_id}", use_container_width=True):
                            complete_task(task_id)
                            st.rerun()
                with col3:
                    if st.button("Del", key=f"del_task_{task_id}", use_container_width=True):
                        delete_task(task_id)
                        st.rerun()

    with tab3:
        st.markdown("### Add Recurring Activity")
        st.caption("Things you do every week -- classes, tuition, gym etc. These auto-show in your daily plan.")

        col1, col2 = st.columns(2)
        with col1:
            r_title = st.text_input("Activity", placeholder="e.g. Physics class", key="rec_title")
            r_subject = st.text_input("Subject/Category", placeholder="e.g. Physics", key="rec_subject")
        with col2:
            r_days = st.multiselect("Which days?",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                key="rec_days")

        if st.button("Add Recurring Activity", use_container_width=True, key="add_rec_btn"):
            if r_title.strip() == "" or not r_days:
                st.error("Please enter activity and select at least one day.")
            else:
                add_recurring_task(username, r_title.strip(), r_subject.strip(), r_days)
                st.success("Recurring activity added!")
                st.rerun()

        st.markdown("---")
        st.markdown("### My Recurring Activities")
        recurring = get_recurring_tasks(username)

        if not recurring:
            st.info("No recurring activities added yet.")
        else:
            for rec in recurring:
                rec_id, title, subject, days = rec
         
                display_days = days
                if isinstance(days, str):
                    display_days = days.replace("[", "").replace("]", "").replace("'", "")

                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"""
                        <div style='border-left:4px solid #8B5CF6; padding:10px 14px;
                                    border-radius:8px; background:#8B5CF611; margin-bottom:8px;'>
                            <strong>{title}</strong>
                            <span style='color:#888; font-size:0.8rem; margin-left:8px;'>{subject}</span>
                            <p style='color:#8B5CF6; font-size:0.8rem; margin:4px 0 0 0;'>🗓️ {display_days}</p>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Del", key=f"del_rec_{rec_id}", use_container_width=True):
                        delete_recurring_task(rec_id)
                        st.rerun()

  
    with tab4:
        today_str = str(date.today())
        today_checkin = get_day_checkin(username, today_str)

        if today_checkin:
            rating, mood, study_hours = today_checkin
            st.success("You have already checked in for today!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Day Rating", f"{rating}/5")
            col2.metric("Mood", mood.capitalize())
            col3.metric("Study Hours", f"{study_hours}h")
            st.markdown("---")

        st.markdown("### End of Day Check-in")
        st.caption("Take 2 minutes to reflect on your day and plan tomorrow.")

        rating = st.slider("How was your day? (1 = terrible, 5 = amazing)", 1, 5, 3)
        eod_mood = st.selectbox("How are you feeling now?", ["Good", "Okay", "Tired", "Stressed", "Happy"])
        study_hours_logged = st.number_input("How many hours did you study today?", min_value=0.0, max_value=24.0, value=2.0, step=0.5)

        st.markdown("---")
        st.markdown("### Plan Tomorrow's Tasks")
        st.caption("Add up to 3 tasks for tomorrow.")

        tomorrow = date.today() + timedelta(days=1)
        t1 = st.text_input("Task 1", placeholder="e.g. Read Chapter 5", key="tmr_task1")
        t2 = st.text_input("Task 2", placeholder="e.g. Solve 10 past paper questions", key="tmr_task2")
        t3 = st.text_input("Task 3", placeholder="e.g. Review notes", key="tmr_task3")
        tmr_subject = st.text_input("Subject (for all tasks)", placeholder="e.g. Maths", key="tmr_subject")
        tmr_priority = st.selectbox("Priority", ["High", "Medium", "Low"], key="tmr_priority")

        if st.button("Save Check-in & Plan Tomorrow", use_container_width=True):
            save_day_checkin(username, rating, eod_mood.lower(), study_hours_logged, today_str)
            if t1.strip():
                add_task(username, t1.strip(), tmr_subject.strip(), str(tomorrow), tmr_priority)
            if t2.strip():
                add_task(username, t2.strip(), tmr_subject.strip(), str(tomorrow), tmr_priority)
            if t3.strip():
                add_task(username, t3.strip(), tmr_subject.strip(), str(tomorrow), tmr_priority)
            st.success("Check-in saved! Tomorrow's tasks added.")
            st.rerun()
elif page == "🎁 Rewards":
    from datetime import date, datetime
    import sqlite3
    import math

    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>🎁 Rewards</h1>
            <p style='color: #888;'>Keep your flame alive. Study every day.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    streak = get_streak(username)
    done_tasks = get_tasks(username, status="done")
    checkins = get_checkin_last_7_days(username)
    earned_badges = [b[0] for b in get_badges(username)]

    DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'planner.db')
    checkin_dates = set()
    checkin_hours = {}
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT checkin_date, study_hours FROM day_checkin')
        for row in c.fetchall():
            checkin_dates.add(row[0])
            checkin_hours[row[0]] = row[1]
        conn.close()
    except:
        pass

    today_str = date.today().strftime("%Y-%m-%d")
    
    if len(done_tasks) >= 1 and "First Task" not in earned_badges:
        award_badge(username, "First Task"); earned_badges.append("First Task")
    if len(done_tasks) >= 10 and "Task Master" not in earned_badges:
        award_badge(username, "Task Master"); earned_badges.append("Task Master")
    if streak >= 3 and "3 Day Streak" not in earned_badges:
        award_badge(username, "3 Day Streak"); earned_badges.append("3 Day Streak")
    if streak >= 7 and "7 Day Streak" not in earned_badges:
        award_badge(username, "7 Day Streak"); earned_badges.append("7 Day Streak")
    if streak >= 14 and "14 Day Streak" not in earned_badges:
        award_badge(username, "14 Day Streak"); earned_badges.append("14 Day Streak")
    if streak >= 30 and "30 Day Streak" not in earned_badges:
        award_badge(username, "30 Day Streak"); earned_badges.append("30 Day Streak")
    if len(checkins) >= 7 and "Perfect Week" not in earned_badges:
        award_badge(username, "Perfect Week"); earned_badges.append("Perfect Week")
    if len(get_all_exams(username)) >= 1 and "Exam Warrior" not in earned_badges:
        award_badge(username, "Exam Warrior"); earned_badges.append("Exam Warrior")

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT created_at FROM day_checkin WHERE strftime("%H", created_at) >= "22" LIMIT 1')
        if c.fetchone() and "Night Owl" not in earned_badges:
            award_badge(username, "Night Owl"); earned_badges.append("Night Owl")
        conn.close()
    except:
        pass

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT created_at FROM day_checkin WHERE strftime("%H", created_at) <= "08" LIMIT 1')
        if c.fetchone() and "Early Bird" not in earned_badges:
            award_badge(username, "Early Bird"); earned_badges.append("Early Bird")
        conn.close()
    except:
        pass

    if len(get_all_exams(username)) >= 5 and "Subject Master" not in earned_badges:
        award_badge(username, "Subject Master"); earned_badges.append("Subject Master")

    if streak == 0:
        flame = "💤"; flame_label = "No streak yet"
        flame_color = "#888"
        flame_msg = "Complete your end of day check-in to start your streak!"
        motivational = "Every journey starts with a single step. Start today!"
        progress_pct = 0
        next_milestone = 3
    elif streak <= 2:
        flame = "🔥"; flame_label = "Starting"
        flame_color = "#fd7e14"
        flame_msg = "Good start! Keep going tomorrow!"
        motivational = "You've started something great. Don't stop now!"
        progress_pct = streak / 3
        next_milestone = 3
    elif streak <= 6:
        flame = "🔥🔥"; flame_label = "Heating Up"
        flame_color = "#fd7e14"
        flame_msg = "You're building momentum -- don't break it!"
        motivational = "Consistency is the key to success. You're proving it!"
        progress_pct = streak / 7
        next_milestone = 7
    elif streak <= 13:
        flame = "🔥🔥🔥"; flame_label = "On Fire"
        flame_color = "#dc3545"
        flame_msg = "One week down! You're on fire!"
        motivational = "A week of dedication! Sri Lankan students who study daily score 40% higher!"
        progress_pct = streak / 14
        next_milestone = 14
    elif streak <= 29:
        flame = "🔥🔥🔥🔥"; flame_label = "Blazing"
        flame_color = "#dc3545"
        flame_msg = "Two weeks strong! You're unstoppable!"
        motivational = "Two weeks of consistency! You're in the top 10% of students!"
        progress_pct = streak / 30
        next_milestone = 30
    else:
        flame = "🔥🔥🔥🔥🔥"; flame_label = "Unstoppable"
        flame_color = "#8B5CF6"
        flame_msg = "30+ days! You are a legend!"
        motivational = "30 days strong! You have built a habit that will change your life!"
        progress_pct = 1.0
        next_milestone = streak

    radius = 60
    circumference = 2 * 3.14159 * radius
    dash_offset = circumference * (1 - min(progress_pct, 1.0))

    st.markdown(f"""
        <div style='text-align:center; padding:20px 0;'>
            <svg width='160' height='160' viewBox='0 0 160 160'>
                <circle cx='80' cy='80' r='{radius}' fill='none' stroke='#2d333b' stroke-width='12'/>
                <circle cx='80' cy='80' r='{radius}' fill='none' stroke='{flame_color}' stroke-width='12'
                    stroke-dasharray='{circumference}' stroke-dashoffset='{dash_offset}'
                    stroke-linecap='round' transform='rotate(-90 80 80)'/>
                <text x='80' y='72' text-anchor='middle' font-size='28' font-weight='800' fill='{flame_color}'>{streak}</text>
                <text x='80' y='92' text-anchor='middle' font-size='11' fill='#888'>day streak</text>
                <text x='80' y='108' text-anchor='middle' font-size='18'>{flame}</text>
            </svg>
            <div style='font-size:1.3rem; font-weight:700; color:{flame_color}; margin-top:8px;'>{flame_label}</div>
            <div style='font-size:0.9rem; color:#888; margin-top:4px;'>{flame_msg}</div>
            <div style='background:{flame_color}11; border-left:4px solid {flame_color}; 
                        padding:12px 16px; border-radius:8px; margin-top:16px; text-align:left;'>
                <strong style='color:{flame_color};'>💬 {motivational}</strong>
            </div>
            {f"<div style='color:#888; font-size:0.85rem; margin-top:8px;'>Next milestone: {next_milestone} days</div>" if streak < 30 else ""}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div style='background:#8B5CF611; border-radius:10px; padding:16px; text-align:center;'>
                <div style='font-size:2rem; font-weight:700; color:#8B5CF6;'>{streak}</div>
                <div style='color:#888; font-size:0.85rem;'>Current Streak 🔥</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div style='background:#8B5CF611; border-radius:10px; padding:16px; text-align:center;'>
                <div style='font-size:2rem; font-weight:700; color:#8B5CF6;'>{len(done_tasks)}</div>
                <div style='color:#888; font-size:0.85rem;'>Tasks Completed ✅</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div style='background:#8B5CF611; border-radius:10px; padding:16px; text-align:center;'>
                <div style='font-size:2rem; font-weight:700; color:#8B5CF6;'>{len(checkin_dates)}</div>
                <div style='color:#888; font-size:0.85rem;'>Total Days Tracked 📅</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### This Week")
    today = date.today()
    from datetime import timedelta
    week_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    cols = st.columns(7)
    for i, d in enumerate(week_days):
        checked = d in checkin_dates
        with cols[i]:
            if checked:
                st.markdown(f"""
                    <div style='background:#8B5CF622; border:2px solid #8B5CF6;
                                border-radius:10px; padding:10px 4px; text-align:center;'>
                        <div style='font-size:1.4rem;'>🔥</div>
                        <div style='font-size:0.7rem; color:#888; margin-top:4px;'>{day_labels[i]}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style='background:#2d333b22; border:2px solid #2d333b;
                                border-radius:10px; padding:10px 4px; text-align:center;'>
                        <div style='font-size:1.4rem;'>○</div>
                        <div style='font-size:0.7rem; color:#888; margin-top:4px;'>{day_labels[i]}</div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Badges")
    all_badges = [
        {"name": "First Task", "icon": "✅", "desc": "Complete your first task"},
        {"name": "Task Master", "icon": "🏆", "desc": "Complete 10 tasks"},
        {"name": "3 Day Streak", "icon": "🔥", "desc": "3 days in a row"},
        {"name": "7 Day Streak", "icon": "⚡", "desc": "7 days in a row"},
        {"name": "14 Day Streak", "icon": "💪", "desc": "14 days in a row"},
        {"name": "30 Day Streak", "icon": "👑", "desc": "30 days in a row"},
        {"name": "Perfect Week", "icon": "🌟", "desc": "7 day check-ins in a week"},
        {"name": "Exam Warrior", "icon": "⚔️", "desc": "Add your first exam"},
        {"name": "Night Owl", "icon": "🦉", "desc": "Check in after 10PM"},
        {"name": "Early Bird", "icon": "🐦", "desc": "Check in before 8AM"},
        {"name": "Subject Master", "icon": "📚", "desc": "Add 5+ exams"},
    ]

    cols = st.columns(4)
    for i, badge in enumerate(all_badges):
        earned = badge["name"] in earned_badges
        with cols[i % 4]:
            bg_color = "#8B5CF6" if earned else "#888"
            opacity = "1" if earned else "0.3"
            st.markdown(f"""
                <div style='background:{bg_color}11; border:2px solid {bg_color};
                            border-radius:12px; padding:12px; text-align:center;
                            margin-bottom:12px; opacity:{opacity};'>
                    <div style='font-size:1.8rem;'>{badge["icon"]}</div>
                    <div style='font-weight:700; font-size:0.85rem; 
                                color:var(--color-text-primary); margin-top:6px;'>{badge["name"]}</div>
                    <div style='color:#888; font-size:0.75rem; margin-top:4px;'>{badge["desc"]}</div>
                    {"<div style='color:#8B5CF6; font-size:0.7rem; margin-top:4px;'>✓ Earned</div>" if earned else "<div style='color:#888; font-size:0.7rem; margin-top:4px;'>Locked</div>"}
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### How to Keep Your Streak")
    st.markdown(f"""
        <div style='background:#8B5CF611; border-radius:12px; padding:16px;'>
            <p style='margin:6px 0;'>📅 Complete End of Day check-in every day</p>
            <p style='margin:6px 0;'>😊 Set your mood on the Home page daily</p>
            <p style='margin:6px 0;'>✅ Complete at least 1 task per day</p>
            <p style='margin:6px 0;'>🔥 Don't break the streak -- consistency is everything!</p>
        </div>
    """, unsafe_allow_html=True)
elif page == "📈 Dashboard":
    from datetime import date, datetime, timedelta
    import plotly.graph_objects as go
    import sqlite3

    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>📈 Dashboard</h1>
            <p style='color: #888;'>Your weekly progress at a glance.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    checkins = get_checkin_last_7_days(username)
    moods = get_mood_last_7_days(username)
    all_tasks = get_tasks(username)
    done_tasks = get_tasks(username, status="done")
    upcoming_exams = [e for e in get_all_exams(username)
                      if (datetime.strptime(e[2], "%Y-%m-%d").date() - date.today()).days >= 0]

    st.markdown("### This Week")
    col1, col2, col3 = st.columns(3)

    with col1:
        total_hours = sum([c[2] for c in checkins]) if checkins else 0
        avg_hours = round(total_hours / len(checkins), 1) if checkins else 0
        st.markdown(f"""
            <div style='background:#8B5CF611; border-radius:12px; padding:20px; text-align:center;'>
                <div style='font-size:2.5rem; font-weight:800; color:#8B5CF6;'>{total_hours}h</div>
                <div style='color:#888; font-size:0.9rem; margin-top:4px;'>Total Study Hours</div>
                <div style='color:#8B5CF6; font-size:0.8rem; margin-top:4px;'>avg {avg_hours}h/day</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        total_done = len(done_tasks)
        total_all = len(all_tasks)
        completion_rate = round(total_done / total_all * 100) if total_all else 0
        st.markdown(f"""
            <div style='background:#8B5CF611; border-radius:12px; padding:20px; text-align:center;'>
                <div style='font-size:2.5rem; font-weight:800; color:#8B5CF6;'>{total_done}</div>
                <div style='color:#888; font-size:0.9rem; margin-top:4px;'>Tasks Completed</div>
                <div style='color:#8B5CF6; font-size:0.8rem; margin-top:4px;'>out of {total_all} total</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        mood_counts = {"good": 0, "okay": 0, "not great": 0}
        for m, _ in moods:
            if m in mood_counts:
                mood_counts[m] += 1
        dominant_mood = max(mood_counts, key=mood_counts.get) if moods else None
        mood_display = {"good": "😊 Good", "okay": "😐 Okay", "not great": "😔 Struggling"}
        mood_color_map = {"good": "#8B5CF6", "okay": "#ffc107", "not great": "#dc3545"}
        m_label = mood_display.get(dominant_mood, "No data")
        m_color = mood_color_map.get(dominant_mood, "#888")
        st.markdown(f"""
            <div style='background:{m_color}11; border-radius:12px; padding:20px; text-align:center;'>
                <div style='font-size:2rem; font-weight:800; color:{m_color};'>{m_label}</div>
                <div style='color:#888; font-size:0.9rem; margin-top:4px;'>Mood This Week</div>
                <div style='color:{m_color}; font-size:0.8rem; margin-top:4px;'>most common</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    wellness_today = get_today_wellness(username, str(date.today()))
    wellness_7days = get_wellness_last_7_days(username)

    if wellness_7days:
        avg_sleep = round(sum([w[0] for w in wellness_7days]) / len(wellness_7days), 1)
        avg_stress = round(sum([w[5] for w in wellness_7days]) / len(wellness_7days), 1)
        avg_focus = round(sum([w[6] for w in wellness_7days]) / len(wellness_7days), 1)

        st.markdown("### Wellness This Week")
        col1, col2, col3 = st.columns(3)
        with col1:
            sleep_color = "#8B5CF6" if 6 <= avg_sleep <= 8 else "#dc3545"
            st.markdown(f"""
                <div style='background:{sleep_color}11; border-radius:10px; padding:16px; text-align:center;'>
                    <div style='font-size:2rem; font-weight:700; color:{sleep_color};'>{avg_sleep}h</div>
                    <div style='color:#888; font-size:0.85rem;'>Avg Sleep 😴</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            stress_color = "#dc3545" if avg_stress >= 4 else "#ffc107" if avg_stress >= 3 else "#8B5CF6"
            st.markdown(f"""
                <div style='background:{stress_color}11; border-radius:10px; padding:16px; text-align:center;'>
                    <div style='font-size:2rem; font-weight:700; color:{stress_color};'>{avg_stress}/5</div>
                    <div style='color:#888; font-size:0.85rem;'>Avg Stress 😰</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            focus_color = "#8B5CF6" if avg_focus >= 4 else "#ffc107" if avg_focus >= 3 else "#dc3545"
            st.markdown(f"""
                <div style='background:{focus_color}11; border-radius:10px; padding:16px; text-align:center;'>
                    <div style='font-size:2rem; font-weight:700; color:{focus_color};'>{avg_focus}/5</div>
                    <div style='color:#888; font-size:0.85rem;'>Avg Focus 📖</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("---")


    st.markdown("### Activity Heatmap")
    st.caption("Your daily study activity -- last 3 months")

    today = date.today()
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'planner.db')
    checkin_map = {}
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT study_hours, checkin_date FROM day_checkin ORDER BY checkin_date DESC LIMIT 90')
        for row in c.fetchall():
            checkin_map[row[1]] = row[0]
        conn.close()
    except:
        pass

    all_dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(55, -1, -1)]

    def get_color(hours):
        if hours == 0: return "#2d333b"
        elif hours < 2: return "#4c1d95"
        elif hours < 4: return "#7c3aed"
        elif hours < 6: return "#8b5cf6"
        else: return "#a78bfa"

    week_cols = []
    for i in range(0, len(all_dates), 7):
        week_cols.append(all_dates[i:i+7])
    while len(week_cols[-1]) < 7:
        week_cols[-1].append("")

    month_week_counts = {}
    for week in week_cols:
        if week[0]:
            month = datetime.strptime(week[0], "%Y-%m-%d").strftime("%b")
            month_week_counts[month] = month_week_counts.get(month, 0) + 1

    month_labels = "<td style='width:30px;'></td>"
    prev_month = ""
    for week in week_cols:
        if not week[0]:
            month_labels += "<td></td>"
            continue
        month = datetime.strptime(week[0], "%Y-%m-%d").strftime("%b")
        if month != prev_month:
            month_labels += f"<td colspan='{month_week_counts[month]}' style='font-size:11px;color:#8b949e;padding-bottom:4px;'>{month}</td>"
            prev_month = month

    day_names = ["Mon", "", "Wed", "", "Fri", "", ""]
    rows = ""
    for day_idx in range(7):
        label = day_names[day_idx]
        row = f"<tr><td style='font-size:11px;color:#8b949e;padding-right:8px;vertical-align:middle;width:30px;'>{label}</td>"
        for week in week_cols:
            d = week[day_idx] if day_idx < len(week) else ""
            h = checkin_map.get(d, 0) if d else 0
            color = get_color(h)
            title = f"{d}: {h}h" if d else ""
            row += f"<td><div title='{title}' style='width:10px;height:10px;border-radius:2px;background:{color};margin:1px;'></div></td>"
        row += "</tr>"
        rows += row

    legend = """
        <tr>
            <td colspan='100' style='padding-top:8px;'>
                <div style='display:flex;align-items:center;gap:4px;font-size:11px;color:#8b949e;'>
                    <span>Less</span>
                    <div style='width:12px;height:12px;border-radius:2px;background:#2d333b;'></div>
                    <div style='width:12px;height:12px;border-radius:2px;background:#4c1d95;'></div>
                    <div style='width:12px;height:12px;border-radius:2px;background:#7c3aed;'></div>
                    <div style='width:12px;height:12px;border-radius:2px;background:#8b5cf6;'></div>
                    <div style='width:12px;height:12px;border-radius:2px;background:#a78bfa;'></div>
                    <span>More</span>
                </div>
            </td>
        </tr>
    """

    table_content = "<tr>" + month_labels + "</tr>" + rows + legend
    st.markdown(
        "<div style='overflow-x:auto; padding:10px 0;'>"
        "<table style='border-collapse:collapse; width:100%;'>"
        + table_content +
        "</" + "table></div>",
        unsafe_allow_html=True
    )
    st.markdown("---")
   
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Study Hours -- Last 7 Days")
        if checkins:
            dates = [c[3] for c in checkins][::-1]
            hours = [c[2] for c in checkins][::-1]
            short_dates = [datetime.strptime(d, "%Y-%m-%d").strftime("%a %d %b") for d in dates]
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=short_dates,
                y=hours,
                marker_color="#8B5CF6",
                marker_line_color="#6d28d9",
                marker_line_width=1,
                width=0.3,
                text=[f"{h}h" for h in hours],
                textposition="outside",
                textfont=dict(size=12, color="#8B5CF6")
            ))
            fig.update_layout(
                showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=40, b=0),
                height=250,
                xaxis=dict(showgrid=False, tickfont=dict(size=11)),
                yaxis=dict(
                    gridcolor="rgba(139,92,246,0.15)",
                    ticksuffix="h",
                    tickfont=dict(size=11),
                    range=[0, max(hours) + 1] if hours else [0, 5]
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No study data yet. Complete end of day check-in to see charts.")

    with col_right:
        st.markdown("### Study Tips")
        st.caption("Based on your performance this week")

        if "dashboard_tips" not in st.session_state:
            st.session_state.dashboard_tips = None

        avg_h = round(sum([c[2] for c in checkins]) / len(checkins), 1) if checkins else 0
        done_pct = completion_rate
        mood_this_week = dominant_mood or "okay"

        if st.session_state.dashboard_tips is None:
            if st.button("Get AI Study Tips", use_container_width=True, key="get_tips"):
                try:
                    from groq import Groq
                    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                    prompt = f"""A Sri Lankan student's weekly performance:
    - Average study hours per day: {avg_h}h
    - Task completion rate: {done_pct}%
    - General mood this week: {mood_this_week}
    - Upcoming exams: {len(upcoming_exams)}

    Give 3 short, specific, practical study tips based on this data.
    Each tip max 2 sentences. Be direct and friendly. No bullet numbers needed. """

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=200,
                        temperature=0.7)
                    st.session_state.dashboard_tips = response.choices[0].message.content
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            tips = st.session_state.dashboard_tips.split("\n")
            for tip in tips:
                if tip.strip():
                    st.markdown(f"""
                        <div style='background:#8B5CF611; border-left:4px solid #8B5CF6;
                                    padding:10px 14px; border-radius:8px; margin-bottom:8px;'>
                            <span style='color:var(--color-text-primary); font-size:0.9rem;'>{tip.strip()}</span>
                        </div>
                    """, unsafe_allow_html=True)
            if st.button("Refresh Tips", key="refresh_tips"):
                st.session_state.dashboard_tips = None
                st.rerun()

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Task Completion")
        if all_tasks:
            pending_count = len(all_tasks) - len(done_tasks)
            done_count = len(done_tasks)
            st.markdown(f"""
                <div style='display:flex; gap:16px; margin-bottom:16px;'>
                    <div style='flex:1; background:#8B5CF611; border-radius:10px; padding:16px; text-align:center;'>
                        <div style='font-size:2rem; font-weight:700; color:#8B5CF6;'>{done_count}</div>
                        <div style='color:#888; font-size:0.85rem;'>Completed</div>
                    </div>
                    <div style='flex:1; background:#dc354511; border-radius:10px; padding:16px; text-align:center;'>
                        <div style='font-size:2rem; font-weight:700; color:#dc3545;'>{pending_count}</div>
                        <div style='color:#888; font-size:0.85rem;'>Pending</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.progress(done_count / len(all_tasks))
            st.caption(f"{completion_rate}% of all tasks completed")
        else:
            st.info("No tasks added yet.")

    with col_right:
        st.markdown("### Auto Risk Score")
        if checkins:
            avg_hours = sum([c[2] for c in checkins]) / len(checkins)
            avg_rating = sum([c[0] for c in checkins]) / len(checkins)
            bad_moods = sum(1 for m, _ in moods if m == "not great")
            completion = len(done_tasks) / len(all_tasks) if all_tasks else 0

            risk_score = 0
            if avg_hours < 1: risk_score += 3
            elif avg_hours < 2: risk_score += 2
            elif avg_hours < 3: risk_score += 1
            if avg_rating < 2: risk_score += 3
            elif avg_rating < 3: risk_score += 2
            elif avg_rating < 4: risk_score += 1
            if bad_moods >= 4: risk_score += 3
            elif bad_moods >= 2: risk_score += 2
            elif bad_moods >= 1: risk_score += 1
            if completion < 0.3: risk_score += 2
            elif completion < 0.6: risk_score += 1

            if risk_score >= 7:
                risk_label = "High Risk"
                risk_color = "#dc3545"
                risk_msg = "You need to take action now -- study more, sleep better, stay consistent."
            elif risk_score >= 4:
                risk_label = "Moderate Risk"
                risk_color = "#ffc107"
                risk_msg = "Things could be better -- try to build a more consistent routine."
            else:
                risk_label = "Low Risk"
                risk_color = "#8B5CF6"
                risk_msg = "You are on track -- keep up the good habits!"

            st.markdown(f"""
                <div style='background:{risk_color}11; border-left:4px solid {risk_color};
                            padding:20px; border-radius:12px; text-align:center;'>
                    <div style='font-size:1.5rem; font-weight:700; color:{risk_color};'>{risk_label}</div>
                    <div style='color:#888; font-size:0.85rem; margin-top:8px;'>{risk_msg}</div>
                    <div style='font-size:2rem; font-weight:800; color:{risk_color}; margin-top:12px;'>{risk_score}/11</div>
                    <div style='color:#888; font-size:0.75rem;'>risk score</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Complete at least one end of day check-in to see your risk score.")
elif page == "👤 Profile":
    from datetime import date, datetime

    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>👤 Profile</h1>
            <p style='color: #888;'>Your academic profile and stats.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    profile = get_profile(username)
    checkins = get_checkin_last_7_days(username)
    done_tasks = get_tasks(username, status="done")
    all_tasks = get_tasks(username)
    streak = get_streak(username)
    wellness_7 = get_wellness_last_7_days(username)

    total_study = sum([c[2] for c in checkins]) if checkins else 0
    completion_rate = round(len(done_tasks) / len(all_tasks) * 100) if all_tasks else 0
    avg_wellness = 0
    if wellness_7:
        scores = []
        for w in wellness_7:
            s = 0
            sleep, ate, water, phone, exercise, stress = w[0], w[1], w[2], w[3], w[4], w[5]
            if 6 <= sleep <= 8: s += 20
            elif sleep >= 5: s += 10
            if ate == "Yes": s += 20
            elif ate == "Partially": s += 10
            if water >= 8: s += 20
            elif water >= 4: s += 10
            if phone <= 2: s += 20
            elif phone <= 4: s += 10
            if exercise == "Yes": s += 20
            s = max(0, s - (stress - 1) * 3)
            scores.append(s)
        avg_wellness = round(sum(scores) / len(scores))

    st.markdown(f"""
        <div style='background:#8B5CF611; border:2px solid #8B5CF6;
                    border-radius:16px; padding:24px; text-align:center; margin-bottom:20px;'>
            <div style='font-size:4rem;'>👤</div>
            <div style='font-size:1.8rem; font-weight:800; color:var(--color-text-primary); margin-top:8px;'>
                {profile[0] if profile and profile[0] else username}
            </div>
            <div style='color:#888; font-size:0.9rem; margin-top:4px;'>@{username}</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div style='background:#8B5CF611; border-radius:10px; padding:16px; text-align:center;'>
            <div style='font-size:1.8rem; font-weight:700; color:#8B5CF6;'>{streak}</div>
            <div style='color:#888; font-size:0.8rem;'>Day Streak 🔥</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div style='background:#8B5CF611; border-radius:10px; padding:16px; text-align:center;'>
            <div style='font-size:1.8rem; font-weight:700; color:#8B5CF6;'>{len(done_tasks)}</div>
            <div style='color:#888; font-size:0.8rem;'>Tasks Done ✅</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div style='background:#8B5CF611; border-radius:10px; padding:16px; text-align:center;'>
            <div style='font-size:1.8rem; font-weight:700; color:#8B5CF6;'>{total_study}h</div>
            <div style='color:#888; font-size:0.8rem;'>Study Hours 📚</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div style='background:#8B5CF611; border-radius:10px; padding:16px; text-align:center;'>
            <div style='font-size:1.8rem; font-weight:700; color:#8B5CF6;'>{avg_wellness}</div>
            <div style='color:#888; font-size:0.8rem;'>Wellness Score 💊</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Edit Profile")

    col1, col2 = st.columns(2)
    with col1:
        display_name = st.text_input("Display Name",
            value=profile[0] if profile and profile[0] else "",
            placeholder="e.g. Abii")
        university = st.text_input("University / School",
            value=profile[1] if profile and profile[1] else "",
            placeholder="e.g. University of Kelaniya")
        stream_options = ["A/L Science", "A/L Commerce", "A/L Arts", "University - IT",
             "University - Engineering", "University - Medicine",
             "University - Business", "University - Arts", "Other"]
        stream = st.selectbox("Stream", stream_options,
            index=stream_options.index(profile[2]) if profile and profile[2] in stream_options else 0)
    with col2:
        year_options = ["1st Year", "2nd Year", "3rd Year", "4th Year", "A/L Year 1", "A/L Year 2"]
        year = st.selectbox("Year of Study", year_options,
            index=year_options.index(profile[3]) if profile and profile[3] in year_options else 0)
        study_goal = st.slider("Daily Study Goal (hours)", 1.0, 12.0,
            float(profile[5]) if profile and profile[5] else 4.0, 0.5)
        subjects_input = st.text_input("Your Subjects (comma separated)",
            value=profile[4] if profile and profile[4] else "",
            placeholder="e.g. Maths, Physics, Chemistry")

    if st.button("Save Profile", use_container_width=True):
        subjects_list = [s.strip() for s in subjects_input.split(",") if s.strip()]
        save_profile(username, display_name, university, stream, year, subjects_list, study_goal)
        st.success("Profile saved!")
        st.rerun()

    st.markdown("---")
    st.markdown("### Badges Earned")
    earned = get_badges(username)
    if earned:
        badge_icons = {
            "First Task": "✅", "Task Master": "🏆", "3 Day Streak": "🔥",
            "7 Day Streak": "⚡", "14 Day Streak": "💪", "30 Day Streak": "👑",
            "Perfect Week": "🌟", "Exam Warrior": "⚔️", "Night Owl": "🦉",
            "Early Bird": "🐦", "Subject Master": "📚"
        }
        cols = st.columns(4)
        for i, (name, earned_at) in enumerate(earned):
            with cols[i % 4]:
                icon = badge_icons.get(name, "🏅")
                st.markdown(f"""
                    <div style='background:#8B5CF611; border:2px solid #8B5CF6;
                                border-radius:12px; padding:12px; text-align:center; margin-bottom:8px;'>
                        <div style='font-size:1.8rem;'>{icon}</div>
                        <div style='font-weight:700; font-size:0.8rem; color:var(--color-text-primary);'>{name}</div>
                        <div style='color:#888; font-size:0.7rem;'>{earned_at}</div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No badges yet -- complete tasks and check in daily to earn badges!")