import base64
import os
import random
import secrets
from datetime import datetime

import jwt
import streamlit as st
from dotenv import load_dotenv
from faker import Faker


class JwtUtil:
    def __init__(self):
        self.secret = os.getenv("JWT_SECRET")
        self.jwt_expiration = 60 * 60 * 24

    def generate_secret_key(self, length=64):
        random_bytes = secrets.token_bytes(length)
        return base64.urlsafe_b64encode(random_bytes).decode("utf-8")

    def generate(self, payload: dict):
        payload["iat"] = datetime.now().timestamp()
        payload["exp"] = datetime.now().timestamp() + self.jwt_expiration

        return jwt.encode(payload, self.secret, algorithm="HS512")

    def validate(self, token: str) -> dict | bool:
        try:
            decoded_token = jwt.decode(token, self.secret, algorithms=["HS512"])
            return decoded_token
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False


if __name__ == "__main__":
    load_dotenv()

    jwt_util = JwtUtil()
    faker = Faker()

    with st.form(key="jwt_form"):
        st.markdown("## JWT Generator")
        idx = st.text_input("idx", value=random.randint(1, 1000))
        email = st.text_input("email", value=faker.email())
        nickname = st.text_input("nickname", value=faker.name())

        if st.form_submit_button("Generate JWT"):
            jwt_payload = {"idx": idx, "email": email, "nickname": nickname}
            jwt_token = jwt_util.generate(jwt_payload)

            if jwt_token:
                st.write(jwt_token)
            else:
                st.write("Failed to generate JWT")

    with st.form(key="jwt_validator"):
        st.markdown("## JWT Validator")
        jwt_token = st.text_area("Token")
        if st.form_submit_button("Validate JWT"):
            decoded_token = jwt_util.validate(jwt_token)

            if decoded_token:
                st.write(decoded_token)
            else:
                st.write("Failed to validate JWT")
