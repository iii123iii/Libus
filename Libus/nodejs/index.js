const express = require('express');
const http = require('http');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const io = require('socket.io')(server, {
    cors: {
        origin: ["http://127.0.0.1:8000", "localhost:8000"],
        methods: ["GET", "POST"],
        credentials: true,
    }
});

app.use(cors({
    origin: ["http://127.0.0.1:8000", "localhost:8000"],
    credentials: true,
    optionSuccessStatus: 200,
}));

const userSocketMap = new Map();

io.on('connection', (socket) => {
    // Handle user registration
    socket.on('register', (userId) => {
        // If the user ID is not in the map, initialize an array for it
        if (!userSocketMap.has(userId)) {
            userSocketMap.set(userId, []);
        }

        // Add the current socket to the array for the user ID
        userSocketMap.get(userId).push(socket);

    });

    // Handle incoming messages
    socket.on('message', (data) => {
        // Assuming the data includes a 'to' field specifying the target user ID
        const toUserId = data.to;

        // Check if the target user is registered
        if (userSocketMap.has(toUserId)) {
            // Get the array of sockets for the target user ID
            const toUserSockets = userSocketMap.get(toUserId);

            // Send the message to all sockets of the target user
            toUserSockets.forEach((toUserSocket) => {
                if (data.text.trim()) {
                    toUserSocket.emit('message', {
                        to: data.to,
                        me: data.me,
                        message: data.text,
                        d: true,
                    });
                }
            });
        }

        const UserId = data.me;

        // Check if the target user is registered
        if (userSocketMap.has(UserId) && data.to != data.me) {
            // Get the array of sockets for the target user ID
            const toUserSockets = userSocketMap.get(UserId);

            // Send the message to all sockets of the target user
            toUserSockets.forEach((toUserSocket) => {
                if (data.text.trim()) {
                    toUserSocket.emit('message', {
                        to: data.to,
                        me: data.me,
                        message: data.text,
                        d: true,
                    });
                }
            });
        }
    });

    // Handle disconnection
    socket.on('disconnect', () => {
        // Remove the disconnected socket from the array for the corresponding user ID
        userSocketMap.forEach((sockets, key) => {
            userSocketMap.set(
                key,
                sockets.filter((userSocket) => userSocket !== socket)
            );
        });
    });
});

const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
