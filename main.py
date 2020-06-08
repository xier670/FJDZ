import pygame                #导入pygame模块
from pygame.locals import *  #导入pygame库中的一些常量
from sys import exit         #导入sys库中的exit函数
import random
import codecs

#设置游戏屏幕大小
SCREEN_WIDTH=480
SCREEN_HEIGHT=800

#初始化pygame
pygame.init()
#设置游戏界面大小
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#设置游戏界面标题
pygame.display.set_caption("彩图版飞机大战")
#设置游戏界面图标位于界面标题前的
picture=pygame.image.load('resources/image/picture.ico').convert_alpha()
pygame.display.set_icon(picture)
#设置背景图
background=pygame.image.load("resources/image/background.png").convert_alpha()

def startGame():
    #游戏循环帧率
    clock=pygame.time.Clock()
    #判断游戏退出循环参数
    running=True
    #游戏主循环
    while running:
        #绘制背景
        screen.fill(0)
        screen.blit(background,(0,0))
        #控制游戏最大帧率60
        clock.tick(60)
        #更新屏幕
        pygame.display.update()
        #处理游戏退出
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
startGame()
