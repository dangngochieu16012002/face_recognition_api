const video = document.getElementById('video');
const canvas = document.createElement('canvas');
canvas.width = video.width;
canvas.height = video.height;

navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
});

document.getElementById('capture-photo').onclick = () => {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    document.getElementById('save-employee').disabled = false;
};

document.getElementById('save-employee').onclick = () => {
    const employeeName = document.getElementById('employee-name').value;
    const employeeId = document.getElementById('employee-id').value;
    const dataURL = canvas.toDataURL('image/jpeg');

    fetch('/add-employee', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: employeeName,
            employeeId: employeeId,
            photos: [dataURL]
        })
    }).then(response => response.json()).then(data => {
        alert(data.message);
    });
};

async function recognizeFace(attendanceType) {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const base64Image = canvas.toDataURL('image/jpeg').split(',')[1];

    const response = await fetch('/attendance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            image: base64Image,
            type: attendanceType
        })
    });

    const result = await response.json();
    alert(result.message);
}

document.getElementById('check-in').onclick = () => recognizeFace('in');
document.getElementById('check-out').onclick = () => recognizeFace('out');
