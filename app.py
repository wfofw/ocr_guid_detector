import json
from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from guid_detector.extractor import find_guids_by_stripes
from PIL import Image, UnidentifiedImageError

app = FastAPI(title="GUID Detector API", version="1.0.0")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "guid-detector"}


@app.post("/recognize")
def recognize_guid(file: Annotated[UploadFile, File()]):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="The file must be an image"
        )

    try:
        image = Image.open(file.file)
        image.load()
    except (UnidentifiedImageError, ValueError, OSError):
        raise HTTPException(
            status_code=400, detail="Incorrect or corrupted image file"
        )

    def event_generator():
            for event in find_guids_by_stripes(image):
                # We transmit chunks in Server-Sent Events (SSE) format.
                yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")