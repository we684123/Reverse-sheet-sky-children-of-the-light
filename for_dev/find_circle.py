from pathlib import Path

import cv2

import numpy as np


img_path = str(Path("./video_link_line.png").resolve())
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray.get_imag()


circles = cv2.HoughCircles(gray, method=cv2.HOUGH_GRADIENT, dp=1, minDist=30,
                           param1=75, param2=30, minRadius=0, maxRadius=300)

circles = np.uint16(np.around(circles))

cimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
for i in circles[0, :]:
    # draw the outer circle
    cv2.circle(cimg, (int(i[0]), int(i[1])), int(i[2]), (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(cimg, (int(i[0]), int(i[1])), 2, (0, 0, 255), 3)


cv2.imshow('detected circles', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
