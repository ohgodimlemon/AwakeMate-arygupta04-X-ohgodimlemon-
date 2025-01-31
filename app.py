import cv2
import numpy as np
import face_recognition
from scipy.spatial import distance
import pygame
# Initialize pygame mixer
pygame.mixer.init()

def play_beep():
    beep_sound = pygame.mixer.Sound("beep.wav")  # Replace "beep.wav" with a valid path to a .wav file
    beep_sound.play()

def stop_beep():
    pygame.mixer.stop()  # Stop any currently playing sound


def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def process_image(frame, sleep_counter):
    if frame is None:
        raise ValueError('Image is not found or unable to open')

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations
    face_locations = face_recognition.face_locations(rgb_frame)
    
    for face_location in face_locations:
        # Extract facial landmarks
        landmarks = face_recognition.face_landmarks(rgb_frame, [face_location])[0]
        left_eye = np.array(landmarks['left_eye'])
        right_eye = np.array(landmarks['right_eye'])

        # Calculate EAR
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        # Check if eyes are closed
        
        if ear >= 0.28:
            if hasattr(process_image, "last_status"): #and process_image.last_status != "Active":
                stop_beep()  # Stop the beep if the status changes to "Active"
            process_image.last_status = "Active"
            sleep_counter = 0
            return "Active", sleep_counter

        sleep_counter += 1  # Increment sleep counter when eyes are partially or fully closed

        if 0.20 <= ear < 0.28:
            if sleep_counter > 6: #and process_image.last_status != "Drowsy":
                play_beep()  # Start beeping when drowsy
                process_image.last_status = "Drowsy"
            return "Drowsy", sleep_counter

        if ear < 0.20:
            if sleep_counter > 6: #and process_image.last_status != "Asleep":
                play_beep()  # Start beeping when asleep
                process_image.last_status = "Asleep"
            return "Asleep", sleep_counter
    
    return process_image.last_status, sleep_counter

process_image.last_status = "Active"  # Initialize status variable  
# Main function to display the webcam feed and status
def main():
    # **Live Camera Feed**
    cap = cv2.VideoCapture(0)
    sleep_counter = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        status, sleep_counter = process_image(frame, sleep_counter)
    
        # Display the video feed with status overlay
        cv2.putText(frame, f"Status: {status}", (30, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        cv2.imshow("Live Eye Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

