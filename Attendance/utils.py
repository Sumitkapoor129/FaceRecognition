import cv2
import numpy as np
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import  face_recognition
import time

def capture_face_data():
    # Initialize variables
    face_encoding = None
    capture_done = False
    countdown_complete = False
    face_detection_start_time = None
    
    # Create GUI window
    window = tk.Tk()
    window.title("Face Capture")
    window.attributes('-topmost', True)
    window.focus_force()
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    # Create labels
    video_label = Label(window)
    video_label.pack()
    
    countdown_label = Label(window, text="Getting ready...", font=("Arial", 50))
    countdown_label.pack()
    
    def update_frame():
        nonlocal face_encoding, capture_done, face_detection_start_time
        
        if capture_done:
            return
            
        ret, frame = cap.read()
        if ret:
            # Convert frame for display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
            
            # If countdown is complete, try to capture face
            if countdown_complete and not capture_done:
                current_time = time.time()
                
                # Initialize face detection start time if not set
                if face_detection_start_time is None:
                    face_detection_start_time = current_time
                    countdown_label.config(text="Looking for face...")
                
                # Check if we've exceeded 10 second timeout
                if current_time - face_detection_start_time > 10:
                    # Capture frame anyway
                    face_encoding = face_recognition.face_encodings(frame_rgb)
                    if face_encoding:
                        face_encoding = face_encoding[0]
                    countdown_label.config(text="Time's up! Capturing frame...")
                    capture_done = True
                    window.after(500, window.destroy)
                    return
                else:
                    # Try to detect face
                    face_locations = face_recognition.face_locations(frame_rgb)
                    if face_locations:
                        face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)
                        if face_encodings:
                            face_encoding = face_encodings[0]
                            countdown_label.config(text="Face detected!")
                            capture_done = True
                            window.after(500, window.destroy)
                            return
                
            window.after(10, update_frame)
    
    def countdown(count):
        nonlocal countdown_complete
        if count > 0:
            countdown_label.config(text=str(count))
            window.after(1000, lambda: countdown(count - 1))
        else:
            countdown_label.config(text="Looking for face...")
            countdown_complete = True
    
    # Start countdown after a short delay
    window.after(1000, lambda: countdown(3))
    
    # Start frame updates
    update_frame()
    
    # Run GUI
    try:
        window.mainloop()
    finally:
        cap.release()
    
    # Return results
    return face_encoding

def compare_faces(encoding1, encoding2, tolerance=0.6):
    if encoding1 is None or encoding2 is None:
        return False
    
    face_distance = face_recognition.face_distance([encoding1], encoding2)
    return face_distance[0] <= tolerance