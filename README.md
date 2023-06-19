# Color_Segmentation
This code is designed to estimate the pose (position and orientation) of an object in the world coordinates based on its centroid and angle. It utilizes computer vision techniques using the OpenCV library in Python.
## Prerequisites

    - Python 3.x
    - OpenCV library
    - Numpy library

## Installation

    Clone or download the code repository from GitHub.

    Make sure you have Python 3.x installed on your system. If not, download and install Python from the official website: Python.org.

    Install the required dependencies by running the following command:

    ```pip install opencv-python numpy```

## Usage

    Open a terminal or command prompt and navigate to the directory where you have downloaded/cloned the code.

    Run the following command to execute the code:

    ```python pose_estimation.py```

    The code will access your default camera and start capturing frames.

    Hold an object with distinct colors (red, green, blue, or yellow) in front of the camera.

    The code will estimate the pose of the object and display the output on the screen.

    Press the 'q' key to quit and close the application.

## Functionality

The code performs the following tasks:

    - pose_estimate(centroid, angle): This function estimates the pose of an object based on its centroid and angle. It calculates the object's position (x and y) in millimeters in the world coordinates. It also prints the position and angle information and returns the centroid coordinates.

    - determine_orientation(image): This function determines the orientation of colored contours and the 2D pose in the provided image. It takes an image as input and performs the following steps:
        * Converts the image to the HSV color space.
        * Defines color ranges for red, green, blue, and yellow.
        * Creates a mask based on the color ranges.
        * Finds contours in the masked image.
        * Calculates the orientation of each contour using PCA (Principal Component Analysis).
        * Draws the contours and orientation lines on the image.
        * Calls the pose_estimate function to estimate the pose of each contour.
        * Displays the image with contours and orientation lines.

    - main(): This is the main function of the code. It initializes the video capture from the default camera and continuously reads frames. It calls the determine_orientation function to process each frame. The application can be terminated by pressing the 'q' key.

## Customization

    You can modify the color ranges in the determine_orientation function to match the colors of the objects you want to detect.

    Feel free to adjust the image display window size by modifying the values in the cv2.resizeWindow function.

    Additional functionalities or modifications can be made to suit your specific requirements.
