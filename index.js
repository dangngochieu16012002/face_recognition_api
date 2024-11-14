const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql2');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// Kết nối đến MySQL trên InfinityFree
const db = mysql.createConnection({
  host: "sql312.infinityfree.com",
  user: "if0_37577660",
  password: "Hieu16012002",
  database: "if0_37577660_membershiphp"
});

db.connect((err) => {
  if (err) throw err;
  console.log("Đã kết nối đến cơ sở dữ liệu MySQL");
});

// Route thêm nhân viên mới
app.post('/add-employee', async (req, res) => {
  const { name, employeeId, photos } = req.body;

  // Lưu ảnh và thông tin nhân viên vào CSDL
  db.query("INSERT INTO employees (name, employee_id) VALUES (?, ?)", [name, employeeId], (err) => {
    if (err) throw err;
    res.json({ status: 'success', message: `Nhân viên ${name} đã được thêm thành công!` });
  });
});

// Route chấm công
app.post('/attendance', async (req, res) => {
  const { image, type } = req.body;

  try {
    // Ở đây, bạn có thể tích hợp với thư viện nhận diện khuôn mặt như `face-api.js` trên server Node.js
    // Dự kiến dùng face-api.js để nhận diện và so sánh ảnh
    const isRecognized = true; // Thay bằng logic nhận diện

    if (isRecognized) {
      const employeeName = "Tên Nhân Viên"; // Lấy từ kết quả nhận diện khuôn mặt

      // Lưu bản ghi chấm công vào MySQL
      db.query("INSERT INTO attendance_logs (employee_name, attendance_type) VALUES (?, ?)", [employeeName, type], (err) => {
        if (err) throw err;
        res.json({ status: 'success', message: `Đã ${type} thành công cho nhân viên ${employeeName}` });
      });
    } else {
      res.json({ status: 'fail', message: "Không tìm thấy khuôn mặt hoặc không khớp với nhân viên nào." });
    }
  } catch (error) {
    res.status(500).json({ status: 'error', message: 'Lỗi khi nhận diện khuôn mặt' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server đang chạy trên cổng ${PORT}`);
});
