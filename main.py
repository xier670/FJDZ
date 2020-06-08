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



#子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self,bullet_img,init_pos):
        # 调用父类的初始化方法初始化Sprite的属性
        pygame.sprite.Sprite.__init__(self)
        self.image=bullet_img
        self.rect=self.image.get_rect()
        self.rect.midbottom=init_pos
        self.speed=10

    def move(self):
        self.rect.top -= self.speed

# 敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    # 敌机移动，边界判断及删除在游戏主循环里处理
    def move(self):
        self.rect.top += self.speed





#玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self,player_rect,init_pos):
        #调用父类的初始化方法初始化sprite的属性
        pygame.sprite.Sprite.__init__(self)
        self.image=[] #用来存储玩家飞机图片的列表
        for i in range(len(player_rect)):
            self.image.append(player_rect[i].convert_alpha())

        self.rect=player_rect[0].get_rect()
        self.rect.topleft=init_pos
        self.speed=8
        self.bullets=pygame.sprite.Group()
        self.img_index=0
        self.is_hit=False

    #发射子弹
    def shoot(self,bullet_img):
        bullet=Bullet(bullet_img,self.rect.midtop)
        self.bullets.add(bullet)

    #向上移动，需要判断边界
    def moveUp(self):
        if self.rect.top<=0:
            self.rect.top=0
        else:
            self.rect.top-=self.speed

    #向下移动，需要判断边界
    def moveDown(self):
        if self.rect.top>=SCREEN_HEIGHT-self.rect.height:
            self.rect.top=SCREEN_HEIGHT-self.rect.height
        else:
            self.rect.top+=self.speed

    #向左移动，需要判断边界
    def moveLeft(self):
        if self.rect.left <=0:
            self.rect.left=0
        else:
            self.rect.left-=self.speed

    #向右移动，需要判断边界
    def moveRight(self):
        if self.rect.left>=SCREEN_WIDTH-self.rect.width:
            self.rect.left=SCREEN_WIDTH-self.rect.width
        else:
            self.rect.left+=self.speed


# 游戏结束背景图
game_over = pygame.image.load('resources/image/gameover.png')
# 子弹图片
plane_bullet = pygame.image.load('resources/image/bullet.png')
# 飞机图片
player_img1= pygame.image.load('resources/image/player1.png')
player_img2= pygame.image.load('resources/image/player2.png')
player_img3= pygame.image.load('resources/image/player_off1.png')
player_img4= pygame.image.load('resources/image/player_off2.png')
player_img5= pygame.image.load('resources/image/player_off3.png')
# 敌机图片
enemy_img1= pygame.image.load('resources/image/enemy1.png')
enemy_img2= pygame.image.load('resources/image/enemy2.png')
enemy_img3= pygame.image.load('resources/image/enemy3.png')
enemy_img4= pygame.image.load('resources/image/enemy4.png')

def startGame():
    # 设置玩家飞机不同状态的图片列表，多张图片展示为动画效果
    player_rect = []
    # 玩家飞机图片
    player_rect.append(player_img1)
    player_rect.append(player_img2)
    # 玩家爆炸图片
    player_rect.append(player_img2)
    player_rect.append(player_img3)
    player_rect.append(player_img4)
    player_rect.append(player_img5)
    player_pos = [200, 600]
    # 初始化玩家飞机
    player = Player(player_rect, player_pos)
    # 子弹图片
    bullet_img = plane_bullet
    # 敌机不同状态的图片列表，多张图片展示为动画效果
    enemy1_img = enemy_img1
    enemy1_rect = enemy1_img.get_rect()
    enemy1_down_imgs = []
    enemy1_down_imgs.append(enemy_img1)
    enemy1_down_imgs.append(enemy_img2)
    enemy1_down_imgs.append(enemy_img3)
    enemy1_down_imgs.append(enemy_img4)
    # 储存敌机
    enemies1 = pygame.sprite.Group()
    # 存储被击毁的飞机，用来渲染击毁动画
    enemies_down = pygame.sprite.Group()
    # 初始化射击及敌机移动频率
    shoot_frequency = 0
    enemy_frequency = 0
    # 玩家飞机被击中后的效果处理
    player_down_index = 16
    # 初始化分数
    score = 0
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
        # 生成子弹，需要控制发射频率
        # 首先判断玩家飞机没有被击中
        if not player.is_hit:
            if shoot_frequency % 15 == 0:
                player.shoot(bullet_img)
            shoot_frequency += 1
            if shoot_frequency >= 15:
                shoot_frequency = 0
        for bullet in player.bullets:
            # 以固定速度移动子弹
            bullet.move()
            # 移动出屏幕后删除子弹
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        # 显示子弹
        player.bullets.draw(screen)
        # 生成敌机，需要控制生成频率
        if enemy_frequency % 50 == 0:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        enemy_frequency += 1
        if enemy_frequency >= 100:
            enemy_frequency = 0
        for enemy in enemies1:
            # 移动敌机
            enemy.move()
            # 敌机与玩家飞机碰撞效果处理 两个精灵之间的圆检测
            if pygame.sprite.collide_circle(enemy, player):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player.is_hit = True
                break
            # 移动出屏幕后删除飞机
            if enemy.rect.top < 0:
                enemies1.remove(enemy)
        # 敌机被子弹击中效果处理
        # 将被击中的敌机对象添加到击毁敌机 Group 中，用来渲染击毁动画
        # 方法groupcollide()是检测两个精灵组中精灵们的矩形冲突
        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        # 遍历key值 返回的碰撞敌机
        for enemy_down in enemies1_down:
            # 点击销毁的敌机到列表
            enemies_down.add(enemy_down)
        # 绘制玩家飞机
        if not player.is_hit:
            screen.blit(player.image[player.img_index], player.rect)
            # 更换图片索引使飞机有动画效果
            player.img_index = shoot_frequency // 8
        else:
            # 玩家飞机被击中后的效果处理
            player.img_index = player_down_index // 8
            screen.blit(player.image[player.img_index], player.rect)
            player_down_index += 1
            if player_down_index > 47:
                # 击中效果处理完成后游戏结束
                running = False
        # 敌机被子弹击中效果显示
        for enemy_down in enemies_down:
            if enemy_down.down_index == 0:
                pass
            if enemy_down.down_index > 7:
                enemies_down.remove(enemy_down)
                score += 100
                continue
            # 显示碰撞图片
            screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
            enemy_down.down_index += 1
        # 显示精灵
        enemies1.draw(screen)
        # 绘制当前得分
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (255, 255, 255))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)
        # 更新屏幕
        pygame.display.update()
        # 处理游戏退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # 获取键盘事件（上下左右按键）
        key_pressed = pygame.key.get_pressed()
        # 处理键盘事件（移动飞机的位置）
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()

        #更新屏幕
        pygame.display.update()
        #处理游戏退出
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
startGame()
