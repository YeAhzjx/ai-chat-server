#导入fastapi框架
from fastapi import FastAPI
#解决跨域引入cors中间件
from fastapi.middleware.cors import CORSMiddleware
#导入openai客户端
from openai import OpenAI

#创建fastapi应用
app=FastAPI()

#配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#测试接口
@app.get("/")
def root():
    return {"message":"后端服务启动成功！"}

#配置apikey
client=OpenAI(
    api_key="sk-gemgkzxqafjlrubkgifzltzwzgmfrwshqtzvrgdpbjxhbquv",
    base_url="https://api.siliconflow.cn/v1"
)

#聊天接口
@app.post("/chat")
def chat(message:str):
    #调用大模型
    response=client.chat.completions.create(
        model="Qwen/Qwen2-7B-Instruct",
        messages=[{"role":"user","content":message}]
    )
    #返回回答
    reply=response.choices[0].message.content
    return {"reply":reply}

#运行main.py就运行服务
if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)