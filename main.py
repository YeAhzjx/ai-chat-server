#导入fastapi框架 test
from fastapi import Body, FastAPI
# 导入流式响应+异步生成器类型注解
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
#解决跨域引入cors中间件
from fastapi.middleware.cors import CORSMiddleware
#导入openai客户端
from openai import OpenAI
# 导入异步模块
import asyncio
# 导入os模块读取环境变量
import os
from dotenv import load_dotenv
# langchain核心
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
# 加载.env文件
load_dotenv()
#创建fastapi应用
app=FastAPI()

#配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("FRONTEND_ORIGIN"),
    allow_credentials=True,
    allow_methods=["POST","GET"],
    allow_headers=["Content-Type"],
)

#测试接口
@app.get("/")
def root():
    return {"message":"后端服务启动成功！"}

# #配置apikey
# client=OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     base_url=os.getenv("OPENAI_BASE_URL")
# )

#聊天接口
@app.post("/chat/stream")
async def chat_stream(history: list = Body(...)):
    """流式返回AI回复，遵循SSE标准格式"""
    # 异步生成器：逐块返回流式数据
    async def generate_stream() -> AsyncGenerator[str, None]:
        try:
            # 初始化langchain模型
            llm = ChatOpenAI(
                model="deepseek-ai/DeepSeek-V3",
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL"),
                temperature=0.7,
                top_p=0.9,
                max_tokens=2000,
                stream=True,  # 开启流式
            )
            # 把历史消息转成 LangChain 格式
            langchain_messages=[]
            for msg in history:
                if msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    langchain_messages.append(AIMessage(content=msg["content"]))
            # LangChain流式输出
            async for chunk in llm.astream(langchain_messages):
                if chunk.content:
                    yield f"data: {chunk.content}\n\n"
                    await asyncio.sleep(0.01)
            
            # 流式结束标记（前端可识别）
            yield "data: [DONE]\n\n"
        
        except Exception as e:
            # 错误信息按SSE格式返回
            yield f"data: [ERROR] {e}\n\n"
    
    # 返回流式响应，指定SSE标准MIME类型
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream"
    )
#运行main.py就运行服务
if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)