from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import face_recognition
from scipy.spatial import distance
import pygame

# Initialize Flask application
app = Flask(__name__)

# Initialize pygame mixer for sound alerts (e.g., beeping sounds)
pygame.mixer.init()

# Function to play beep sound
def play_beep():
    beep_sound = pygame.mixer.Sound("beep.wav")  # Ensure path to beep sound is correct
    beep_sound.play()

# Function to stop beep sound
def stop_beep():
    pygame.mixer.stop()

# Function to calculate Eye Aspect Ratio (EAR) for eye tracking
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])  # Distance between vertical eye landmarks
    B = distance.euclidean(eye[2], eye[4])  # Distance between vertical eye landmarks
    C = distance.euclidean(eye[0], eye[3])  # Distance between horizontal eye landmarks
    ear = (A + B) / (2.0 * C)  # Calculate EAR
    return ear

# Global flags to control detection state
detection_active = False  # Flag to check if detection is active
detection_paused = False  # Flag to check if detection is paused
sleep_counter = 0  # Counter to track sleep state based on EAR

# Function to process each frame of video for face and eye detection
def process_image(frame):
    global sleep_counter, detection_active, detection_paused

    # If no frame is received or detection is inactive, return default status
    if frame is None or not detection_active:
        return "No Frame", sleep_counter

    # Convert frame to RGB for face recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)

    # Loop through all detected faces
    for face_location in face_locations:
        # Find facial landmarks (including eyes) for each face
        landmarks = face_recognition.face_landmarks(rgb_frame, [face_location])[0]
        left_eye = np.array(landmarks['left_eye'])
        right_eye = np.array(landmarks['right_eye'])

        # Calculate EAR for both eyes
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0  # Average EAR for both eyes

        # Determine the status based on EAR value
        if ear >= 0.28:  # Active if EAR is above threshold
            stop_beep()  # Stop beeping sound
            sleep_counter = 0  # Reset sleep counter
            return "Active", sleep_counter

        sleep_counter += 1  # Increment sleep counter if EAR is below threshold

        # Drowsy state: EAR between 0.20 and 0.28 and sleep counter exceeds threshold
        if 0.20 <= ear < 0.28 and sleep_counter > 6:
            play_beep()  # Play beep sound
            return "Drowsy", sleep_counter

        # Asleep state: EAR below 0.20 and sleep counter exceeds threshold
        if ear < 0.20 and sleep_counter > 6:
            play_beep()  # Play beep sound
            return "Asleep", sleep_counter

    # Default status is "Active" if no sleep-related conditions are met
    return "Active", sleep_counter

# Function to generate video stream frames
def generate_frames():
    global detection_active, detection_paused, sleep_counter

    # Initialize video capture from default webcam (device 0)
    cap = cv2.VideoCapture(0)

    # Continuously capture and process video frames
    while True:
        success, frame = cap.read()
        if not success:
            break

        # If detection is active and not paused, process the frame
        if detection_active and not detection_paused:
            status, sleep_counter = process_image(frame)
        else:
            status = "Paused"  # Show "Paused" if detection is inactive or paused

        # Add status text on the video frame
        cv2.putText(frame, f"Status: {status}", (30, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Encode the frame as JPEG to send over HTTP
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame in the appropriate format for live streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # Release the video capture after processing
    cap.release()

# Route to render the index HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to stream video feed to the front-end
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to start the detection process
@app.route('/start_detection')
def start_detection():
    global detection_active, detection_paused
    detection_active = True  # Activate detection
    detection_paused = False  # Ensure detection is not paused
    return jsonify({"status": "Detection Started"})  # Return status as JSON response

# Route to pause the detection process
@app.route('/pause_detection')
def pause_detection():
    global detection_paused
    detection_paused = True  # Pause detection
    return jsonify({"status": "Detection Paused"})  # Return status as JSON response

# Route to resume the detection process
@app.route('/resume_detection')
def resume_detection():
    global detection_paused
    detection_paused = False  # Resume detection
    return jsonify({"status": "Detection Resumed"})  # Return status as JSON response

# Route to stop the detection process
@app.route('/end_detection')
def end_detection():
    global detection_active, detection_paused
    detection_active = False  # Deactivate detection
    detection_paused = False  # Reset pause flag
    return jsonify({"status": "Detection Ended"})  # Return status as JSON response

# Run the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)
