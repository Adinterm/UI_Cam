import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk

class UI_Cam:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Camera")

        self.video_source = 0  # Use default camera (change to video file path if needed)

        # Create OpenCV video capture object
        self.vid = cv2.VideoCapture(self.video_source)

        # Create a Canvas widget to display the video feed
        self.canvas = tk.Canvas(root, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Create buttons
        self.exposure_button = tk.Button(root, text="Start Long Exposure", command=self.toggle_long_exposure)
        self.exposure_button.pack()

        self.save_button = tk.Button(root, text="Save Long Exposure", command=self.save_long_exposure)
        self.save_button.pack()

        # Initialize variables for long exposure
        self.long_exposure_running = False
        self.long_exposure_frames = []

        # Start the video feed display
        self.update()

    def update(self):
        # Get the latest video frame
        ret, frame = self.vid.read()
        if ret:
            # Convert the frame from BGR to RGB and then to ImageTk format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_tk = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))

            # Update the Canvas with the new video frame
            self.canvas.create_image(0, 0, anchor=tk.NW, image=frame_tk)

            # If long exposure is running, add the frame to the list
            if self.long_exposure_running:
                self.long_exposure_frames.append(frame)

            # Repeat the update after 10 milliseconds (adjust as needed)
            self.root.after(10, self.update)

    def toggle_long_exposure(self):
        if self.long_exposure_running:
            self.stop_long_exposure()
        else:
            self.start_long_exposure()

    def start_long_exposure(self):
        if not self.long_exposure_running:
            self.long_exposure_running = True
            self.exposure_button.config(text="Stop Long Exposure")
            self.long_exposure_frames.clear()

            # Call the stop_long_exposure method after 1 minute (60000 milliseconds)
            self.root.after(60000, self.stop_long_exposure)

    def stop_long_exposure(self):
        self.long_exposure_running = False
        self.exposure_button.config(text="Start Long Exposure")

        # If there are frames captured during long exposure, average them
        if self.long_exposure_frames:
            averaged_frame = np.mean(self.long_exposure_frames, axis=0).astype(np.uint8)
            self.display_long_exposure_preview(averaged_frame)

    def display_long_exposure_preview(self, averaged_frame):
        # Convert the averaged frame to RGB and then to ImageTk format
        averaged_frame_rgb = cv2.cvtColor(averaged_frame, cv2.COLOR_BGR2RGB)
        self.averaged_frame_tk = ImageTk.PhotoImage(image=Image.fromarray(averaged_frame_rgb))

        # Create a preview window to display the long exposure result
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Long Exposure Result")
        preview_label = tk.Label(preview_window, image=self.averaged_frame_tk)
        preview_label.pack()

    def save_long_exposure(self):
        if self.long_exposure_frames:
            averaged_frame = np.mean(self.long_exposure_frames, axis=0).astype(np.uint8)
            cv2.imwrite("long_exposure_result.png", averaged_frame)

if __name__ == "__main__":
    root = tk.Tk()
    ui_cam = UI_Cam(root)
    root.mainloop()

