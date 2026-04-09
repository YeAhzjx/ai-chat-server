#导入fastapi框架
from fastapi import Body, FastAPI
#解决跨域引入cors中间件
from fastapi.middleware.cors import CORSMiddleware
#导入openai客户端
from openai import OpenAI
# 导入os模块读取环境变量
import os
from dotenv import load_dotenv
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

#配置apikey
client=OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

#聊天接口
@app.post("/chat")
def chat(history:list=Body(...)):
    try:
        #调用大模型
        response=client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=history,
            temperature=0.7,
            top_p=0.9,
            max_tokens=2000,
        )
        #返回回答
        reply=response.choices[0].message.content
        return {"reply":reply}
    except Exception as e:
        print(f"❌ 调用AI失败: {e}")
        return {"reply": "服务异常，请稍后重试"}
#运行main.py就运行服务
if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)