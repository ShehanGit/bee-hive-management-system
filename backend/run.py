# run.py

from app import create_app
from flask_cors import CORS

app = create_app()
CORS(app)  # Enable CORS for all routes

if __name__ == "__main__":
    app.run(debug=True)



# # This patch is essential for Socket.IO to work with long-polling and web-sockets.
# import eventlet
# eventlet.monkey_patch()

# # Import the app factory and the socketio instance from the app package.
# from app import create_app, socketio

# # Create the Flask application instance.
# app = create_app()

# @socketio.on('connect')
# def handle_connect():
#     """
#     Server-side event handler for when a new client connects via Socket.IO.
#     This is useful for logging connections or initializing user-specific data.
#     """
#     print("Client connected")
#     print("Starting real-time monitoring...")

# # The main entry point for the application.
# if __name__ == "__main__":
#     """
#     Use socketio.run() instead of app.run() to start the server.
#     This ensures that the web server is compatible with Socket.IO and can handle
#     both standard HTTP requests and WebSocket connections.
#     host="0.0.0.0" makes the server accessible on the local network.
#     """
#     socketio.run(app, host="0.0.0.0", port=5000, debug=True)