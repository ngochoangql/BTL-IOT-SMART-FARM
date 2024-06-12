// server.js
const mosca = require('mosca');
const fs = require('fs')
// Cấu hình server MQTT
const settings = {
  port: 1883, // Cổng mặc định của MQTT
};

// Khởi tạo MQTT broker
const server = new mosca.Server(settings);

// Xử lý sự kiện khi broker được khởi động
server.on('ready', function() {
  console.log('Mosca server is up and running on port 1883');
});

// Xử lý sự kiện khi một client kết nối đến broker
server.on('clientConnected', function(client) {
  console.log('Client connected:', client.id);
});

// Xử lý sự kiện khi một client ngắt kết nối từ broker
server.on('clientDisconnected', function(client) {
  console.log('Client disconnected:', client.id);
});

const express = require('express');
const app = express();

// API endpoint for data synchronization
app.get('/api/schedulers', (req, res) => {
    // Đọc dữ liệu từ tệp schedulers.json
    fs.readFile('schedulers.json', 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading file:', err);
            res.status(500).send('Internal server error');
            return;
        }

        // Chuyển đổi dữ liệu JSON thành đối tượng JavaScript
        const schedulers = JSON.parse(data);
        
        // Trả về dữ liệu qua API
        res.json(schedulers);
    });
});

// Start the Express server
const port = 3000; // Choose a port number
app.listen(port, () => {
    console.log(`Express server is running on port ${port}`);
});