<p align="center">
  <a href="https://www.python.org/downloads/release/python-3104/"><img src="https://img.shields.io/badge/python-3.10.4-3776AB?logo=python&logoColor=white" alt="Python 3.10.4"></a>
  <a href="https://www.docker.com/products/docker-desktop/"><img src="https://img.shields.io/badge/Docker-29.7.2-2496ED?logo=docker&logoColor=white" alt="Docker 29.7.2"></a>
</p>

## 👁 ocr_guid_detector

ocr_guid_detector is an automatic detector based on optical character recognition Tesseract-OCR.

It works with screenshots, photos (in the future with PDF, Word, etc.), recognizes GUIDs (Globally Unique Identifiers) and displays them as text on the screen.

## 🌟 Highlights

- Designed for automated processing of large image collections
- Advanced image preprocessing (slicing, scaling, thresholding, and color inversion)
- FastAPI-backed REST API with streaming real-time status updates

## ℹ️ Overview

The goal is to reliably recognize GUIDs regardless of their position, font, or size.

Tesseract-OCR was used as a basis, but out-of-the-box:

- its success rate was ~20-30% (of characters)
- it didn't collect complete words
- it produced a lot of garbage

Therefore, a multi-pass pipeline was implemented:

- a slicing and layering method
- dynamic detection configurations (thresholds, scale factors, color inversion)
- hamming distance metric filtering to remove corrupted GUID parts

## ⚙️ Installation & Setup

Clone repository:

```bash
git clone https://github.com/wfofw/ocr_guid_detector.git
cd ocr_guid_detector
```

Build a Docker image and create container

```bash
docker build -t guid_detector .
docker run -d -p 5000:5000 --name cont_guid_detector guid_detector
```

Swagger UI documentation will be instantly available at http://localhost:5000/docs

## 🛠 API Usage & Quick Test

The API accepts image uploads and streams real-time processing statistics during execution.

Use one of the following commands to test the API.

### Linux / macOS

```bash
curl -N -X POST "http://localhost:5000/recognize" -F "file=@./sample_screenshot.jpeg"
```

### Windows (PowerShell)

```PowerShell
curl.exe -N -X POST "http://localhost:5000/recognize" -F "file=@${PWD}\sample_screenshot_2.jpeg"
```

### Example Response

```JSON
{
"type": "result",
"count": 6,
"guids": ["e4d909c2-984e-4e42-8958-8686d655f463", "f2a11b88-11f0-4a3b-9c12-3456789abcde"],
"total_time_seconds": 1.76
}
```

## 🧹 Cleanup

To stop and remove the active container:

```bash
docker stop cont_guid_detector
docker rm cont_guid_detector
```

