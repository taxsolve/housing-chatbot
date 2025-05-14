import streamlit as st
import openai

# Assistant ID
ASSISTANT_ID = "asst_NypvU80xC5V0LYEa6c3cyHa4"

# OpenAI API 키
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 세션 상태 초기화
if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id
    st.session_state.chat_log = []

st.set_page_config(page_title="주택임대소득 AI 세무사", layout="wide")
st.title("🏠 주택임대소득 AI 세무사")
st.markdown("국세청 문서 기반으로 작동하는 AI 세무사 챗봇입니다. 정확하고 신뢰할 수 있는 답변을 제공합니다.")

# 사용자 질문 입력
user_input = st.chat_input("질문을 입력하세요...")

# 대화 출력
for msg in st.session_state.chat_log:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 질문 처리
if user_input:
    st.session_state.chat_log.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 사용자 메시지를 쓰레드에 추가
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input
    )

    with st.chat_message("assistant"):
        with st.spinner("답변 생성 중..."):
            run = client.beta.threads.runs.create(
                thread_id=st.session_state.thread_id,
                assistant_id=ASSISTANT_ID,
            )

            # Run 완료까지 대기
            while run.status != "completed":
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id,
                )

            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )

            answer = messages.data[0].content[0].text.value
            st.markdown(answer)
            st.session_state.chat_log.append({"role": "assistant", "content": answer})

