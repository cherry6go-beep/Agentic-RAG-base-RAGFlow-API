# agent.py
from ragflow_client import ask_ragflow


def classify_intent(query: str) -> str:
    if any(word in query for word in ["总结", "概括", "归纳"]):
        return "doc_summary"

    if any(word in query for word in ["对比", "区别", "差异", "相比"]):
        return "policy_compare"

    if any(word in query for word in ["话术", "回复客户", "客服", "安抚"]):
        return "customer_reply"

    if any(word in query for word in ["合同金额", "员工工资", "隐私", "账号密码"]):
        return "fallback"

    return "knowledge_qa"


def run_agent(query: str) -> dict:
    intent = classify_intent(query)

    if intent == "knowledge_qa":
        prompt = f"""
你是电商企业知识库助手。请基于知识库资料回答用户问题。
如果知识库没有依据，请明确说明无法确定。

用户问题：{query}
"""
        answer = ask_ragflow(prompt)

    elif intent == "doc_summary":
        prompt = f"""
请基于知识库资料，对用户提到的规则或文档进行结构化总结。
输出格式：
1. 核心结论
2. 适用场景
3. 关键规则
4. 注意事项

用户问题：{query}
"""
        answer = ask_ragflow(prompt)

    elif intent == "policy_compare":
        prompt = f"""
请基于知识库资料，对用户提到的两个或多个规则进行对比。
输出为表格形式，包含：规则名称、适用条件、限制条件、适合场景、引用依据。
如果知识库信息不足，请明确说明。

用户问题：{query}
"""
        answer = ask_ragflow(prompt)

    elif intent == "customer_reply":
        prompt = f"""
请基于知识库资料，生成一段面向客户的电商客服回复话术。
要求：
1. 语气礼貌
2. 不承诺知识库没有的信息
3. 说明处理依据
4. 如果资料不足，提示需要人工客服进一步确认

用户问题：{query}
"""
        answer = ask_ragflow(prompt)

    else:
        answer = "根据当前知识库和权限范围，无法回答该问题。请补充相关资料或联系人工管理员确认。"

    return {
        "intent": intent,
        "answer": answer
    }