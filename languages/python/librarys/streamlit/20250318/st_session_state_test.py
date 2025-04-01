import streamlit as st

st.session_state.reservoir_networks = {
    "ethereum": "api",
    "polygon": "api-polygon",
    "bsc": "api-bsc",
    "arbitrum": "api-arbitrum",
    "optimism": "api-optimism",
    "base": "api-base",
    "linea": "api-linea",
    "avalanche": "api-avalanche",
}
st.session_state.models = ["gpt-4o", "gpt-4-turbo", "gpt-o3-mini"]

st.selectbox("Selected Network", st.session_state.reservoir_networks)
st.text_input("Collection ID", key="nft_collection_id")

with st.expander("LLM Model Options"):
    st.selectbox("Selected Model", st.session_state.models, key="selected_model")
    st.slider("NFT Images", 1, 20, 10, 1, key="nft_images")
    st.slider("Max Tokens", 50, 1000, 500, 50, key="max_tokens")
    st.slider("Question Count", 1, 3, 1, 1, key="question_count")

st.write(st.session_state.models)

st.write(st.session_state.reservoir_networks["ethereum"])

st.write(st.session_state)
