from fastapi import APIRouter, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from App.utils.pinata import PinataStore
import os
import io
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=['File Management'])

# Initialize PinataStore with API key
pinata_store = PinataStore(api_key=os.getenv('JWT'))

@router.post("/pin-file")
async def pin_file(file: UploadFile):
    try:
        # Read the file content
        file_content = await file.read()
        print(f"File Content: {file_content}")

        # Create a BytesIO object from file content to pass to Pinata
        file_like_object = io.BytesIO(file_content)
        
        # Pin the file content to IPFS using Pinata
        result = pinata_store.pin_file_to_ipfs(file_like_object, file.filename)
        
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["error"])
        
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/get-file-info")
async def get_file_info(cid: str):
    try:
        info = pinata_store.get_file_info_from_pinata(cid)
        
        if "error" in info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=info["error"])
        
        return JSONResponse(content=info, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/read-file")
async def read_file(cid: str):
    try:
        result = pinata_store.read_file_from_pinata(cid)
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])
        
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/delete-file")
async def delete_file(cid: str):
    try:
        result = pinata_store.delete_file_from_pinata(cid)
        
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["error"])
        
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/list-pins")
async def list_pins():
    try:
        pins = pinata_store.list_current_pins_from_pinata()
        
        if "error" in pins:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=pins["error"])
        
        return JSONResponse(content={"pins": pins}, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
