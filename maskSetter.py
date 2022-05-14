import cv2
import numpy as np

color_codes = {
    "pink": (147, 20, 255),
    "red": (0, 0, 255),
    "yellow": (0, 255, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "white": (255, 255, 255),
    "grey": (30, 30, 30)
}

color_id = {
    1: "pink",
    2: "red",
    3: "yellow",
    4: "green",
    5: "blue",
    6: "white"
}

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.7
path = "/home/danandla/BOTAY/embedded/mk3/samples/photo/c1.jpg"
cv2.namedWindow("TrackedBars")
cv2.resizeWindow("TrackedBars", 640, 240)

img = cv2.imread(path)
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def print_borders(color, vals):
    # print(color + "_lower = np.array([" + str(vals[0][0]) + ", " + str(vals[0][1]) + ", " + str(vals[0][2]) + "])")
    # print(color + "_upper = np.array([" + str(vals[1][0]) + ", " + str(vals[1][1]) + ", " + str(vals[1][2]) + "])")
    s = (color + "_lower = np.array([" + str(vals[0][0]) + ", " + str(vals[0][1]) + ", " + str(vals[0][2]) + "])\n" +
         color + "_upper = np.array([" + str(vals[1][0]) + ", " + str(vals[1][1]) + ", " + str(vals[1][2]) + "])\n" +
         color + " = (" + color + "_lower, " + color + "_upper)\n")
    return s


def on_trackbar(val):
    hue_min = cv2.getTrackbarPos("Hue Min", "TrackedBars")
    hue_max = cv2.getTrackbarPos("Hue Max", "TrackedBars")
    sat_min = cv2.getTrackbarPos("Sat Min", "TrackedBars")
    sat_max = cv2.getTrackbarPos("Sat Max", "TrackedBars")
    val_min = cv2.getTrackbarPos("Val Min", "TrackedBars")
    val_max = cv2.getTrackbarPos("Val Max", "TrackedBars")

    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])

    return lower, upper


cv2.createTrackbar("Hue Min", "TrackedBars", 0, 179, on_trackbar)
cv2.createTrackbar("Hue Max", "TrackedBars", 179, 179, on_trackbar)
cv2.createTrackbar("Sat Min", "TrackedBars", 0, 255, on_trackbar)
cv2.createTrackbar("Sat Max", "TrackedBars", 255, 255, on_trackbar)
cv2.createTrackbar("Val Min", "TrackedBars", 0, 255, on_trackbar)
cv2.createTrackbar("Val Max", "TrackedBars", 255, 255, on_trackbar)

# Show some stuff
on_trackbar(0)
work = img.copy()
ans = ""

while True:
    print("(1) full setup")
    print("(2) separate setup")
    print("(0) quit")
    mode = int(input())
    if mode == 1:
        for i in color_id.values():
            cv2.putText(work, i, (20, 20), font, fontScale, color_codes[i], 2, cv2.LINE_AA)
            while True:
                vals = on_trackbar(0)
                imgMASK = cv2.inRange(imgHSV, vals[0], vals[1])
                cv2.imshow("Output1", work)
                cv2.imshow("Mask", imgMASK)
                k = cv2.waitKey(1) & 0xFF
                if k == 53:  # ord 5
                    work = img.copy()
                    ans += print_borders(i, vals)
                    ans += "\n"
                    break
    elif mode == 2:
        col = str(input())
        cv2.putText(work, col, (20, 20), font, fontScale, color_codes[col], 2, cv2.LINE_AA)
        while True:
            vals = on_trackbar(0)
            imgMASK = cv2.inRange(imgHSV, vals[0], vals[1])
            cv2.imshow("Output1", work)
            cv2.imshow("Mask", imgMASK)
            k = cv2.waitKey(1) & 0xFF
            if k == 53:  # ord 5
                work = img.copy()
                sep = print_borders(col, vals)
                print(sep)
                break
    elif mode == 0:
        cv2.destroyAllWindows()
        break
