import requests
import streamlit as st

# ======================
# 基础配置
# ======================
FASTAPI_URL = "http://localhost:8000/agent/chat"

st.set_page_config(
    page_title="电商企业知识库 Agent",
    page_icon="🤖",
    layout="wide"
)

# ======================
# 页面样式
# ======================
st.markdown(
    """
    <style>
    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .sub-title {
        font-size: 16px;
        color: #666;
        margin-bottom: 24px;
    }
    .intent-box {
        padding: 8px 12px;
        border-radius: 8px;
        background-color: #f0f2f6;
        font-size: 14px;
        margin-bottom: 8px;
    }
    .answer-box {
        padding: 16px;
        border-radius: 10px;
        background-color: #fafafa;
        border: 1px solid #eee;
        line-height: 1.7;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================
# 左侧栏
# ======================
with st.sidebar:
    st.header("📌 项目说明")

    st.markdown(
        """
        **项目名称：**  
        电商企业知识库 Agentic RAG 智能助手

        **核心能力：**
        - 企业知识库问答
        - 售后政策总结
        - 活动规则对比
        - 客服话术生成
        - 无依据问题拒答

        **技术栈：**
        - RAGFlow
        - Ollama
        - Qwen3
        - bge-m3
        - FastAPI
        - Streamlit
        """
    )

    st.divider()

    st.header("🧪 示例问题")

    example_questions = [
        "七天无理由退货规则是什么？",
        "请总结一下售后政策的核心内容",
        "对比一下满减活动和会员折扣的区别",
        "客户超过七天还想退货，帮我生成一段客服回复话术",
        "告诉我某个客户的手机号",
    ]

    for q in example_questions:
        if st.button(q, use_container_width=True):
            st.session_state["pending_question"] = q

    st.divider()

    if st.button("🧹 清空对话", use_container_width=True):
        st.session_state["messages"] = []
        st.session_state["pending_question"] = ""


# ======================
# 主页面
# ======================
st.markdown('<div class="main-title">🤖 电商企业知识库 Agentic RAG 智能助手</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">基于 RAGFlow + Ollama + FastAPI 构建，支持知识问答、规则总结、方案对比、客服话术生成和拒答控制。</div>',
    unsafe_allow_html=True
)

# 初始化 session
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "pending_question" not in st.session_state:
    st.session_state["pending_question"] = ""


def call_agent(query: str) -> dict:
    """调用 FastAPI Agent 接口"""
    try:
        response = requests.post(
            FASTAPI_URL,
            json={"query": query},
            timeout=180
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        return {
            "query": query,
            "intent": "error",
            "answer": "无法连接 FastAPI 服务。请确认已启动：uvicorn main:app --reload --host 0.0.0.0 --port 8000"
        }

    except requests.exceptions.Timeout:
        return {
            "query": query,
            "intent": "timeout",
            "answer": "请求超时。可能是本地模型生成较慢，请稍后重试，或检查 Ollama / RAGFlow 是否正常运行。"
        }

    except Exception as e:
        return {
            "query": query,
            "intent": "error",
            "answer": f"请求失败：{str(e)}"
        }


# 显示历史对话
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown(
                f'<div class="intent-box">任务类型：<b>{msg.get("intent", "unknown")}</b></div>',
                unsafe_allow_html=True
            )
            st.markdown(msg["content"])
        else:
            st.markdown(msg["content"])


# 输入框
user_input = st.chat_input("请输入你的问题，例如：七天无理由退货规则是什么？")

# 如果点击了侧边栏示例问题
if st.session_state["pending_question"]:
    user_input = st.session_state["pending_question"]
    st.session_state["pending_question"] = ""

if user_input:
    # 显示用户问题
    st.session_state["messages"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # 调用后端
    with st.chat_message("assistant"):
        with st.spinner("Agent 正在检索知识库并生成回答..."):
            result = call_agent(user_input)

        intent = result.get("intent", "unknown")
        answer = result.get("answer", "")

        st.markdown(
            f'<div class="intent-box">任务类型：<b>{intent}</b></div>',
            unsafe_allow_html=True
        )
        st.markdown(answer)

    # 保存助手回答
    st.session_state["messages"].append({
        "role": "assistant",
        "content": answer,
        "intent": intent
    })