import cv2
import numpy as np
from progress.bar import PixelBar
import time
import random

"""DOCSTRING:
The program performs the following functions: 
using the built-in computer vision methods from the OpenCV library, 
as well as using mathematical calculations from the NumPy library, 
a model for searching and identifying road marking lines is built 
(widespread use: self-driving-cars) 
"""


def make_coordinates(image, line_parameters):
    # Y = MX + B
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3/5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):

    left_fit = []
    right_fit = []

    while lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))

        left_fit_average = np.average(left_fit, axis=0)
        print('LEFT: ', left_fit_average)
        left_line = make_coordinates(image, left_fit_average)
        right_fit_average = np.average(right_fit, axis=0)
        right_line = make_coordinates(image, right_fit_average)
        print('RIGHT: ', right_fit_average)
        return np.array([left_line, right_line])


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 15)
    return line_image


def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([(200, height), (1100, height), (550, 250)])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, np.array([polygons], dtype=np.int64), 1024)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


"""IMAGE DETECTION LINE'S"""

# image = cv2.imread('road.jpg')
# lane_image = np.copy(image)
# canny_image = canny(lane_image)
# cropped_image = region_of_interest(canny_image)
# lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([()]),
# minLineLength=40, maxLineGap=5)
# averaged_lines = average_slope_intercept(lane_image, lines)
# line_image = display_lines(lane_image, averaged_lines)
# combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)

# cv2.imshow('result', combo_image)
# cv2.waitKey(0)

"""Debugger for GCP"""

if __name__ == '__main__':

    """GCP DEBUGGER"""

    try:
        import googleclouddebugger
        googleclouddebugger.enable(
            module='[detection]',
            version='[v 1.0]',
            service_account_json_file='/Users/'
                                      'admin/Downloads/savvy-etching-254922-e6fda8dabd2c.json')
    except ImportError:
        pass


def sleep():
    t = 0.01
    t += t * random.uniform(-0.1, 0.1)  # Add some variance
    time.sleep(t)


suffix = '%(index)d/%(max)d [%(elapsed)d / %(eta)d / %(eta_td)s]'
bar = PixelBar('PROCESSING', suffix=suffix)
for i in bar.iter(range(150)):
    sleep()


"""VIDEO DETECTION LINE'S"""


cap = cv2.VideoCapture("test2.mp4")
while cap.isOpened():
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    # Угловой коээфициент
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([()]),
                            minLineLength=40,
                            maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow('result', combo_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
