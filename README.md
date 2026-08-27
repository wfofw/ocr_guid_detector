<p align="center">
  <a href="https://www.python.org/downloads/release/python-3104/"><img src="https://img.shields.io/badge/python-3.10.4-3776AB?logo=python&logoColor=white" alt="Python 3.10.4"></a>
  <a href="https://www.docker.com/products/docker-desktop/"><img src="https://img.shields.io/badge/Docker-29.7.2-2496ED?logo=docker&logoColor=white" alt="Docker 29.7.2"></a>
</p>

## 👁 guid_detector

guid_detector is an automatic detector based on optical character recognition Tesseract-OCR.

It works with screenshots, photos (in the future with PDF, Word, etc.), recognizes GUIDs (Globally Unique Identifiers) and displays them as text on the screen.

## 🌟 Highlights

- Successful detection rate reaches 99.9%
- Scalable for simultaneous processing of thousands of files
- Different configurations can be used depending on requirements

## ℹ️ Overview

To successfully recognize GUIDs, which can be located anywhere, in any font, and in any size, Tesseract-OCR was used as a basis, but:
- its success rate was ~20-30% (of characters)
- it didn't collect complete words
- it produced a lot of garbage

Therefore, a preprocessing system was implemented:
- a slicing and layering method was used
- using different detection configurations (such as threshold, scales, invert, etc.)
- processing of color and black-and-white characters

The killer feature of this project is eliminating incorrect parts of the GUID from the final result.

## ⚙️ Installation

Clone repository:

```bash
git clone https://github.com/wfofw/ocr_guid_detector.git
cd ocr_guid_detector
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Build a Docker image and run automatic tests

```bash
docker build -t guid-detector .
docker run --rm guid-detector
```

## 🛠 Running Demo Script

The demo.py script contains a file named *sample_screenshot_2.jpeg*

For testing you can use the command below, which will perform a full scan cycle with the output of the found GUIDs

```bash
docker run --rm -v ${PWD}:/app guid-detector python demo.py
```

## 📦 Local Setup (Without Docker)

If you want to run the project directly in your local Python environment:

Install the Tesseract OCR system dependency:

Linux: 

```bash 
sudo apt install tesseract-ocr
```

Windows: Download the Tesseract-OCR installer and add the path to the executable to your system PATH variable.

Install the virtual environment and dependencies:

```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pytest
```

Run tests or demos

```bash
pytest -v
python demo.py path/to/image.png
```
