#!/usr/bin/env python3
import numpy as np
import cv2

'''
Function estimating the pose (position and orientation) of an object in the world coordinates
based on the centroid and angle provided.
'''
def pose_estimate(centroid, angle):
    camera_matrix = np.array([[501.81184683, 0.0, 479.35810145],
                              [0.0, 500.84575607, 287.31698522],
                              [0.0, 0.0, 1.0]])
    # dot product of inverse of camera matrix and homogeneous centroid to get centroid in world coordinates
    centroid_world = np.dot(np.linalg.inv(camera_matrix),
                            np.array([centroid[0], centroid[1], 1]))
    # normalize the centroid to get the actual (x, y) values in millimeters
    centroid_world /= centroid_world[2]

    print("X in mm: {}, Y in mm: {}".format(centroid_world[0], centroid_world[1]))
    print("Angle in degrees:", angle)
    return centroid_world[0], centroid_world[1]

'''
Function determining the orientation of colored contours and the 2D pose in the image
'''
def determine_orientation(image):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    red1_Lower = (0, 100, 20)
    red1_Upper = (4, 255, 255)
    red2_Lower = (160,100,20) #
    red2_Upper= (176,255,255) #
    green_Lower = (38, 20, 50)  # adjusted lower bound for green
    green_Upper = (78, 255, 255)  # adjusted upper bound for green
    blue_Lower = (90, 100, 35) #  # adjusted lower bound for blue
    blue_Upper = (120, 255, 255)  # adjusted upper bound for blue
    yellow_Lower = (11, 50, 0)  # adjusted lower bound for yellow
    yellow_Upper = (35, 255, 255)  # adjusted upper bound for yellow

   # Create a mask based on the color range
    mask1 = cv2.inRange(hsv_image, red1_Lower, red1_Upper)
    mask2 = cv2.inRange(hsv_image, red2_Lower, red2_Upper) # red upper mask
    mask3 = cv2.inRange(hsv_image, green_Lower, green_Upper)  
    mask4 = cv2.inRange(hsv_image, blue_Lower, blue_Upper) 
    mask5 = cv2.inRange(hsv_image, yellow_Lower, yellow_Upper) 
    mask = mask3 + mask2 + mask3  + mask4 
    # Find contours of the segmented figure
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contours were found
    if len(contours) > 0:
        # Iterate over all contours
        
        for contour in contours:
            # Calculate the orientation of the contour using PCA
            contour_points = np.squeeze(contour.astype(np.float32))
            if contour_points.shape[0] <= 100:
                continue
            
            _, v = cv2.PCACompute(contour_points,mean =None)
            orientation_vector = v[0]
            angle = np.arctan2(orientation_vector[1], orientation_vector[0]) * 180 / np.pi
            # Draw the contour and the orientation line on the image (optional)
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
            center = np.mean(contour_points, axis=0)#.astype(int)
            endpoint = (int(center[0] + np.cos(np.radians(angle)) * 100),
                        int(center[1] + np.sin(np.radians(angle)) * 100))
            cv2.line(image, tuple(center), endpoint, (0, 0, 255), 2)
            x, y = pose_estimate(center,angle)

            # Put the coordinates on the image
            text = f"x: {x*100:.2f}  y: {y*100:.2f} angle: {angle:.2f}"
            cv2.putText(image, text, (int(center[0]), int(center[1]) - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)

         # Draw a line at the top-left corner of the image
        corner_line_color = (0, 0, 255)  # Red color (BGR format)
        cv2.line(image, (50, 50), (300, 50), corner_line_color, 2)
        cv2.line(image, (50, 50), (50, 300), corner_line_color, 2)
        text_x = f"x(mm)"
        text_y = f"y(mm)"
        cv2.putText(image, text_y, (60,300),
                cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), 2)
        cv2.putText(image, text_x, (330,50),
                cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), 2)
        # Display the image with the contours and orientation lines (optional)
        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("image", 1200, 800)
        cv2.imshow("image", image)
    else:
        print("No contours found.")
             
def main(): 

    video_capture = cv2.VideoCapture(0)  
    while(True):
        ret, frame = video_capture.read()
        determine_orientation(frame)  # Adjust the color range as per your requirement
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

if __name__ == '__main__':
    global cx, cy
    main() 
