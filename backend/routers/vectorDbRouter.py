from typing import Annotated
from fastapi import Depends, HTTPException, status, Request, UploadFile, File
from config.auth import *
from schema.token import Token
from models.user import User
from fastapi import APIRouter
import json
import sys
import os

from .authRouter import get_current_user
from rag_functions.vector_db import VectorDBFactory
from rag_functions.document_loader.pdf_loader import PDFLoader
import aiofiles

router = APIRouter()

config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backend', 'rag_functions', 'config', 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)


vector_db = VectorDBFactory.create_vector_db(config)


@router.post("/query_embeddings/")
def query_embeddings(request: Request, query: str, user: User = Depends(get_current_user)):
    query_result = vector_db.query_db(query, "pdfs", user_owner=user.username)
    return {"query": query, "result": query_result}



#todo: Add hashing to prevent duplicate uploads

@router.post("/store_embeddings/")
async def store_embeddings(request: Request, file: UploadFile = File(...), user: User = Depends(get_current_user)):
    loader = PDFLoader()

    # Read the file
    contents = await file.read()

    # Save the file to the upload folder
    file_location = f"upload/{file.filename}"
    async with aiofiles.open(file_location, 'wb') as out_file:
        await out_file.write(contents)

    # You might need to modify load_docs to accept file contents instead of a path
    documents = loader.load_docs(file_location, user_owner=user.username)

    vector_db.store_embeddings(documents, collection_name="pdfs")

    # Delete the file
    os.remove(file_location)

    return {"message": "Stored embeddings successfully."}