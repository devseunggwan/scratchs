import streamlit as st
import streamlit_authenticator as stauth
import yaml

with open("./.streamlit/auth.yaml") as f:
    config = yaml.load(f, stauth.SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)

name, authentication_status, username = authenticator.login("main")

if authentication_status is False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
