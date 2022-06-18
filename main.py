from threading import Thread
from tkinter import *
from tkinter import messagebox
from tkinter import font
from time import *
from esp32 import *
from image import *
from stack import *

def form(name = ""):
    for wg in root.place_slaves():
        wg.destroy()

    iFont = font.Font(family="맑은 고딕", size=20)

    root.geometry("1230x620")
    if name == "중심점 맞추기":
        root.geometry("420x620")
        Btn = Button(root, text=name, font=iFont, command=init)
        Btn.place(x=10, y=10, width=400, height=400)
    elif name == "시작":
        root.geometry("420x620")
        Btn = Button(root, text=name, font=iFont, command=escape)
        Btn.place(x=10, y=10, width=400, height=400)
    elif name == "지도":
        global canvas
        canvas = Canvas(root, width=400, height=400, bg="white")
        canvas.place(x=10, y=10)

    Btn = Button(root, text="종료", font=iFont, command=exit)
    Btn.place(x=10, y=420, width=400, height=190)

    global cam_label
    cam_label = Label(root)
    cam_label.place(x=420, y=10, width=800, height=600)

def leftright(angle):
    if 1.545 < angle and angle < 1.555:
        return 1
    elif angle < 1.545:
        cam.left()
    else:
        cam.right()
    return 0

def updown(miny):
    if 90 < miny and miny < 110:
        return 2
    elif miny < 90:
        cam.go()
    else:
        cam.back()
    return 1

def initCamUpdate():
    state = 0
    cnt = 0
    while True:
        src, miny, angle = drawLine(cam.getJPG())

        if angle == 0:
            cam.rightOne()
            sleep(1)
        elif state == 0: # 좌우 설정
            state = leftright(angle)
        elif state == 1:
            state = updown(miny)
        elif state == 2:
            if cnt == 2:
                break
            cnt += 1
            state = 0
            cam.rightOne()
            sleep(1)

        global img
        img = cv2tk(src)
        cam_label.config(image=img)

    messagebox.showinfo("ALPHACAR", "중심점 맞추기가 완료되었습니다.")
    form("시작")

def move(next):
    x = next[0] - cam.x
    y = next[1] - cam.y

    # 북 동 남 서 -> (0, 1, 2, 3) // 안움직여도 되면 -1
    if abs(x) > 1 or abs(y) > 1:
        cam.log.pop()
        move(cam.log.peek())

    if x == 0 and y == 0:
        direction = -1
    if x == 1:
        direction = 2
    elif x == -1:
        direction = 0
    elif y == 1:
        direction = 1
    elif y == -1:
        direction = 3

    if direction != -1:
        turn(direction)
        cam.goOne()
        sleep(1)
        cam.x = next[0];
        cam.y = next[1];

def turn(nextDirection):
    way = nextDirection - cam.direction

    if way == 3:
        way = -1
    elif way == -3:
        way = 1

    if abs(way) == 2:
        cam.rightOne()
        sleep(1)
        cam.rightOne()
        sleep(1)
    elif way == -1:
        cam.leftOne()
        sleep(1)
    elif way == 1:
        cam.rightOne()
        sleep(1)

    cam.direction = nextDirection

def intTobin(n):
    res = ""
    a = 8

    for i in range(4):
        if n - a >= 0:
            res += "1"
            n -= a
        else:
            res += "0"
        a = int(a / 2)

    return res

def drawMap(map):
    canvas.delete("all")
    size = len(map)

    x = cam.y * (400 / size)
    y = cam.x * (400 / size)
    canvas.create_oval(x, y, x + (400 / size), y + (400 / size), fill='red')
    for i in range(size):
        for j in range(size):
            wall = intTobin(map[i][j])
            weight = [[0, 0], [400 / size, 0], [400 / size, 400 / size], [0, 400 / size], [0, 0]]
            for k in range(len(wall)):
                if wall[k] == "1":
                    x = j * (400 / size)
                    y = i * (400 / size)
                    canvas.create_line(x + weight[k][0], y + weight[k][1], x + weight[k + 1][0], y + weight[k + 1][1], fill="black")
    root.update()

def escapeCamUpdate():
    go_list = Stack()
    MAP_SIZE = 3
    cam.x = MAP_SIZE
    cam.y = MAP_SIZE

    my_map = []
    visit_map = []
    for i in range((MAP_SIZE * 2) + 1):
        row1 = []
        row2 = []
        for j in range((MAP_SIZE * 2) + 1):
            row1.append(0)
            row2.append(0)
        my_map.append(row1)
        visit_map.append(row2)

    visit_map[cam.x][cam.y] += pow(2, 3 - cam.direction)
    visit_map[cam.north()[0]][cam.north()[1]] += pow(2, 3 - ((cam.direction + 2) % 4))
    go_list.push((cam.x, cam.y, cam.direction))

    while not go_list.isEmpty():
        go_list.print()
        current = go_list.peek()
        go_list.pop()

        x = current[0]
        y = current[1]
        direction = current[2]
        cam.log.push((x, y))

        move((x, y))
        turn(direction)

        src, miny, angle = drawLine(cam.getJPG())
        global img
        img = cv2tk(src)
        cam_label.config(image=img)
        root.update()

        if intTobin(visit_map[x][y])[cam.westDirection()] == '0':
            go_list.push((x, y, cam.westDirection()))
            visit_map[x][y] += pow(2, 3 - cam.westDirection())
            visit_map[cam.west()[0]][cam.west()[1]] += pow(2, 3 - ((cam.westDirection() + 2) % 4))

        if intTobin(visit_map[x][y])[cam.eastDirection()] == '0':
            go_list.push((x, y, cam.eastDirection()))
            visit_map[x][y] += pow(2, 3 - cam.eastDirection())
            visit_map[cam.east()[0]][cam.east()[1]] += pow(2, 3 - ((cam.eastDirection() + 2) % 4))

        if angle == 0: # 벽이 없다.
            if intTobin(visit_map[cam.north()[0]][cam.north()[1]])[direction] == '0': # 이동하는 지역에 같은 방향의 지역이 미탐색 지역이라면
                go_list.push((cam.north()[0], cam.north()[1], direction))
                cam.x, cam.y = cam.north()
                visit_map[cam.x][cam.y] += pow(2, 3 - direction)
                visit_map[cam.north()[0]][cam.north()[1]] += pow(2, 3 - ((direction + 2) % 4))
                cam.x, cam.y = cam.south()
        else:
            my_map[x][y] += pow(2, 3 - direction)
            my_map[cam.north()[0]][cam.north()[1]] += pow(2, 3 - ((direction + 2) % 4))

            drawMap(my_map)

            state = 0
            while True:
                src, miny, angle = drawLine(cam.getJPG())
                img = cv2tk(src)
                cam_label.config(image=img)
                root.update()

                if state == 0:  # 좌우 설정
                    state = leftright(angle)
                elif state == 1:
                    state = updown(miny)
                elif state == 2:
                    break

            img = cam.getJPG()
            (b, g, r) = img[400, 200]

            if r > 200: # 도착점
                break


    messagebox.showinfo("ALPHACAR", "미로 탐색이 완료되었습니다.")



def print_map(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            print(m[i][j], end = ' ')
        print()
    print()

def init():
    form()
    initCam = Thread(target=initCamUpdate)
    initCam.start()

def escape():
    form("지도")
    escapeCam = Thread(target=escapeCamUpdate)
    escapeCam.start()

def exit():
    root.destroy()
    quit()

if __name__ == "__main__":
    global cam
    cam = esp32(url="http://172.20.10.7/")
    root = Tk()
    root.title("ALPHACAR")
    root.resizable(False,False)

    form("시작")

    root.mainloop()