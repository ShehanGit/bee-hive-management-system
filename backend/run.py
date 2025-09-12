# # run.py

# from app import create_app
# from flask_cors import CORS

# app = create_app()
# CORS(app)  # Enable CORS for all routes

# if __name__ == "__main__":
#     app.run(debug=True)


# run.py
import eventlet
eventlet.monkey_patch()

from app import create_app, socketio

app = create_app()

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    print("Starting real-time monitoring...")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
