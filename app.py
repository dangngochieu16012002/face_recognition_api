from flask import Flask, request, jsonify
import face_recognition
import os
import base64
import numpy as np

app = Flask(__name__)

# Lưu đặc trưng khuôn mặt của nhân viên
employees_encodings = {}

# API nhận diện khuôn mặt
@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.get_json()
    image_data = base64.b64decode(data['image'])
    np_image = np.frombuffer(image_data, np.uint8)
    face = face_recognition.load_image_file(np_image)

    # Thực hiện nhận diện khuôn mặt
    result = {"employee_id": None}
    for emp_id, encoding in employees_encodings.items():
        matches = face_recognition.compare_faces([encoding], face)
        if True in matches:
            result["employee_id"] = emp_id
            break

    return jsonify(result)

# API thêm nhân viên mới
@app.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.get_json()
    emp_id = data["id"]
    emp_name = data["name"]
    image_data = base64.b64decode(data["image"])
    np_image = np.frombuffer(image_data, np.uint8)
    face = face_recognition.load_image_file(np_image)

    encoding = face_recognition.face_encodings(face)[0]
    employees_encodings[emp_id] = encoding

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
