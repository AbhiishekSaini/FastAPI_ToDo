from fastapi import FastAPI
import uvicorn
from database import engine
from models import Base
from crud import router as crud_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


Base.metadata.create_all(bind=engine)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['http://localhost:3000/'],
#     allow_credentials = True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

app.include_router(crud_router,prefix='/todo',tags=["Crud Router"])

@app.get('/')
def home(title: str,description: str,done:bool):
    return { "message":f"{title}-{description} -{done}"}

# if __name__ =="__main__":
#     uvicorn.run(app, host = "127.0.0.1",port=8000)