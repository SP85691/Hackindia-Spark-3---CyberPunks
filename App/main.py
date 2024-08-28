from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from App.routes.FileManagement import router as file_management_router
from App.routes.agent import router as agent_router

app = FastAPI(title="PDF Agent API", description="API for interacting with the PDF Agent", version="0.1")
app.include_router(file_management_router)
app.include_router(agent_router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}