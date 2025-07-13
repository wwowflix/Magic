import streamlit as st

# Dummy user store
USERS = {
    "admin": "password123",
    "user": "secret"
}

st.title("🔐 Login Demo")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if USERS.get(user) == pw:
            st.session_state["authenticated"] = True
            st.success("✅ Logged in!")
        else:
            st.error("Invalid credentials")
else:
    st.write("🎉 You are logged in!")
    if st.button("Logout"):
        st.session_state["authenticated"] = False
