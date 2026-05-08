"""
main.py – starter entry point for the interview exercise.

Feel free to modify, extend, or replace this file as you see fit.
"""

from xarm.wrapper import XArmAPI
import pyrealsense2 as rs
import numpy as np
import cv2
import threading
import time


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

        code = self.arm.set_gripper_mode(0)
        print('set gripper mode: location mode, code={}'.format(code))

        code = self.arm.set_gripper_enable(True)
        print('set gripper enable, code={}'.format(code))

        code = self.arm.set_gripper_speed(5000)
        print('set gripper speed, code={}'.format(code))

        self.arm.set_gripper_position(500, wait=True, speed=8000)

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
        self.arm.set_position(x=x, y=y, z=150, roll=-180, pitch=0, yaw=00, speed=100, wait=False)

    def get_latest_frame(self) -> np.ndarray:
        """Get the latest color frame from the camera."""
        return self.camera.get_latest_frame()


    def detect_banana(self,frame):
        """
        Detect banana in RGB frame using yellow thresholding.
        Returns frame with bounding box drawn.
        """

        # Convert RGB to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define yellow range in HSV
        # These values may need tuning depending on lighting
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([35, 255, 255])

        # Create mask
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Remove noise (morphological operations)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Get largest contour (assume banana is largest yellow object)
            largest_contour = max(contours, key=cv2.contourArea)

            # Ignore very small areas (noise filtering)
            if cv2.contourArea(largest_contour) > 500:
                x, y, w, h = cv2.boundingRect(largest_contour)

                # Draw bounding box
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Banana", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        return frame, mask, (x, y, w, h)

    def get_longer_dimension(self, x, y, w, h):
        """
        Returns:
            orientation (str) -> 'horizontal', 'vertical', 'diagonal'
        """

        if w == 0 or h == 0:
            return None

        ratio = w / float(h)

        # If nearly square → treat as diagonal
        if 0.8 < ratio < 1.2:
            return "diagonal"

        elif w > h:
            return "horizontal"
        else:
            return "vertical"

    def set_orientation(self, orientation, x, y):
        z = 8  # safe height
        x = 300
        y = 0

        if orientation == "horizontal":
            yaw = 90

        elif orientation == "vertical":
            yaw = 0

        elif orientation == "diagonal":
            yaw = -45

        else:
            return None

        self.arm.set_position(
            x=x,
            y=y,
            z=z,
            roll=-180,
            pitch=0,
            yaw=yaw,
            speed=100,
            wait=True
        )

        return yaw



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
    # arm.draw_square(side_length=100)
    cv2.namedWindow("Camera", cv2.WINDOW_AUTOSIZE)
    orientation_set=False
    x = 300
    y = 0 
    arm.arm.set_position(x=x, y=y, z=150, roll=-180, pitch=0, yaw=0, speed=100, wait=False)
    # code = arm.set_gripper_mode(0)


    time.sleep(5)
    while True:
        frame = arm.get_latest_frame()
        if frame is not None:
            output, mask, (x, y, w, h) = arm.detect_banana(frame)

            orientation = arm.get_longer_dimension(x, y, w, h)

            print("Detected orientation:", orientation)

            # If diagonal → rotate -45 and re-evaluate
            if orientation == "diagonal":
                print("Diagonal detected. Rotating to -45° and re-checking...")

                arm.set_orientation("diagonal", 300, 0)
                time.sleep(2)

                # Get new frame after rotation
                new_frame = arm.get_latest_frame()
                if new_frame is not None:
                    _, _, (x, y, w, h) = arm.detect_banana(new_frame)
                    orientation = arm.get_longer_dimension(x, y, w, h)

                    print("New orientation:", orientation)

            break

            cv2.imshow("f{opp_orientation}", output)
            cv2.imshow("Mask", mask)
            cv2.imshow("Camera", frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

    yaw = arm.set_orientation(orientation, x, y)
    arm.arm.set_gripper_position(220, wait=True, speed=8000)
    x = 300
    y = 0
    z = 100
    arm.arm.set_position(x=x, y=y, z=z, roll=-180, pitch=0, yaw=yaw, speed=100, wait=False)

    #move to the basket
    x = 650
    y = -20
    arm.arm.set_position(x=x, y=y, z=z, roll=-180, pitch=0, yaw=yaw, speed=100, wait=False)
    arm.arm.set_gripper_position(500, wait=True, speed=8000)





if __name__ == "__main__":
    main()
