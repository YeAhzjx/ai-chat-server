#导入fastapi框架
from fastapi import FastAPI

#解决跨域引入cors中间件
from fastapi.middleware.cors import CORSMiddleware

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

#接口
@app.get("/")
def root():
    return {"message":"后端服务启动成功！"}


#运行main.py就运行服务
if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)