# Importing required libraries
import cv2
import numpy as np
from imgbeddings import imgbeddings
from PIL import Image
import psycopg2
import os
from openpyxl import Workbook
from datetime import datetime

# Paths
ALG_PATH = "/home/clutchmac/Desktop/FR/haarcascade_frontalface_default.xml"
IMAGE_PATH = "/home/clutchmac/Desktop/FR/WhatsApp Image 2025-06-14 at 12.08.57 AM.jpeg"
CROPPED_FACES_DIR = "/home/clutchmac/Desktop/FR/stored-faces/"
DB_CONNECTION = "postgres://avnadmin:AVNS_AnbZlD4S63-OBG1_1yw@pg-258135ce-omkarputti14-d2b5.b.aivencloud.com:16233/defaultdb?sslmode=require"
ATTENDANCE_FILE = "attendance.xlsx"

# Ensure the directory for cropped faces exists
os.makedirs(CROPPED_FACES_DIR, exist_ok=True)

# Load Haar Cascade
if not os.path.exists(ALG_PATH):
    raise FileNotFoundError(f"Haarcascade file not found at {ALG_PATH}")
haar_cascade = cv2.CascadeClassifier(ALG_PATH)

# Load and process the image
img = cv2.imread(IMAGE_PATH)
if img is None:
    raise ValueError(f"Image at {IMAGE_PATH} could not be loaded. Check the file path.")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = haar_cascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=5, minSize=(100, 100))
if len(faces) == 0:
    print("No faces detected.")
else:
    print(f"{len(faces)} face(s) detected.")

# Save cropped faces
for i, (x, y, w, h) in enumerate(faces):
    cropped_image = img[y:y + h, x:x + w]
    target_file_name = os.path.join(CROPPED_FACES_DIR, f"{i}.jpg")
    cv2.imwrite(target_file_name, cropped_image)
    print(f"Cropped face saved at {target_file_name}")

# Initialize Excel workbook
wb = Workbook()
ws = wb.active
ws.title = "Attendance"
ws.append(["Student ID", "Name", "Date"])  # Header row

# Connect to the database and process attendance
try:
    conn = psycopg2.connect(DB_CONNECTION)
    cur = conn.cursor()
    ibed = imgbeddings()

    for filename in os.listdir(CROPPED_FACES_DIR):
        filepath = os.path.join(CROPPED_FACES_DIR, filename)
        img = Image.open(filepath)
        embedding = ibed.to_embeddings(img)
        embedding_str = ",".join(map(str, embedding[0].tolist()))

        # Query for the most similar student face in the database
        cur.execute("SELECT student_id, name FROM students ORDER BY embedding <-> %s LIMIT 1;", (embedding_str,))
        row = cur.fetchone()

        if row:
            student_id, student_name = row
            print(f"Attendance recorded for {student_name} (ID: {student_id}).")
            ws.append([student_id, student_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        else:
            print(f"Face in {filename} not recognized. No match found.")

    # Save the attendance sheet
    wb.save(ATTENDANCE_FILE)
    print(f"Attendance sheet saved as {ATTENDANCE_FILE}. Open it in VS Code for details.")

    conn.commit()
    cur.close()

except psycopg2.Error as db_error:
    print(f"Database error: {db_error}")
except Exception as general_error:
    print(f"An unexpected error occurred: {general_error}")
finally:
    if 'conn' in locals() and conn:
        conn.close()