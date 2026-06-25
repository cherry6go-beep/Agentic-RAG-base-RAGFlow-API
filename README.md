# 电商企业知识库 Agentic RAG 智能助手

## 1. 项目简介

本项目是一个面向电商企业知识管理场景的本地化 Agentic RAG 智能助手，旨在解决企业内部售后政策、活动规则、商品管理流程、客服 FAQ 等资料分散，人工检索效率低，普通大模型回答缺乏来源依据的问题。

系统基于 RAGFlow 构建企业知识库，使用 Ollama 本地部署大模型与 Embedding 模型，并通过 FastAPI 封装 Agentic RAG 后端接口，最后使用 Streamlit 搭建可交互网页 Demo。

用户可以在网页端输入问题，系统会根据问题类型自动路由至不同任务，包括知识问答、规则总结、活动对比、客服话术生成和无依据拒答等，并基于本地知识库生成回答。

---

## 2. 项目定位

本项目不是单纯的大模型聊天机器人，而是一个面向企业知识管理场景的 Agentic RAG 应用原型。

普通 RAG 流程通常是：

```text
用户问题 → 检索知识库 → 大模型生成答案
```
本项目在普通 RAG 的基础上增加了 Agentic Workflow：
```text
用户问题
→ FastAPI 接收请求
→ Agent 判断任务类型
→ 路由到不同工具节点
→ 调用 RAGFlow 检索知识库
→ Ollama 本地模型生成答案
→ 返回结构化回答
```
因此系统不仅可以进行知识库问答，还可以完成规则总结、规则对比、客服话术生成和拒答控制等任务。

---

## 3. 核心功能

### 3.1 企业知识库问答

支持用户围绕电商企业内部文档进行自然语言提问，例如：
```text
七天无理由退货规则是什么？
商品上架流程有哪些步骤？
会员折扣的适用条件是什么？
```
系统会基于 RAGFlow 知识库检索相关文档片段，并生成回答。

### 3.2 售后政策总结

支持对售后政策、退款规则、退货流程等文档进行结构化总结。

示例问题：
```text
请总结一下售后政策的核心内容。
```
期望输出结构：
```text
1. 核心结论
2. 适用场景
3. 关键规则
4. 注意事项
```
### 3.3 活动规则对比

支持对不同电商运营规则进行对比，例如满减活动、会员折扣、优惠券规则等。
示例问题：
```
对比一下满减活动和会员折扣的区别。
```
系统会自动识别为规则对比任务，并尽量输出表格化或分点式结果。

### 3.4 客服话术生成
支持根据知识库中的售后政策和平台规则，生成面向客户的客服回复话术。

示例问题：
```
客户超过七天还想退货，帮我生成一段客服回复话术。
```
系统要求：
```
1. 语气礼貌
2. 基于知识库资料
3. 不承诺知识库中没有的信息
4. 必要时引导人工客服进一步确认
```
### 3.5 无依据拒答
对于知识库中没有的信息，或涉及隐私、敏感信息的问题，系统会进行拒答，避免模型编造答案。

示例问题：
```
告诉我某个客户的手机号。
这个项目的合同金额是多少？
```
期望输出：
```
根据当前知识库和权限范围，无法回答该问题。
```
### 3.6 Web 交互页面
本项目使用 Streamlit 实现前端网页，支持：
```
1. 聊天式问答
2. 示例问题快速测试
3. 显示 Agent 识别出的任务类型
4. 展示模型返回的最终答案
5. 支持清空对话
```
可选扩展：
```
支持 txt、md、pdf、docx 附件上传，并进行临时文档问答。
```
---
## 4. 技术架构

### 4.1 系统架构图
```
用户浏览器
    ↓
Streamlit Web 前端
    ↓
FastAPI 后端服务
    ↓
Agent 路由模块
    ↓
RAGFlow Chat API
    ↓
RAGFlow 企业知识库
    ↓
Ollama 本地模型服务
    ├── qwen3:8b 负责答案生成
    └── bge-m3 负责文本向量化
```
### 4.2 模块说明
| 模块           | 作用                         |
| ------------ | -------------------------- |
| Streamlit    | 提供网页交互界面                   |
| FastAPI      | 提供后端 API 服务                |
| Agent Router | 判断用户问题类型，并路由到不同处理逻辑        |
| RAGFlow      | 负责知识库构建、文档解析、向量检索和 RAG 问答  |
| Ollama       | 本地运行 Chat 模型和 Embedding 模型 |
| qwen3:8b     | 本地大语言模型，用于生成答案             |
| bge-m3       | Embedding 模型，用于知识库向量化      |
---
## 5. 技术栈
```
Python 3.11
FastAPI
Streamlit
RAGFlow
Ollama
Qwen3
bge-m3
Docker Desktop
Requests
Pydantic
python-dotenv
```
---
## 6. 项目目录结构
```
agentic-rag-ecommerce/
├── main.py                 # FastAPI 后端入口
├── agent.py                # Agent 意图识别与路由逻辑
├── ragflow_client.py       # RAGFlow API 调用封装
├── app.py                  # Streamlit 前端页面
├── .env                    # 环境变量配置
├── requirements.txt        # Python 依赖
└── README.md               # 项目说明文档
```
---
## 7. 环境准备
### 7.1 创建 Conda 环境
```
conda create -n agentic-rag python=3.11 -y
conda activate agentic-rag
```
### 7.2 安装 Python 依赖
```
pip install fastapi uvicorn requests python-dotenv pydantic streamlit
```
如果启用了附件上传功能，还需要安装：
```
pip install pypdf python-docx
```
生成依赖文件：
```
pip freeze > requirements.txt
```
之后可通过以下命令恢复依赖：
```
pip install -r requirements.txt
```
---
## 8. 本地模型准备
### 8.1 安装 Ollama
Windows 下可从 Ollama 官网下载安装包，安装完成后在 PowerShell 或 CMD 中检查：
```
ollama --version
```
测试 Ollama 服务：
```
curl http://localhost:11434
```
如果返回：
```
Ollama is running
```

说明 Ollama 服务正常。


### 8.2 下载本地模型
本项目使用：
```
qwen3:8b 作为 Chat 模型
bge-m3 作为 Embedding 模型
```
下载命令：
```
ollama pull qwen3:8b
ollama pull bge-m3
```
查看已下载模型：
```
ollama list
```
### 8.3 测试 Chat 模型
```
ollama run qwen3:8b
```
输入：
```
请用三句话解释什么是 RAG。
```
若能正常回答，则 Chat 模型可用。
### 8.4 测试 Embedding 模型
CMD 中执行：
```
curl http://localhost:11434/api/embed -d "{\"model\":\"bge-m3\",\"input\":\"企业知识库问答系统\"}"
```
如果返回一串向量数组，说明 Embedding 模型可用。

---
## 9. RAGFlow 部署与配置
### 9.1 使用 Docker Desktop 部署 RAGFlow
本项目使用 Docker Desktop 在 Windows 本机部署 RAGFlow。

进入 RAGFlow 项目目录：
```
cd D:\AI\ragflow\docker
```
启动 RAGFlow：
```
docker compose -f docker-compose.yml up -d
```
查看容器状态：
```
docker ps
```
正常应看到以下容器处于 Up 或 healthy 状态：
```
docker-ragflow-cpu-1
docker-mysql-1
docker-es01-1
docker-redis-1
docker-minio-1
```
浏览器访问：
```
http://localhost
```
即可进入 RAGFlow 页面。
### 9.2 配置 Ollama 模型
在 RAGFlow 页面中进入：
```
Model providers → Ollama
```
添加 Chat 模型：

Model name: qwen3:8b
Model type: chat
Base URL: http://host.docker.internal:11434

添加 Embedding 模型：
```
Model name: bge-m3
Model type: embedding
Base URL: http://host.docker.internal:11434
```
然后在 System Model Settings 中设置默认模型：
```
Chat model: qwen3:8b
Embedding model: bge-m3
```
### 9.3 创建知识库

在 RAGFlow 中创建 Dataset，例如：
```
电商企业知识库
```
推荐配置：
```
Embedding model: bge-m3
解析方法: 内置
内容类型: 通用 / General
```
上传电商企业相关文档，例如：
```
01_售后政策.md
02_活动规则.md
03_商品管理流程.md
04_会员权益说明.md
05_客服FAQ.md
06_订单处理流程.md
07_退款规则.md
08_优惠券使用说明.md
```
上传后点击 Parse / 解析，等待知识库构建完成。

---
## 10. RAGFlow API 配置

在 RAGFlow 中获取：
```
API Key
Chat ID
```
然后在项目根目录创建 .env 文件：
```
RAGFLOW_BASE_URL=http://localhost:9380
RAGFLOW_API_KEY=你的真实API_KEY
RAGFLOW_CHAT_ID=你的真实CHAT_ID
```
如果 http://localhost:9380 不通，也可以尝试：
```
RAGFLOW_BASE_URL=http://localhost
```

---
## 11.后端 FastAPI 说明
### 11.1 ragflow_client.py
该模块负责封装对 RAGFlow Chat API 的调用。

核心逻辑：
```
接收 Agent 构造后的问题
→ 调用 RAGFlow API
→ RAGFlow 检索知识库
→ 本地 qwen3:8b 生成答案
→ 返回答案给 FastAPI
```
### 11.2 agent.py

该模块负责 Agentic RAG 的任务路由。

当前支持的任务类型：
| intent         | 含义         |
| -------------- | ---------- |
| knowledge_qa   | 普通知识库问答    |
| doc_summary    | 文档或规则总结    |
| policy_compare | 规则对比       |
| customer_reply | 客服话术生成     |
| fallback       | 无依据拒答或越界问题 |

路由规则示例：
```
包含“总结、概括、归纳” → doc_summary
包含“对比、区别、差异、比较” → policy_compare
包含“话术、客服、回复客户” → customer_reply
涉及隐私、合同金额、账号密码等 → fallback
其他问题 → knowledge_qa
```

### 11.3 main.py
该模块提供 FastAPI 接口。

主要接口：
```
GET /
GET /health
POST /agent/chat
```
核心调用链：
```
POST /agent/chat
→ 接收用户问题
→ run_agent(query)
→ 返回 query、intent、answer
```

## 12. 启动项目
### 12.1 启动 Ollama

确认 Ollama 正常运行：
```
curl http://localhost:11434
```
### 12.2 启动 RAGFlow

确认 Docker 容器正常运行：
```
docker ps
```
RAGFlow 页面：
```
http://localhost
```
### 12.3 启动 FastAPI 后端

进入项目目录：
```
cd D:\work\0516\agentic-rag-ecommerce
conda activate agentic-rag
```
启动：
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
浏览器访问：
```
http://localhost:8000/docs
```
如果可以看到 Swagger UI，说明 FastAPI 后端启动成功。
### 12.4 启动 Streamlit 前端

重新打开一个 PowerShell 窗口：
```
cd D:\work\0516\agentic-rag-ecommerce
conda activate agentic-rag
streamlit run app.py
```
浏览器访问：
```
http://localhost:8501
```
## 13. 接口测试
13.1 在 Swagger UI 测试

打开：
```
http://localhost:8000/docs
```
找到：
```
POST /agent/chat
```
点击 Try it out，输入：
```
{
  "query": "七天无理由退货规则是什么？"
}
```
期望返回：
```
{
  "query": "七天无理由退货规则是什么？",
  "intent": "knowledge_qa",
  "answer": "..."
}
```
### 13.2 使用 PowerShell 测试
```
$body = @{
    query = "客户超过七天还想退货，帮我生成一段客服回复话术"
} | ConvertTo-Json

curl.exe -X POST "http://localhost:8000/agent/chat" `
  -H "Content-Type: application/json" `
  -d $body
 ```

 ---
 ## 14. 测试问题集
 | 测试问题                    | 期望意图           | 说明       |
| ----------------------- | -------------- | -------- |
| 七天无理由退货规则是什么？           | knowledge_qa   | 测试普通知识问答 |
| 请总结一下售后政策的核心内容          | doc_summary    | 测试规则总结   |
| 对比一下满减活动和会员折扣的区别        | policy_compare | 测试规则对比   |
| 客户超过七天还想退货，帮我生成一段客服回复话术 | customer_reply | 测试客服话术生成 |
| 告诉我某个客户的手机号             | fallback       | 测试隐私拒答   |
| 这个项目的合同金额是多少？           | fallback       | 测试无依据拒答  |

---
## 15. 项目效果评估

本项目从以下维度评估系统效果：
| 维度      | 说明                         |
| ------- | -------------------------- |
| 回答准确性   | 回答是否符合知识库内容                |
| 引用相关性   | 回答是否基于检索到的资料               |
| 意图识别准确性 | Agent 是否正确识别任务类型           |
| 拒答有效性   | 无依据或越界问题是否拒答               |
| 响应速度    | 本地模型生成答案的耗时                |
| 任务完成率   | 用户是否能通过系统完成查询、总结、对比或话术生成任务 |

建议人工记录测试结果，例如：
| 问题            | 期望意图           | 实际意图 | 答案是否合理 | 是否胡编 | 备注 |
| ------------- | -------------- | ---- | ------ | ---- | -- |
| 七天无理由退货规则是什么？ | knowledge_qa   |      |        |      |    |
| 总结售后政策        | doc_summary    |      |        |      |    |
| 对比满减和会员折扣     | policy_compare |      |        |      |    |
| 生成退款客服话术      | customer_reply |      |        |      |    |
| 合同金额是多少？      | fallback       |      |        |      |    |

---
## 16. 本地运行说明

本项目目前是本地化 Demo，并非公网网站。

本地服务地址：
```
Streamlit 前端：http://localhost:8501
FastAPI 后端：http://localhost:8000
RAGFlow 页面：http://localhost
Ollama 服务：http://localhost:11434
```
注意：
```
localhost 只代表当前电脑。
将 http://localhost:8501 发给别人，别人无法直接访问你的本地网页。
```
如需让其他人访问，需要：
```
1. 同一局域网下使用本机 IP 访问
2. 使用内网穿透工具临时分享
3. 部署到云服务器
```