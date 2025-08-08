import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Adaptive Learning App")

BASE_URL = "http://127.0.0.1:8000"

# Sidebar menu
st.sidebar.title("Menu")
option = st.sidebar.radio("Choose an option", ["Register", "Login", "Upload CSVs", "View Table"])

st.title(f"{option} Section")

# 🔐 Register
if option == "Register":
    user_id = st.text_input("User ID")
    user_name = st.text_input("User Name")
    password = st.text_input("Password", type="password")
    preferences = st.text_area("Preferences")

    if st.button("Register"):
        payload = {
            "user_id": user_id,
            "user_name": user_name,
            "password": password,
            "preferences": preferences
        }
        response = requests.post(f"{BASE_URL}/register", json=payload)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json()["detail"])

# 🔓 Login
elif option == "Login":
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        payload = {
            "user_id": user_id,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/login", json=payload)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json()["detail"])

# 📤 Upload CSVs
elif option == "Upload CSVs":
    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            files = {"file": (file.name, file.getvalue(), "text/csv")}
            response = requests.post(f"{BASE_URL}/upload_csv/", files=files)
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(f"Upload failed: {response.json().get('detail', 'Unknown error')}")

# 📊 Enhanced View Table
elif option == "View Table":
    table_name = st.text_input("Enter table name (from uploaded CSV):")
    search_query = st.text_input("Search logic (e.g., subject == 'Geography' and difficulty == 'Hard')")
    select_columns = st.text_input("Columns to display (comma-separated, e.g., subject,title,description)")

    if st.button("View Table") and table_name:
        params = {
            "query": search_query,
            "columns": select_columns
        }
        response = requests.get(f"{BASE_URL}/search_table/{table_name}", params=params)

        if response.status_code == 200:
            data = response.json()
            if data:
                st.dataframe(pd.DataFrame(data))
            else:
                st.warning("No rows matched your query.")
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")