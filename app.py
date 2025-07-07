import streamlit as st
import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pandas as pd
from PIL import Image

# Ensure faces folder exists
if not os.path.exists('faces'):
    os.makedirs('faces')

# ----------------- Load Known Faces -----------------
def load_known_faces():
    known_encodings = []
    known_names = []
    for filename in os.listdir('faces'):
        if filename.endswith('.jpg'):
            path = os.path.join('faces', filename)
            img = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(img)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
    return known_encodings, known_names

# ----------------- Mark Attendance -----------------
def mark_attendance(name):
    file_path = 'attendance.csv'
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=["Name", "Timestamp"])

    if not ((df['Name'] == name) & (df['Timestamp'].str.startswith(now.strftime('%Y-%m-%d')))).any():
        new_entry = {"Name": name, "Timestamp": timestamp}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(file_path, index=False)

# ----------------- Face Recognition -----------------
def recognize_face():
    st.info("Initializing camera for face recognition...")
    known_encodings, known_names = load_known_faces()
    if not known_encodings:
        st.warning("No registered faces found. Please register a face.")
        return

    cap = cv2.VideoCapture(0)
    start_time = datetime.now()

    FRAME_WINDOW = st.image([])

    while (datetime.now() - start_time).seconds < 5:
        ret, frame = cap.read()
        if not ret:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]
                    mark_attendance(name)

            top, right, bottom, left = [v * 4 for v in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    cap.release()
    st.success("Face recognition completed.")

# ----------------- Register Face -----------------
def register_face(name):
    cap = cv2.VideoCapture(0)
    start_time = datetime.now()
    face_saved = False

    st.info("Capturing face image...")

    while (datetime.now() - start_time).seconds < 5:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations:
            top, right, bottom, left = face_locations[0]
            face_image = frame[top:bottom, left:right]
            if face_image.size != 0:
                filepath = f"faces/{name}.jpg"
                cv2.imwrite(filepath, face_image)
                face_saved = True
                break

    cap.release()

    return face_saved

# ----------------- Main Streamlit App -----------------
st.title("Face Recognition Attendance System")

menu = st.sidebar.selectbox("Menu", ["Home", "Admin Login"])

if menu == "Home":
    if st.button("Start Attendance"):
        recognize_face()

elif menu == "Admin Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "123":
            st.success("Welcome, Admin!")

            st.subheader("Register New Face")
            new_name = st.text_input("Enter Name")
            if st.button("Register Face"):
                if new_name:
                    if register_face(new_name):
                        st.success(f"Face registered for {new_name}")
                    else:
                        st.warning("Face not detected. Try again.")
                else:
                    st.warning("Please enter a name.")

            st.subheader("Download Attendance by Month")
            month = st.text_input("Enter Month (YYYY-MM)")
            if st.button("Download Attendance"):
                if os.path.exists("attendance.csv"):
                    df = pd.read_csv("attendance.csv")
                    filtered = df[df['Timestamp'].str.startswith(month)]
                    if not filtered.empty:
                        st.download_button(
                            label="Download CSV",
                            data=filtered.to_csv(index=False),
                            file_name=f"attendance_{month}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("No records found for this month.")
                else:
                    st.warning("Attendance file not found.")
        else:
            st.error("Invalid login credentials.")
