# Project Name

## Overview

This project provides a FastAPI application that interacts with IPFS via Pinata. It allows users to upload files, which are then pinned to IPFS. The application uses various tools and libraries for processing, storing, and managing files and embeddings.

## Table of Contents

1. [Setup](#setup)
2. [Running the Project](#running-the-project)
3. [API Endpoints](#api-endpoints)
4. [Purpose of Pinata](#purpose-of-pinata)
5. [Additional Notes](#additional-notes)

## Setup

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-repo/project-name.git
    cd project-name
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set Up Environment Variables**

    Create a `.env` file in the root directory and add your environment variables. Example:

    ```env
    PINATA_API_KEY=your_pinata_api_key
    ```

## Running the Project

1. **Start the FastAPI Server**

    ```bash
    uvicorn App.main:app --reload
    ```

    The server will start at `http://127.0.0.1:8000`.

2. **Access API Documentation**

    Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the automatically generated Swagger UI documentation.

## API Endpoints

### 1. `/pin-file`

- **Method**: `POST`
- **Description**: Uploads a file and pins it to IPFS using Pinata.
- **Request Body**: Multipart form-data with file.
- **Parameters**:
    - `file` (required): The file to be uploaded and pinned.
- **Responses**:
    - `201 Created`: File successfully pinned to IPFS.
    - `500 Internal Server Error`: An error occurred.

**Example Request:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pin-file' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@path/to/your/file.pdf;type=application/pdf'
```

**Example Response:**

```json
{
  "IpfsHash": "QmExampleHash",
  "PinSize": 12345,
  "Timestamp": "2024-08-27T12:34:56Z"
}
```

## Purpose of Pinata

Pinata is a service that provides reliable and scalable IPFS pinning. It allows you to store and manage files on IPFS without having to run your own IPFS nodes. By using Pinata, you ensure that your files are permanently stored on IPFS and can be retrieved reliably.

**Key Benefits:**

- **Scalability**: Handle large volumes of files without managing infrastructure.
- **Reliability**: Ensure your files remain accessible and pinned to IPFS.
- **Ease of Use**: Simplify interaction with IPFS through a user-friendly API.

## Additional Notes

- **Error Handling**: The API returns a detailed error message in case of issues during file upload or pinning.
- **Testing**: Ensure that your environment variables are set correctly and that you have network access to the Pinata API.