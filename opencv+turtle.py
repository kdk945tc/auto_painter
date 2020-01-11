import cv2
import os
import numpy as np
import pyautogui as pg
import turtle


def get_img(img_path=""):
    cv_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
    return cv_img


class DrawPic:
    def __init__(self, image, resizedH=200, step=4):
        self.image = image
        self.resizedH = resizedH
        # print(image.shape)
        self.resizedW = int(resizedH * (image.shape[1] / image.shape[0]))
        if self.resizedW >= 300:
            self.resizedW = 300
            self.resizedH = int(self.resizedW * (image.shape[0] / image.shape[1]))
        self.step = step
        self.zoom = 2.0
        self.upLeft = [300, 300]
        self.route = []
        self.process()

    def process(self):
        self.route = []
        resized = cv2.resize(self.image, (self.resizedW, self.resizedH), interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 30, 80)
        cv2.imshow('preview', edges)
        for i in range(len(edges)):
            for j in range(len(edges[0])):
                distance = 0
                if edges[i][j]:
                    cursorY = i
                    cursorX = j
                    subroute = [(j, i)]
                    while edges[cursorY][cursorX]:
                        distance += 1
                        if not distance % self.step:
                            subroute.append((cursorX, cursorY))
                        edges[cursorY][cursorX] = 0
                        if cursorX < len(edges[0]) - 1:
                            if edges[cursorY][cursorX + 1]:
                                cursorX += 1
                                continue
                        if cursorX < len(edges[0]) - 1 and cursorY < len(edges) - 1:
                            if edges[cursorY + 1][cursorX + 1]:
                                cursorX += 1
                                cursorY += 1
                                continue
                        if cursorY < len(edges) - 1:
                            if edges[cursorY + 1][cursorX]:
                                cursorY += 1
                                continue
                        if cursorX > 1 and cursorY < len(edges) - 1:
                            if edges[cursorY + 1][cursorX - 1]:
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
                        if cursorX > 1 and cursorY < len(edges) - 1:
                            if edges[cursorY + 1][cursorX - 1]:
                                cursorX -= 1
                                cursorY += 1
                                continue
                        if distance >= self.step:
                            self.route.append(subroute)
                        break
        if not self.route:
            pg.alert(text='生成路径笔画数为0, 请检查图片', title='路径规划完成', button='退出')
            return 0

        else:
            startrawing = pg.confirm(text='生成路径笔画数为'+str(len(self.route)), title='路径规划完成', buttons=['开始绘制', '取消绘制'])
            cv2.destroyAllWindows()
            if startrawing == "取消绘制":
                self.route = []
                return 0

        routeF = []
        routeB = []
        for i, j in enumerate(self.route):
            routeF.append([i, j])
            routeB.append([i, j[::-1]])
        # print("total stroke:", len(self.route))
        tail = self.route[0][0]
        self.route = []

        while len(self.route) < len(routeF):
            distance2 = self.resizedH ** 2 + self.resizedW ** 2
            forward = True
            index = 0
            for i in range(len(routeF)):
                if not routeF[i][1] or not routeB[i][1]:
                    continue
                else:
                    dis02 = (tail[0]-routeF[i][1][0][0])**2+(tail[1]-routeF[i][1][0][1])**2
                    dis12 = (tail[0]-routeB[i][1][0][0])**2+(tail[1]-routeB[i][1][0][1])**2
                    if distance2 >= dis02:
                        distance2 = dis02
                        index = i
                        forward = True
                    if distance2 >= dis12:
                        distance2 = dis12
                        index = i
                        forward = False

            # print(index, routeF[index][1], routeB[index][1])
            if forward:
                self.route.append(routeF[index][1])
                tail = routeF[index][1][-1]
                routeF[index][1] = []
            else:
                self.route.append(routeB[index][1])
                tail = routeB[index][1][-1]
                routeB[index][1] = []

    def locate(self):
        top = pg.locateOnScreen('loc/top.png')
        bottom = pg.locateOnScreen('loc/bottom.png')
        if top is not None:
            self.upLeft = (top.left + top.width, top.top + top.height)
            if bottom is not None:
                self.zoom = (bottom.top - top.top) / self.resizedH/1.5
                if self.resizedW * self.zoom >= (bottom.top - top.top) * 1.5:
                    self.zoom = (bottom.top - top.top) * 1.5/self.resizedW
            if self.resizedW * self.zoom >= 600:
                self.zoom = 600 / self.resizedW
            return 1
        return 0

    def draw(self, game=False):
        # game:True(drawing in a game); False:(practising)
        if not self.route:
            return 0
        while not self.locate() and game:
            option = pg.confirm(text="未检测到游戏窗口", title='未检测到窗口', buttons=['重试', '取消'])
            if option == "重试":
                continue
            else:
                return 0
        for stroke in self.route:
            key = cv2.waitKey(0)
            if key == 27:
                return 0
            turtle.goto(stroke[0][0] * self.zoom - 200,300 - stroke[0][1] * self.zoom)
            turtle.pendown()
            for step in stroke:
                turtle.goto(step[0] * self.zoom - 200,300 - step[1] * self.zoom)

            turtle.penup()
        pg.alert(text='图片绘制完成, 共计'+str(len(self.route))+"笔", title='绘制完成', button='ok')
        return 1


if __name__ == '__main__':
    warning = "请将图片文件拖入文件夹img \n点击重新检测开始规划路径\n 规划完成后图片会被删除!"
    option = pg.confirm(text=warning, title='文件缺失', buttons=['开始绘制', '退出'])
    if option == "游戏中绘制":
        game = True
    else:
        game = False
    while True:
        turtle.penup()
        turtle.clear()
        photos = os.listdir("img")
        if photos:
            a = DrawPic(get_img('img/' + photos[0]))
            a.draw(game)
            for i in photos:
                os.remove('img/' + i)
        else:
            option = pg.confirm(text=warning, title='文件缺失', buttons=['开始绘制', '退出'])
            if option == "退出":
                break
            elif option == "游戏中绘制":
                game = True
            else:
                game = False
