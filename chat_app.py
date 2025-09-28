import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase

# Initialize Firebase with service account key
SERVICE_ACCOUNT_PATH = '/home/hp/ufaz_25/programing/python_25/chat-app-7f2b4-firebase-adminsdk-fbsvc-2d6062c353.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.title("Streamlit Chat App")

# User registration/login
username = st.text_input("Enter your username:")
if st.button("Register/Login"):
    user_ref = db.collection('users').document(username)
    if not user_ref.get().exists:
        user_ref.set({"username": username})
    st.session_state['username'] = username

if 'username' in st.session_state:
    st.subheader(f"Welcome, {st.session_state['username']}")
    # Chat interface
    chat_with = st.text_input("Chat with (username):")
    message = st.text_input("Type your message:")
    if st.button("Send"):
        db.collection('messages').add({
            "from": st.session_state['username'],
            "to": chat_with,
            "message": message
        })
    # Display messages
    st.write("--- Chat History ---")
    messages = db.collection('messages').where('from', '==', st.session_state['username']).where('to', '==', chat_with).stream()
    for msg in messages:
        st.write(f"You: {msg.to_dict()['message']}")
    messages = db.collection('messages').where('from', '==', chat_with).where('to', '==', st.session_state['username']).stream()
    for msg in messages:
        st.write(f"{chat_with}: {msg.to_dict()['message']}")

