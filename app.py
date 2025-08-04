import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Student Growth Analyst Dashboard", layout="wide")

st.title("📊 Growth Analyst: Student Dashboard")

if "data" not in st.session_state:
    st.session_state["data"]= pd.DataFrame(columns=["Date", "Study Hours", "Subjects", "Grade", "Mood", "Focus"])

df=st.session_state["data"]

# Sidebar - Data Entry
st.sidebar.header("📥 Log Today's Progress")
with st.sidebar.form("log_form"):
    today = date.today()
    study_hours = st.number_input("Study Hours", 0.0, 24.0, 1.0)
    subject = st.selectbox("Subject", ["Math", "Science", "English", "History", "CS"])
    grade = st.slider("Performance Grade (out of 100)", 0, 100, 75)
    mood = st.selectbox("Mood", ["🙂 Happy", "😐 Neutral", "🙁 Stressed"])
    focus = st.slider("Focus Level (1–10)", 1, 10, 7)
    submit = st.form_submit_button("Add Entry")

    if submit:
        new_row = {
            "Date": today,
            "Study Hours": study_hours,
            "Subject": subject,
            "Grade": grade,
            "Mood": mood,
            "Focus": focus
        }
        st.session_state["data"] = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Entry added successfully!")

df=st.session_state["data"]

if df.empty:
    st.warning("No data yet! Log your progress in the sidebar to see insights.")

else:
    # Study Hours Trend
    st.subheader("📈 Study Hours Over Time")
    fig1 = px.line(df, x="Date", y="Study Hours", color="Subject", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    # Grades per Subject
    st.subheader("🏅 Grade Distribution by Subject")
    fig2 = px.box(df, x="Subject", y="Grade", points="all", color="Subject")
    st.plotly_chart(fig2, use_container_width=True)

    # Focus Level Trend
    st.subheader("🧠 Focus Trend Over Time")
    focus_df = df.groupby("Date")["Focus"].mean().reset_index()
    fig3 = px.line(focus_df, x="Date", y="Focus", title="Average Daily Focus Level")
    st.plotly_chart(fig3, use_container_width=True)

    # Study vs Grade Correlation
    st.subheader("📊 Study Hours vs Grade")
    fig4 = px.scatter(df, x="Study Hours", y="Grade", color="Subject", trendline="ols")
    st.plotly_chart(fig4, use_container_width=True)

    # Download data
    st.download_button("⬇️ Download Data as CSV", df.to_csv(index=False), "student_growth_data.csv", "text/csv")
