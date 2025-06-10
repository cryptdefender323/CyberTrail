from rich.console import Console
import requests
import os
from PIL import Image
from PIL.ExifTags import TAGS
from bs4 import BeautifulSoup
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By

console = Console()

GOOGLE_API_URL = "https://www.google.com/searchbyimage" 
YANDEX_API_URL = "https://yandex.com/images/search" 
SAUCENAO_API_URL = "https://saucenao.com/search.php" 

def display_image_preview(image_path):
    console.print("Displaying image preview...")
    try:
        image = Image.open(image_path)
        image.show()
    except Exception as e:
        console.print(f"Failed to display image preview: {e}")

def extract_metadata(image_path):
    console.print("Extracting metadata from image...")
    if not os.path.exists(image_path):
        console.print("Image file not found.")
        return {}
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if not exif_data:
            console.print("No metadata found in the image.")
            return {}
        metadata = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            metadata[tag] = value
        return metadata
    except Exception as e:
        console.print(f"Metadata extraction failed: {e}")
        return {}

def google_reverse_image_search(image_path):
    console.print("Performing reverse image search using Google...")
    try:
        if not os.path.exists(image_path):
            console.print("Image file not found.")
            return {"error": "File not found"}
        with open(image_path, "rb") as image_file:
            files = {"encoded_image": image_file}
            response = requests.post(
                GOOGLE_API_URL,
                headers={"User-Agent": "Mozilla/5.0"},
                files=files
            )
        if response.status_code == 200:
            results = []
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                url = link["href"]
                if "http" in url and "google.com" not in url:
                    results.append(url)
            return {"results": results[:5]}
        else:
            return {"error": f"Google API returned status code {response.status_code}"}
    except Exception as e:
        console.print(f"Reverse image search failed: {e}")
        return {"error": str(e)}

def yandex_reverse_image_search(image_path):
    console.print("Performing reverse image search using Yandex...")
    try:
        if not os.path.exists(image_path):
            console.print("Image file not found.")
            return {"error": "File not found"}
        with open(image_path, "rb") as image_file:
            files = {"upfile": image_file}
            response = requests.post(
                YANDEX_API_URL,
                headers={"User-Agent": "Mozilla/5.0"},
                files=files,
                params={"rpt": "imageview"}
            )
        if response.status_code == 200:
            results = []
            for link in response.text.split('href="')[1:]:
                url = link.split('"')[0]
                if "http" in url:
                    results.append(url)
            return {"results": results[:5]}
        else:
            return {"error": f"Yandex API returned status code {response.status_code}"}
    except Exception as e:
        console.print(f"Reverse image search failed: {e}")
        return {"error": str(e)}

def saucenao_reverse_image_search(image_path):
    console.print("Performing reverse image search using SauceNAO...")
    try:
        driver = webdriver.Chrome()
        driver.get(SAUCENAO_API_URL)
        upload_input = driver.find_element(By.NAME, "file")
        upload_input.send_keys(image_path)
        driver.find_element(By.ID, "form").submit()
        results = []
        for link in driver.find_elements(By.TAG_NAME, "a"):
            url = link.get_attribute("href")
            if url and "http" in url:
                results.append(url)
        driver.quit()
        return {"results": results[:5]}
    except Exception as e:
        console.print(f"Reverse image search failed: {e}")
        return {"error": str(e)}

def deepfake_detection(image_path):
    console.print("Performing deepfake detection using OpenCV...")
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(faces) == 0:
            console.print("No faces detected.")
            return {"face_count": 0}
        return {"face_count": len(faces), "faces": [{"x": int(x), "y": int(y), "width": int(w), "height": int(h)} for (x, y, w, h) in faces]}
    except Exception as e:
        console.print(f"Deepfake detection failed: {e}")
        return {"error": str(e)}

def run():
    console.print("Enter the path to the image for reverse image search:")
    image_path = input("> ").strip()
    if not image_path or not os.path.exists(image_path):
        console.print("Image file not found.")
        return
    display_image_preview(image_path)
    metadata = extract_metadata(image_path)
    console.print("Metadata Results:")
    console.print(metadata)
    google_results = google_reverse_image_search(image_path)
    console.print("Google Reverse Image Search Results:")
    console.print(google_results)
    if "error" in google_results:
        console.print("Google search failed, trying Yandex...")
        yandex_results = yandex_reverse_image_search(image_path)
        console.print("Yandex Reverse Image Search Results:")
        console.print(yandex_results)
        if "error" in yandex_results:
            console.print("Yandex search failed, trying SauceNAO...")
            saucenao_results = saucenao_reverse_image_search(image_path)
            console.print("SauceNAO Reverse Image Search Results:")
            console.print(saucenao_results)
    deepfake_results = deepfake_detection(image_path)
    console.print("Deepfake Detection Results:")
    console.print(deepfake_results)

if __name__ == "__main__":
    run()