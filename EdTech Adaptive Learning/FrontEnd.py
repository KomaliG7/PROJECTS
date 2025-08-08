import streamlit as st
import requests
from ollama import chat

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="EdTech Adaptive Learning Platform", layout="centered")
st.title("📚 EdTech Adaptive Learning Platform")

menu = st.sidebar.selectbox("Choose a feature", [
    "Submit Learning Data",
    "Get Recommendations",
    "Adaptive Assessment",
    "Feedback Analyzer",
    "Chatbot Tutor"
])

if menu == "Submit Learning Data":
    st.header("📥 Submit Learning Data")
    with st.form("submit_form"):
        user_id = st.number_input("User ID", min_value=1, value=101)
        topic = st.selectbox("Topic", ["Algebra", "Geometry", "Calculus", "Trigonometry", "Statistics"])
        time_spent = st.slider("Time Spent (minutes)", 5, 120, 30)
        quiz_score = st.slider("Quiz Score", 0, 100, 70)
        preference = st.selectbox("Learning Preference", ["Visual", "Text", "Audio", "Interactive"])
        feedback = st.text_area("Feedback")
        rating = st.slider("Content Rating (1-5)", 1, 5, 4)
        submitted = st.form_submit_button("Submit")

    if submitted:
        payload = {
            "user_id": user_id,
            "topic": topic,
            "time_spent": time_spent,
            "quiz_score": quiz_score,
            "preference": preference,
            "feedback": feedback,
            "rating": rating
        }
        res = requests.post(f"{API_URL}/submit_data", json=payload)
        st.success(res.json().get("message"))

elif menu == "Get Recommendations":
    st.header("📌 Learning Recommendations")
    user_id = st.number_input("Enter your User ID", min_value=1)
    if st.button("Get Recommendations"):
        res = requests.get(f"{API_URL}/get_recommendations/{user_id}")
        if res.status_code == 200:
            data = res.json()
            st.write("### Recommended Topics:")
            st.write(data.get("recommended_topics", []))
        else:
            st.error("User not found.")

elif menu == "Adaptive Assessment":
    st.header("📝 Adaptive Assessment")
    user_id = st.number_input("Enter your User ID for assessment", min_value=1)
    if st.button("Generate Assessment"):
        history_res = requests.get(f"{API_URL}/get_recommendations/{user_id}")
        if history_res.status_code != 200:
            st.error("User not found.")
        else:
            topics = ', '.join(history_res.json().get("recommended_topics", []))
            prompt = f"Generate 3 personalized assessment questions for a student with average performance in topics like {topics}. Make them adaptive and helpful."

            try:
                response = chat(
                    model='llama3',
                    messages=[{'role': 'user', 'content': prompt}]
                )
                st.write("### Level: AI-Generated")
                st.write("### Questions:")
                for line in response.message.content.strip().split('\n'):
                    if line.strip():
                        st.write(f"- {line.strip()}")
            except Exception as e:
                st.error(f"Failed to generate questions: {e}")

elif menu == "Feedback Analyzer":
    st.header("💬 Feedback Sentiment Analysis")
    feedback = st.text_area("Enter feedback to analyze")
    if st.button("Analyze Sentiment"):
        res = requests.post(f"{API_URL}/analyze_feedback", json={"feedback": feedback})
        if res.status_code == 200:
            sentiment = res.json().get("feedback_sentiment")
            st.write(f"**Label:** {sentiment['label']}, **Score:** {round(sentiment['score'], 2)}")
        else:
            st.error("Analysis failed.")

elif menu == "Chatbot Tutor":
    st.header("🤖 AI Tutor Chatbot (Ollama)")
    query = st.text_input("Ask something about your subject")
    if st.button("Ask"):
        try:
            response = chat(
                model='llama3',
                messages=[{'role': 'user', 'content': query}]
            )
            st.write("### Tutor Response:")
            st.write(response.message.content)
        except Exception as e:
            st.error(f"Chatbot error: {e}")