"""
main.py – starter entry point for the interview exercise.

Feel free to modify, extend, or replace this file as you see fit.
"""

from xarm.wrapper import XArmAPI
import pyrealsense2 as rs
import numpy as np
import cv2
import threading

class XArm:
    """Wrapper class for XArm robot control."""
    
    def __init__(self, ip: str) -> None:
        """Initialize XArm with the given IP address."""
        self.arm = XArmAPI(ip)
    
    def initialize(self) -> None:
        """Enable motion, set mode and state, then move to home position."""
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.speed = 20
        self.arm.set_servo_angle(angle=[0, -60, -30, 0, 90], speed=self.speed, wait=True)
        self.camera = Camera()

        # Stream camera in a separate thread to keep it responsive
        threading.Thread(target=self.camera.stream, daemon=True).start()

    def draw_square(self, side_length: float) -> None:
        """Draw a square with the given side length (clockwise)."""
        # Define the four corners in clockwise order
        corners = [
            (300, 0),                          # top-left
            (300, side_length),                # top-right
            (300 - side_length, side_length),  # bottom-right
            (300 - side_length, 0),            # bottom-left
        ]
        # Visit each corner and return to the start to close the square
        for x, y in corners:
            self.arm.set_position(x=x, y=y, z=150, roll=-180, pitch=0, yaw=0, speed=100, wait=False)
        # Close the square by returning to the first corner
        x, y = corners[0]
        self.arm.set_position(x=x, y=y, z=150, roll=-180, pitch=0, yaw=0, speed=100, wait=False)

    def get_latest_frame(self) -> np.ndarray:
        """Get the latest color frame from the camera."""
        return self.camera.get_latest_frame()


class Camera:

    """Wrapper class for Intel RealSense camera streaming."""

    def __init__(self) -> None:
        """Initialize the RealSense pipeline and configure the color stream."""
        self.rs = rs
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.running = False
        self.latest_frame = None
        self._lock = threading.Lock()

    def start(self) -> None:
        """Start the camera stream."""
        self.pipeline.start(self.config)
        self.running = True

    def stop(self) -> None:
        """Stop the camera stream."""
        self.running = False
        self.pipeline.stop()

    def get_frame(self) -> np.ndarray:
        """Capture and return a single color frame as a numpy array."""
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            return None
        return np.asanyarray(color_frame.get_data())

    def stream(self) -> None:
        """Capture color frames in a loop, storing the latest frame in a thread-safe manner."""
        self.start()
        try:
            while self.running:
                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                if not color_frame:
                    continue
                frame = np.asanyarray(color_frame.get_data())
                with self._lock:
                    self.latest_frame = frame
        finally:
            self.stop()

    def get_latest_frame(self) -> np.ndarray:
        """Return the latest frame in a thread-safe manner."""
        with self._lock:
            return self.latest_frame.copy() if self.latest_frame is not None else None



def main() -> None:
    arm = XArm("192.168.1.223")
    arm.initialize()
    arm.draw_square(side_length=100)
    cv2.namedWindow("Camera", cv2.WINDOW_AUTOSIZE)
    while True:
        frame = arm.get_latest_frame()
        if frame is not None:
            cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
