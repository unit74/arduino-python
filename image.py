import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk

def drawLine(src):
    src = src.copy()
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    dst = cv2.filter2D(gray, -1, kernel)
    canny = cv2.Canny(dst, 500, 270, apertureSize=5, L2gradient=True)
    lines = cv2.HoughLines(canny, 1, np.pi / 180, 140, srn=1, stn=2, min_theta=0, max_theta=np.pi)
    scale = src.shape[0] + src.shape[1]

    miny = scale
    angle = 0
    cnt = 0
    if lines is not None:
        for i in lines:
            for rho, theta in i:
                a, b = np.cos(theta), np.sin(theta)
                x, y = a * rho, b * rho

                x1 = int(x + scale * -b)
                y1 = int(y + scale * a)
                x2 = int(x - scale * -b)
                y2 = int(y - scale * a)

                y3 = ((y1 + y2) / 2) - ((src.shape[1] / 2) / np.tan(theta))
                if miny > y3:
                    miny = y3
                angle = angle + abs(theta)
                cnt = cnt + 1

                cv2.line(src, (x1, y1), (x2, y2), (0, 0, 255), 5)
        angle = angle / cnt

    return src, miny, angle

def cv2tk(src):
    img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    return ImageTk.PhotoImage(image=img)