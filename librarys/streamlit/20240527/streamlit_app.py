"""
localhost:8502
"""
import streamlit as st
from streamlit_local_storage import LocalStorage

local_stroage = LocalStorage()

js_code = """
<script>
    const parentUrl = 'localhost:8501';

    const receiveMessage = (event) => {
        if (event.origin === undefined || event.data === undefined) return;
        if (!event.origin.includes(parentUrl)) return;

        const message = JSON.parse(event.data);
        if (message.type === 'sendToken') {
            const sendTokenMessage = message;
            setLocalstorage('token', sendTokenMessage.data.token);
            console.log('Token received: ', sendTokenMessage.data.token);
        }
    };

    // ...

    // 페이지 로드 시 실행
    if (window.opener !== null) {
        window.removeEventListener('message', receiveMessage);
        window.addEventListener('message', receiveMessage, false);
        
        const readyMessage = {
            type: 'ready',
            data: undefined,
        };

        window.opener.postMessage(JSON.stringify(readyMessage), parentUrl);
    }
</script>
"""

if __name__ == "__main__":
    st.markdown(js_code, unsafe_allow_html=True)

    st.title("LocalStroage Test")

    with st.form("send_token"):
        send_token = st.text_input("Token")

        if st.form_submit_button("Send Token"):
            if send_token != "":
                local_stroage.setItem("token", send_token)
                st.success("Token sent", icon="🚀")
            else:
                st.error("Token is empty", icon="🔥")

    with st.form("get_token"):
        if st.form_submit_button("Get Token"):
            received_token = local_stroage.getItem("token")
            st.success(f"Token received: {received_token}", icon="🚀")
