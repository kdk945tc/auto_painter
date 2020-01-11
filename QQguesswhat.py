import cv2
import numpy as np
import pyautogui as pg
H = 300
W = 400

HEIGHT = 120
WIDTH = 160

startX = 300
startY = 300

img = cv2.imread('img/test3.png')
resized = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 30, 80)
edgesBK = edges
print(edges)

draw = False

while 1:
    cv2.imshow('gray', edges)
    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == 13:
        draw = True
        break

cv2.destroyAllWindows()


if draw:
    stroke = 0
    print(len(edges))
    print(len(edges[0]))
    for i in range(len(edges)):
        for j in range(len(edges[0])):
            distance = 0
            if edges[i][j]:
                stroke += 1
                cursorY = i
                cursorX = j
                pg.mouseDown(startX + cursorX * H / HEIGHT, startY + cursorY * W / WIDTH, button='left')
                while edges[cursorY][cursorX]:
                    distance += 1
                    if not distance % (HEIGHT/30):
                        pg.dragTo(startX + cursorX * H / HEIGHT, startY + cursorY * W / WIDTH, button='left')
                    # print(cursorY,cursorX)
                    edges[cursorY][cursorX] = 0
                    if cursorX < len(edges[0])-1:
                        if edges[cursorY][cursorX+1]:
                            cursorX += 1
                            continue
                    if cursorX < len(edges[0])-1 and cursorY < len(edges)-1:
                        if edges[cursorY+1][cursorX + 1]:
                            cursorX += 1
                            cursorY += 1
                            continue
                    if cursorY < len(edges)-1:
                        if edges[cursorY+1][cursorX]:
                            cursorY += 1
                            continue
                    if cursorX > 1 and cursorY < len(edges)-1:
                        if edges[cursorY+1][cursorX - 1]:
                            cursorX -= 1
                            cursorY += 1
                            continue
                    if cursorX > 1:
                        if edges[cursorY][cursorX - 1]:
                            cursorX -= 1
                            continue
                    if cursorX > 1 and cursorY > 1:
                        if edges[cursorY - 1][cursorX - 1]:
                            cursorX -= 1
                            cursorY -= 1
                            continue
                    if cursorY > 1:
                        if edges[cursorY - 1][cursorX]:
                            cursorY -= 1
                            continue
                    if cursorX > 1 and cursorY < len(edges) -1:
                        if edges[cursorY + 1][cursorX - 1]:
                            cursorX -= 1
                            cursorY += 1
                            continue
                    pg.dragTo(startX + cursorX * H / HEIGHT, startY + cursorY * W / WIDTH, button='left')
                    break
    print(edges)
    print(stroke)


