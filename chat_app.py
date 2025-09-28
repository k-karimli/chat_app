import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase

# Initialize Firebase with service account key
SERVICE_ACCOUNT_PATH = 'user.json'
DATABASE_URL = 'https://chat-app-7f2b4-default-rtdb.firebaseio.com/'
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': DATABASE_URL
    })

# Set Firebase rules
rules_ref = db.reference('.settings/rules')
rules_ref.set({
    "rules": {
        ".read": True,
        ".write": True
    }
})

st.title("Streamlit Chat App")

# User registration/login
username = st.text_input("Enter your username:")
if st.button("Register/Login"):
    user_ref = db.reference(f'users/{username}')
    if not user_ref.get():
        user_ref.set({"username": username})
    st.session_state['username'] = username

if 'username' in st.session_state:
    st.subheader(f"Welcome, {st.session_state['username']}")
    # Chat interface
    chat_with = st.text_input("Chat with (username):")
    message = st.text_input("Type your message:")
    if st.button("Send"):
        msg_ref = db.reference('messages').push()
        msg_ref.set({
            "from": st.session_state['username'],
            "to": chat_with,
            "message": message
        })
    # Display messages
    st.write("--- Chat History ---")
    messages_ref = db.reference('messages')
    messages = messages_ref.get()
    if messages:
        for msg_id, msg in messages.items():
            if (msg['from'] == st.session_state['username'] and msg['to'] == chat_with) or \
               (msg['from'] == chat_with and msg['to'] == st.session_state['username']):
                sender = "You" if msg['from'] == st.session_state['username'] else chat_with
                st.write(f"{sender}: {msg['message']}")


