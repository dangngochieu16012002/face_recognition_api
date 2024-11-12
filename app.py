from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import numpy as np
import base64
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Thư mục chứa ảnh mẫu của nhân viên
EMPLOYEE_DIR = "./employees/"

# Kết nối đến cơ sở dữ liệu MySQL
def connect_db():
    return mysql.connector.connect(
        host="sql312.infinityfree.com",
        user="if0_37577660",
        password="Hieu16012002",
        database="if0_37577660_membershiphp"
    )

# Tải khuôn mặt của nhân viên
def load_employee_faces():
    employee_faces = []
    employee_names = []
    for folder in os.listdir(EMPLOYEE_DIR):
        folder_path = os.path.join(EMPLOYEE_DIR, folder)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith(".jpg"):
                    image_path = os.path.join(folder_path, filename)
                    image = face_recognition.load_image_file(image_path)
                    encoding = face_recognition.face_encodings(image)
                    if encoding:
                        employee_faces.append(encoding[0])
                        employee_names.append(folder)
    return employee_faces, employee_names

employee_faces, employee_names = load_employee_faces()

# Route để nhận diện khuôn mặt
@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.json
    image_data = base64.b64decode(data['image'])
    attendance_type = data['type']
    np_image = np.frombuffer(image_data, np.uint8)
    img = face_recognition.load_image_file(np_image)

    face_encodings = face_recognition.face_encodings(img)
    if face_encodings:
        face_encoding = face_encodings[0]
        matches = face_recognition.compare_faces(employee_faces, face_encoding)
        if True in matches:
            match_index = matches.index(True)
            employee_name = employee_names[match_index]

            # Lưu dữ liệu chấm công vào bảng `attendance_logs`
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO attendance_logs (employee_name, attendance_type, timestamp) VALUES (%s, %s, %s)",
                (employee_name, attendance_type, datetime.now())
            )
            conn.commit()
            conn.close()

            return jsonify({"status": "success", "message": f"{employee_name} đã {attendance_type} thành công!"}), 200

    return jsonify({"status": "fail", "message": "Không tìm thấy khuôn mặt hoặc không khớp với nhân viên nào."}), 404

# Route để thêm nhân viên
@app.route('/add-employee', methods=['POST'])
def add_employee():
    data = request.json
    employee_id = data['employeeId']
    name = data['name']
    photos = data['photos']

    # Tạo thư mục lưu ảnh của nhân viên
    folder_path = os.path.join(EMPLOYEE_DIR, name)
    os.makedirs(folder_path, exist_ok=True)

    for i, photo in enumerate(photos):
        img_data = base64.b64decode(photo.split(',')[1])
        with open(os.path.join(folder_path, f"{name}_{employee_id}_{i+1}.jpg"), "wb") as f:
            f.write(img_data)

    # Lưu dữ liệu nhân viên vào bảng `employees`
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (name, employee_id) VALUES (%s, %s)",
        (name, employee_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": f"Nhân viên {name} đã được thêm thành công!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
