import streamlit as st
import openai

# API 키를 외부에서 안전하게 불러오기
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 페이지 기본 설정
st.set_page_config(page_title="주택임대소득 AI 세무사", layout="wide")
st.title("🏠 주택임대소득 AI 세무사")
st.markdown("국세청 기준 기반, 주택임대소득 세금 상담 챗봇입니다.")

# 초기 챗로그 세팅
if "chat_log" not in st.session_state:
    st.session_state.chat_log = [
        {"role": "assistant", "content": "이 챗봇은 참고용이며 법적 책임을 지지 않습니다. 동의하시면 질문을 입력해 주세요."}
    ]

# 사용자 질문 입력
user_input = st.chat_input("질문을 입력하세요...")

# 질문 처리
if user_input:
    st.session_state.chat_log.append({"role": "user", "content": user_input})
    try:
        with st.spinner("답변 생성 중입니다..."):
            client = openai.OpenAI()

            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.chat_log,
                temperature=0.3,
            )

            reply = response.choices[0].message.content

            st.session_state.chat_log.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

# 채팅 로그 크기 제한
MAX_CHAT_LOG_LENGTH = 50
if len(st.session_state.chat_log) > MAX_CHAT_LOG_LENGTH:
    st.session_state.chat_log = st.session_state.chat_log[-MAX_CHAT_LOG_LENGTH:]

# 채팅 내용 표시
for msg in st.session_state.chat_log:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

