import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from dotenv import load_dotenv
import os

load_dotenv()

class PinataStore:
    def __init__(self, api_key):
        self.JWT = api_key
        
    def pin_file_to_ipfs(self, file, filename):
        # Prepare the multipart form data
        encoder = MultipartEncoder(
            fields={
                'file': (filename, file, 'application/octet-stream'),
                'pinataMetadata': json.dumps({
                    'name': filename
                }),
                'pinataOptions': json.dumps({
                    'cidVersion': 0
                })
            }
        )
        
        # Headers
        headers = {
            'Content-Type': encoder.content_type,
            'Authorization': f'Bearer {self.JWT}'
        }

        # POST request
        try:
            response = requests.post(
                'https://api.pinata.cloud/pinning/pinFileToIPFS',
                headers=headers,
                data=encoder
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_file_info_from_pinata(self, cid):
        # Endpoint URL for retrieving file information
        url = f"https://api.pinata.cloud/data/pinList?hashContains={cid}"
        
        # Headers
        headers = {
            'Authorization': f'Bearer {self.JWT}'
        }

        # GET request
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to retrieve file information: {response.status_code} - {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def read_file_from_pinata(self, cid):
        # Endpoint URL for retrieving the file from IPFS via Pinata gateway
        
        url = f"https://gateway.pinata.cloud/ipfs/{cid}"
        
        # GET request
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Extract content type and size
                content_type = response.headers.get('Content-Type', 'unknown')
                content_length = response.headers.get('Content-Length', 'unknown')
                
                # Return the file content and metadata
                return {
                    "data": response.content.decode('utf-8', errors='replace'),  # Decode content with error handling
                    "metadata": {
                        "content_type": content_type,
                        "content_length": content_length
                    }
                }
            else:
                return {"error": f"Failed to retrieve the file: {response.status_code} - {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"An error occurred: {e}"}
            
    def delete_file_from_pinata(self, cid):
        # Endpoint URL for unpinning the file from IPFS via Pinata
        url = f"https://api.pinata.cloud/pinning/unpin/{cid}"
        
        # Headers
        headers = {
            'Authorization': f'Bearer {self.JWT}'
        }

        # DELETE request
        try:
            response = requests.delete(url, headers=headers)
            if response.status_code == 200:
                return {"message": f"Successfully deleted the file with CID: {cid}"}
            else:
                return {"error": f"Failed to delete the file: {response.status_code} - {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def list_current_pins_from_pinata(self):
        # Endpoint URL for listing all pins with a status filter
        url = "https://api.pinata.cloud/data/pinList?status=pinned"

        # Headers
        headers = {
            'Authorization': f'Bearer {self.JWT}'
        }

        # GET request
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to retrieve pins: {response.status_code} - {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
