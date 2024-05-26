from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import routers.authRouter as authRouter 


app = FastAPI()
app.include_router(authRouter.router)

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