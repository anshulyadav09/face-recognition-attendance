# face-recognition-attendance
Face Recognition Based Attendance System using Streamlit, OpenCV, and face_recognition.
# 🎓 Face Recognition Attendance System

A real-time face recognition-based attendance system built with **Streamlit**, **OpenCV**, and **face_recognition**.  
Users are recognized via webcam, and attendance is logged automatically.

> Powered by `dlib` deep learning models with ~99.38% accuracy on the LFW benchmark.

---

## 🚀 Features

- ✅ Real-time face recognition via webcam
- ✅ Admin panel to register new users
- ✅ Attendance logged with name and timestamp
- ✅ Export attendance data (CSV by month)
- ✅ Simple and intuitive Streamlit interface

---

## 🖥️ Demo

> _(Add screenshots here if available)_  
> _Or deploy with Streamlit Share / Docker and share a public link._

---

🧰 Installation
1. Clone this repository
     git clone https://github.com/your-username/face-recognition-attendance.git
     cd face-recognition-attendance
2. Create a virtual environment (optional but recommended)
     For macOS/Linux:
        python -m venv venv
        source venv/bin/activate
     For Windows:
       cmd
       python -m venv venv
       venv\Scripts\activate
3. Install required dependencies
      pip install -r requirements.txt


▶️ Run the App
    streamlit run app.py

🔐 Admin Login
    > Username: admin
    > Password: 123
 Admins can:
  > Register new users (via webcam)
  > Export monthly attendance logs


📁 Project Structure
face-recognition-attendance/
├── app.py                # Main Streamlit app
├── faces/                # Folder to store face images
├── attendance.csv        # Generated automatically
├── requirements.txt      # Python dependencies
└── README.md             # This file

⚙️ face_recognition Installation Notes
face_recognition requires dlib, which can be tricky to install on some systems.
   Windows
   Use this order:
     pip install cmake
     pip install dlib
     pip install face_recognition

 Or follow a guide like:
     https://github.com/ageitgey/face_recognition/issues/175#issuecomment-368719429

   macOS
     brew install cmake
     pip install dlib
     pip install face_recognition

 📊 Export Attendance
     Admins can export attendance logs by entering the month in YYYY-MM format and clicking "Download Attendance" in the admin panel.


🧠 How It Works
   > Face encodings are generated and saved during registration.
   >  During attendance, each detected face is compared with known encodings.
   > If matched, the user's name and timestamp are stored in attendance.csv.

📄 License
     This project is licensed under the MIT License.


🙏 Acknowledgments
  > face_recognition by @ageitgey
  > dlib by Davis King
  > Streamlit
  > OpenCV





  
