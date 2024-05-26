from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import routers.authRouter as authRouter 
import routers.vectorDbRouter as vectorDbRouter

app = FastAPI()
app.include_router(authRouter.router)
app.include_router(vectorDbRouter.router)
# origins = [
#     "http://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )