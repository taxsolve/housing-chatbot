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
st.markdown("**국세청 문서 기반으로 작동하는 GPT-4 챗봇입니다.**\n\n답변은 모두 실무 기준에 따릅니다.")

# 사용자 질문 입력
user_input = st.chat_input("질문을 입력하세요...")

# 이전 대화 표시
for msg in st.session_state.chat_log:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 질문 처리
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
                instructions="""
                당신은 대한민국의 주택임대소득 세법에 정통한 AI 세무사입니다.
                사용자 질문에 대해 반드시 업로드된 국세청 문서의 내용만을 근거로 답변하세요.
                문서에 없는 정보는 "답변드릴 수 없습니다"라고 명확히 안내하세요.
                모든 설명은 다음 형식을 따르세요:
                - 용어 정의:
                - 실제 사례:
                - 주의사항:

                절세 팁이나 신고 요건은 문서 근거가 있을 경우에만 안내하며, 일반적인 조언은 하지 마세요.
                """
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


