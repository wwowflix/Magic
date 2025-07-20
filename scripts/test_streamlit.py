import streamlit as st

st.title("[OK] Streamlit Test App")

st.write("If you see this message, Streamlit is working great!")

x = st.slider("Select a value", 0, 100, 25)
st.write("You selected:", x)



