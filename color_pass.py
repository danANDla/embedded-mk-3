import numpy as np
import cv2

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

path = "/home/danandla/BOTAY/embedded/mk3/generatedPasswords/"
password = 3412


def show_color_codes():
    for i in color_id.keys():
        print("(" + str(i) + ") " + color_id[i])


def color_rate(frame, rect, color):
    color_lower, color_upper = color
    rect_start, rect_end = rect

    rect_size = (rect_end[0] - rect_start[0]) * (rect_end[1] - rect_start[1])

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_frame = hsv_frame[rect_start[1]:rect_end[1] + 1, rect_start[0]:rect_end[0] + 1]
    mask_color = cv2.inRange(mask_frame, color_lower, color_upper)
    rate = np.count_nonzero(mask_color) / (rect_size)
    return rate


def process(frame, password):
    rect_size = 60
    gap = 40
    height, width, channels = frame.shape
    if (rect_size * 4 + gap * 3 > width):
        rect_size = 100

    thickness = 2

    rects_coords = []
    start_point = (int((width - rect_size * 4 - gap * 3) / 2), int((height - rect_size) / 2))
    end_point = (rect_size + int((width - rect_size * 4 - gap * 3) / 2), height - int((height - rect_size) / 2))
    rects_coords.append(tuple((start_point, end_point)))
    for i in range(3):
        t = end_point[0] + gap
        start_point = (t, int((height - rect_size) / 2))
        end_point = (t + rect_size, height - int((height - rect_size) / 2))
        rects_coords.append(tuple((start_point, end_point)))

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.7
    access = [0, 0, 0, 0]

    # colors_password = [color_id[i] for i in password]
    colors_borders = get_borders()
    for i in range(4):
        org = rects_coords[i][0]
        rate = color_rate(frame, rects_coords[i], colors_borders[password[i]])
        if rate > 0.9:
            access[i] = 1
            color = color_codes[password[i]]
            text = cv2.putText(frame, password[i], org, font, fontScale, color, thickness, cv2.LINE_AA)
        else:
            access[i] = 0
            color = color_codes["grey"]
            text = cv2.putText(frame, ' wrong ', org, font, fontScale, color, thickness, cv2.LINE_AA)
        cv2.rectangle(frame, rects_coords[i][0], rects_coords[i][1], color, thickness)

    res_org = (int(width / 2 - 30), int(height - 30))
    if np.average(access) == 1:
        color = color_codes["green"]
        for i in range(4):
            cv2.rectangle(frame, rects_coords[i][0], rects_coords[i][1], color, thickness)
        text = cv2.putText(frame, ' access ', res_org, font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        color = color_codes["red"]
        text = cv2.putText(frame, ' denied ', res_org, font, fontScale, color, thickness, cv2.LINE_AA)
    frame = text
    return frame


def application():
    print('Press 4 to Quit the Application\n')
    # Open Default Camera
    cap = cv2.VideoCapture(0)  # gstreamer_pipeline(flip_method=4), cv2.CAP_GSTREAMER)

    # colors_password = []
    # for c in map(int, str(password)):
    #     colors_password.append()
    colors_password = [color_id[i] for i in map(int, str(password))]
    print(colors_password)
    while (cap.isOpened()):
        # Take each Frame
        ret, frame = cap.read()

        # Flip Video vertically (180 Degrees)
        # frame = cv2.flip(frame, 180)

        invert = process(frame, colors_password)

        # Show video
        # cv2.imshow('Cam', frame)
        cv2.imshow('Inverted', invert)

        # Exit if "4" is pressed
        k = cv2.waitKey(1) & 0xFF
        if k == 52:  # ord 4
            # Quit
            print('Good Bye!')
            break
    # Release the Cap and Video
    cap.release()
    cv2.destroyAllWindows()


def get_borders():
    pink_lower = np.array([128, 0, 141])
    pink_upper = np.array([163, 255, 255])
    pink = (pink_lower, pink_upper)

    red_lower = np.array([0, 92, 89])
    red_upper = np.array([15, 255, 255])
    red = (red_lower, red_upper)

    yellow_lower = np.array([25, 90, 84])
    yellow_upper = np.array([40, 255, 255])
    yellow = (yellow_lower, yellow_upper)

    green_lower = np.array([35, 90, 84])
    green_upper = np.array([77, 255, 255])
    green = (green_lower, green_upper)

    blue_lower = np.array([47, 164, 205])
    blue_upper = np.array([129, 255, 255])
    blue = (blue_lower, blue_upper)

    white_lower = np.array([18, 0, 151])
    white_upper = np.array([44, 75, 255])
    white = (white_lower, white_upper)

    ret = {
        "pink": pink,
        "red": red,
        "yellow": yellow,
        "green": green,
        "blue": blue,
        "white": white
    }

    return ret


def generate_template():
    codes = [1, 2, 3, 4, 5, 6]

    rect_size = 100
    width = rect_size * 6
    height = rect_size
    img = np.zeros((height, width, 3), dtype="uint8")

    point = 0
    for i in codes:
        cv2.rectangle(img, (point, 0), (point + rect_size, height), color_codes[color_id[i]], -1)
        print(color_codes[color_id[i]])
        point += rect_size

    cv2.imwrite(path + "temp1.jpg", img)

    while (True):
        cv2.imshow("generated", img)
        k = cv2.waitKey(1) & 0xFF
        if k == 52:  # ord 4
            cv2.destroyWindow("generated")
            return True


def generate_img(new_pass: int):
    if (new_pass > 6666):
        print("bad pass, numbers must be in interval 1-6")
        return False
    codes = []
    for c in map(int, str(new_pass)):
        if c > 6 or c < 1:
            print("bad pass, numbers must be in interval 1-6")
            return False
        else:
            codes.append(c)

    rect_size = 100
    width = rect_size * 4
    height = rect_size * 3
    img = np.zeros((height, width, 3), dtype="uint8")

    point = 0
    for i in codes:
        cv2.rectangle(img, (point, 0), (point + rect_size, height), color_codes[color_id[i]], -1)
        point += rect_size

    cv2.imwrite(path + "pass1.jpg", img)

    while (True):
        cv2.imshow("generated", img)
        k = cv2.waitKey(1) & 0xFF
        if k == 52:  # ord 4
            cv2.destroyWindow("generated")
            return True


def print_divider():
    print("--------------------------")


def main():
    global password
    while True:
        print_divider()
        print('(1) app')
        print('(2) set password')
        print('(0) quit')
        a = input()
        try:
            a = int(a)
        except ValueError:
            print('wrong command')
            continue
        if a == 1:
            if password == -1:
                print("password is unset, set it first")
                continue
            application()
        elif a == 2:
            print("enter password")
            show_color_codes()
            new_pass = int(input())
            while not generate_img(new_pass):
                new_pass = int(input())
            password = new_pass
        elif a == 0:
            break
        else:
            print('wrong command')


if __name__ == "__main__":
    main()
