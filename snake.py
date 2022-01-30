#!/usr/bin/python3
import pygame
from pygame.locals import *
import random
import os

class PixelManager():
    """
        描述：像素管理器
        包含的方法：
        __init__(screen, screen_size, map_size)
        add_pixel(pos_x, pos_y, color, force_write = False)
        remove_pixel(pos_x, pos_y)
        query(pos_x, pos_y)
        clear()
        update()
    """
    screen = None                       #显示层
    pixHeight = 0                       #像素高度
    pixWidth = 0                        #像素宽度
    pix_map = []                         #像素地图
    map_size = ()
    def __init__(self, display_surface, screen_size, map_size):
        """
            描述：构造器
            原型： __init__(screen, screen_size, map_size)
            说明：
                screen：pygame窗口
                screen_size：窗口大小
                map_size：映射后的地图大小
            返回值：无返回值
            备注：PixelManager使用原点在左上角的pygame坐标系
        """
        self.screen = display_surface
        self.pixWidth = screen_size[0] // map_size[0]
        self.pixHeight = screen_size[1] // map_size[1]
        self.map_size = map_size
        self.screen.fill((255, 255, 255))
        for i in range(self.map_size[0]):
            self.pix_map.append([])
            for j in range(self.map_size[1]):
                self.pix_map[i].append([])
                self.pix_map[i][j].append(False)
                self.pix_map[i][j].append((255, 255, 255))
        self.update()

    def update(self):
        """
            描述：更新像素点状态
            原型 update()
            说明：无
            返回值：无
            备注：该方法不会刷新窗口显示
        """
        self.screen.fill((255, 255, 255))
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                if self.pix_map[i][j][0]:
                    pygame.draw.rect(self.screen, self.pix_map[i][j][1], (i * self.pixHeight, j * self.pixWidth, self.pixHeight, self.pixWidth), 0)

    def add_pixel(self, pos_x, pos_y, color, force_write = False):
        """
            描述：添加像素
            原型:add_pixel(pos_x, pos_y, color, force_write = False)
            说明：
                pos_x：像素横坐标
                pos_y：像素纵坐标
                color：像素颜色（RGB元组）
                force_write：强制写入， 默认为False
            返回值：写入成功为True, 失败为False
            备注：pygame坐标系
        """
        if self.pix_map[pos_x][pos_y][0] and not force_write:
            return False
        self.pix_map[pos_x][pos_y][0] = True
        self.pix_map[pos_x][pos_y][1] = color
        return True

    def remove_pixel(self, pos_x, pos_y):
        """
            描述：移除像素
            原型：remove_pixel(pos_x, pos_y)
            说明：
                pos_x：像素横坐标
                pos_y：像素纵坐标
            返回值：移除成功为True, 失败为False
            备注：pygame坐标系
        """
        if not self.pix_map[pos_x][pos_y][0]:
            return False
        self.pix_map[pos_x][pos_y][0] = False
        self.pix_map[pos_x][pos_y][1] = (255, 255, 255)
        return True

    def query(self, pos_x, pos_y):
        """
            描述：查询特定坐标下的像素点
            原型：query(pos_x, pos_y)
            说明：
                pos_x：像素横坐标
                pos_y：像素纵坐标
            返回值：一个元组， 索引0为布尔值， 表示该坐标有无像素
                    有则为True, 无则为False；索引1为像素颜色（RGB元组）
            备注：pygame坐标系
        """
        return self.pix_map[pos_x][pos_y][0], self.pix_map[pos_x][pos_y][1]

    def clear(self):
        """
            描述：清除所有像素
            原型：clear()
            说明：无
            返回值：无
        """
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                self.pix_map[i][j][0] = False
                self.pix_map[i][j][1] = (255, 255, 255)


##贪吃蛇游戏逻辑类
##调试通过
class GameSnake():
    """
        描述：贪吃蛇游戏类
        包含的方法：
            __init__(pix_map, map_size)
            gen_food()
            update()
            move_up(holding)
            move_down(holding)
            move_left(holding)
            move_right(holding)
            fun_key(holding)
            pause(holding)
            resume(holding)
            draw()
    """
    keyDown = False
    over = False
    COLOR_FOOD = (255, 255, 0)
    COLOR_BODY = (150, 150, 150)
    COLOR_HEAD = (0, 0, 255)
    pix_map = None                       #像素管理器的实例
    map_size = None
    food = None
    paused = False
    snake = []
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    direction = LEFT
    moved = False
    def __init__(self, pix_map, map_size):
        """
            描述：构造器
            原型：__init__(pix_map, map_size)
            说明：
                pix_map：像素管理器的实例
                map_size：像素地图的大小
            返回值：无
            备注：无
        """
        assert map_size[0] > 21 and map_size[1] > 21
        self.pix_map = pix_map
        self.map_size = map_size
        self.snake.append((20, 20))
        self.snake.append((21, 20))
        assert self.gen_food()
        self.update()
    
    def gen_food(self):
        """
            描述：生成食物
            原型：gen_food()
            说明：无
            返回值：若生成成功为True, 失败为False
            备注：无
        """
        pos = []
        maxn = self.map_size[0] * self.map_size[1] - 1
        choice = random.randint(0, maxn)
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                pos.append((i, j))
        while not self.pix_map.add_pixel(pos[choice][0], pos[choice][1], self.COLOR_FOOD):
            pos.remove((pos[choice][0], pos[choice][1]))
            maxn -= 1
            if maxn < 0:
                return False
            choice = random.randint(0, maxn)
        self.food = (pos[choice][0], pos[choice][1])
        return True

    def update(self):
        """
        描述：更新游戏状态
            原型：update()
            说明：无
            返回值：游戏的得分情况（单次， 非累积）。
                    若本次游戏结束， 则为-1
            备注：游戏的主逻辑
        """
        self.moved = True
        head = [self.snake[0][0], self.snake[0][1]]
        if self.over or self.paused:
            return 0
        if self.direction == self.UP:
            head[1] -= 1
        elif self.direction == self.DOWN:
            head[1] += 1
        elif self.direction == self.LEFT:
            head[0] -= 1
        else:
            head[0] += 1
        head[0] += self.map_size[0]
        head[0] %= self.map_size[0]
        head[1] += self.map_size[1]
        head[1] %= self.map_size[1]
        color = self.pix_map.query(head[0], head[1])[1]
        if self.pix_map.query(head[0], head[1])[0]:
            if color == self.COLOR_BODY:
                self.over = True
                return -1
            else:
                self.snake.insert(0, (head[0], head[1]))
                self.pix_map.remove_pixel(head[0], head[1])
                self.draw()
                self.gen_food()
                self.pix_map.update()
                return 1
        else:
            i = len(self.snake) - 1
            while i > 0:
                self.snake[i] = self.snake[i - 1]
                i -= 1
            self.snake[0] = (head[0], head[1])
        self.draw()
        self.pix_map.update()
        return 0

    def move_up(self, holding):
        """
            描述：“上”键响应
            原型：move_up(holding)
            说明：
                holding：按键状态， 按下为True, 弹起为False
            返回值：响应成功为True, 失败为False
        """
        if self.direction != self.UP and self.direction != self.DOWN and self.moved and not self.paused and not self.over and holding:
            self.direction = self.UP
            self.moved = False
            return True
        return False

    def move_down(self, holding):
        """
            描述：“下”键响应
            原型：move_down(holding)
            说明：
                holding：按键状态， 按下为True, 弹起为False
            返回值：响应成功为True, 失败为False
        """
        if self.direction != self.DOWN and self.direction != self.UP and self.moved and not self.paused and not self.over and holding:
            self.direction = self.DOWN
            self.moved = False
            return True
        return False

    def move_left(self, holding):
        """
            描述：“左”键响应
            原型：move_left(holding)
            说明：
                holding：按键状态， 按下为True, 弹起为False
            返回值：响应成功为True, 失败为False
        """
        if self.direction != self.LEFT and self.direction != self.RIGHT and self.moved and not self.paused and not self.over and holding:
            self.direction = self.LEFT
            self.moved = False
            return True
        return False

    def move_right(self, holding):
        """
            描述：“右”键响应
            原型：move_right(holding)
            说明：
                holding：按键状态， 按下为True, 弹起为False
            返回值：响应成功为True, 失败为False
        """
        if self.direction != self.RIGHT and self.direction != self.LEFT and self.moved and not self.paused and not self.over and holding:
            self.direction = self.RIGHT
            self.moved = False
            return True
        return False

    def fun_key(self, holding):
        """
            描述：空格响应
            原型：fun_key(holding)
            说明：
                holding：按键状态， 按下为True, 弹起为False
            返回值：响应成功为True, 失败为False
        """
        return False

    def pause(self):
        """
            描述：暂停
            原型：pause()
            说明：无
            返回值：成功暂停游戏运行为True，失败或已暂停为False
        """
        if not self.paused and not self.over:
            self.paused = True
            return True
        return False

    def resume(self):
        """
            描述：继续
            原型：resume()
            说明：无
            返回值：成功使游戏继续运行为True，失败或正在运行为False
        """
        if self.paused and not self.over:
            self.paused = False
            return True
        return False

    def draw(self):
        """
            描述：绘图
            原型：draw()
            说明：无
            返回值：无
            备注：绘制游戏画面
        """
        self.pix_map.clear()
        for item in self.snake:
            if item == self.snake[0]:
                assert self.pix_map.add_pixel(item[0], item[1], self.COLOR_HEAD)
            else:
                assert self.pix_map.add_pixel(item[0], item[1], self.COLOR_BODY)
        self.pix_map.add_pixel(self.food[0], self.food[1], self.COLOR_FOOD)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("snake")
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    pix = PixelManager(screen, (800, 800), (40, 40))
    myGame = GameSnake(pix, (40, 40))
    score = 0
    smallFont = pygame.font.Font(None, 32)
    largeFont = pygame.font.Font(None, 60)
    finished = False
    while True:
        status = myGame.update()
        if status < 0:
            imgText = largeFont.render("GAME OVER", True, (0, 0, 0))
            screen.blit(imgText, (265, 370))
            finished = True
        elif not finished:
            score += status
            imgText = smallFont.render("score:" + str(score), True, (0, 0, 0))
            screen.blit(imgText, (0, 0))
        if not pygame.display.get_active() and not finished:
            myGame.pause()
            imgText = largeFont.render("PAUSED", True, (0, 0, 0))
            screen.blit(imgText, (310, 370))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    print("move_up(True):" + str(myGame.move_up(True)))
                if event.key == K_DOWN:
                    print("move_down(True):" + str(myGame.move_down(True)))
                if event.key == K_LEFT:
                    print("move_left(True):" + str(myGame.move_left(True)))
                if event.key == K_RIGHT:
                    print("move_right(True):" + str(myGame.move_right(True)))
                if event.key == K_ESCAPE:
                    if myGame.pause():
                        imgText = largeFont.render("PAUSED", True, (0, 0, 0))
                        screen.blit(imgText, (310, 370))    
                    print("pause():" + str(myGame.pause()))
                if event.key == K_SPACE:
                    print("fun_key(True):" + str(myGame.fun_key(True)))
                    print("resume():" + str(myGame.resume()))
            if event.type == KEYUP:
                if event.key == K_UP:
                    print("move_up(False):" + str(myGame.move_up(False)))
                if event.key == K_DOWN:
                    print("move_down(False):" + str(myGame.move_down(False)))
                if event.key == K_LEFT:
                    print("move_left(False):" + str(myGame.move_left(False)))
                if event.key == K_RIGHT:
                    print("move_right(False):" + str(myGame.move_right(False)))
                if event.key == K_SPACE:
                    print("fun_key(False):" + str(myGame.fun_key(False)))
        pygame.display.update()
        clock.tick(12)
    
