from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import os
import requests
from App.utils.PDFAgent import MultiPDFDocAgent

router = APIRouter(tags=['Agent'])

# Initialize the agent (you might want to set this up differently in production)
agent = None

@router.on_event("startup")
async def startup_event():
    global agent
    agent = MultiPDFDocAgent()  # Initialize with default or custom settings

class ChatRequest(BaseModel):
    query: str

@router.post("/upload-pdf/")
async def upload_pdf(cid: str):
    global agent
    try:
        # Fetch the PDF file from the Pinata gateway
        url = f"https://gateway.pinata.cloud/ipfs/{cid}"
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Failed to fetch the PDF file")

        # Save the PDF file locally
        os.makedirs('Documents', exist_ok=True)
        pdf_path = "Documents/temp.pdf"
        with open(pdf_path, "wb") as f:
            f.write(response.content)

        # Load and process the PDF
        agent.filePath = pdf_path
        texts, metadatas = agent.load_pdf_locally()
        chain = agent.textChunk_to_docObj(texts, metadatas)

        return {"message": "PDF uploaded and processed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/")
async def chat(request: ChatRequest):
    global agent
    try:
        response = agent.chat(agent.chain, request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/")
async def status():
    return {"status": "Running", "agent": str(agent)}
