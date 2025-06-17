import streamlit as st
from datetime import datetime
from detector import ObjectionDetector
from fallback_llm import get_fallback_objection
from email_util import log_email, send_followup_email
from logger import logger
from utils import *
from objection import *



import os
import pandas as pd

LOG_FILE = "chat_log.csv"

# Create chat log file if it doesn't exist
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["timestamp", "role", "message", "objection", "category", "suggestion"]).to_csv(LOG_FILE, index=False)

def log_message(role, message, objection=None, category=None, suggestion=None):
    df = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": role,
        "message": message,
        "objection": objection or "",
        "category": category or "",
        "suggestion": suggestion or ""
    }])
    df.to_csv(LOG_FILE, mode='a', header=False, index=False)

# Streamlit UI Setup
st.set_page_config(page_title="Objection Detector", layout="centered")
st.title("🎯 Real-Time Sales Objection Detector + Chatbot")

# Initialize state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()
if "show_email_prompt" not in st.session_state:
    st.session_state.show_email_prompt = False
if "email_collected" not in st.session_state:
    st.session_state.email_collected = False

# Show chat history
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Chat Input
user_input = st.chat_input("You (CUSTOMER):")
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)
    log_message("CUSTOMER", user_input)

    detector = ObjectionDetector()
    category = detector.detect(user_input)
    if category:
        suggestion = detector.suggest_response(category)
        objection = f"{category.value} objection detected."
    else:
        objection, suggestion = get_fallback_objection(user_input)
        category = "LLM"

    if objection:
        rep_response = f"🛑 **Objection Detected**: *{objection}*\n\n💡 **Suggested Response**: {suggestion}"
    else:
        rep_response = "👍 Got it! Thanks for sharing."

    st.session_state.chat_history.append(("assistant", rep_response))
    with st.chat_message("assistant"):
        st.markdown(rep_response)

    log_message("REP", rep_response, objection, category, suggestion)

# Email popup prompt after 60 seconds
elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
if elapsed > 60 and not st.session_state.email_collected:
    st.session_state.show_email_prompt = True

if st.session_state.show_email_prompt and not st.session_state.email_collected:
    st.markdown("---")
    st.subheader("📧 We'd love to follow up with you!")
    email_input = st.text_input("Enter your email address below:")

    if email_input:
        if "@" in email_input and "." in email_input:
            log_email(email_input)
            sent = send_followup_email(email_input)
            if sent:
                st.success("✅ Email saved and follow-up sent!")
            else:
                st.warning("⚠️ Email saved, but failed to send follow-up.")
            st.session_state.email_collected = True
        else:
            st.warning("⚠️ Please enter a valid email address.")
