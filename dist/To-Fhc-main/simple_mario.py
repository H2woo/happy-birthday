import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置窗口大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("简单马里奥风格游戏")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100
        self.speed_x = 0
        self.speed_y = 0
        self.on_ground = False
        self.jump_power = -15

    def update(self):
        # 重力
        if not self.on_ground:
            self.speed_y += 1
        else:
            self.speed_y = 0

        # 移动
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 边界检查
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.speed_y = self.jump_power
            self.on_ground = False

# 敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed_x * self.direction
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1

# 平台类
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 创建精灵组
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# 创建玩家
player = Player()
all_sprites.add(player)

# 创建平台
platform1 = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
platforms.add(platform1)
all_sprites.add(platform1)

platform2 = Platform(300, SCREEN_HEIGHT - 150, 200, 20)
platforms.add(platform2)
all_sprites.add(platform2)

# 创建敌人
enemy1 = Enemy(400, SCREEN_HEIGHT - 100)
enemies.add(enemy1)
all_sprites.add(enemy1)

# 时钟
clock = pygame.time.Clock()

# 主循环
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -5
            elif event.key == pygame.K_RIGHT:
                player.speed_x = 5
            elif event.key == pygame.K_SPACE:
                player.jump()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speed_x = 0

    # 更新精灵
    all_sprites.update()

    # 检查玩家与平台的碰撞
    player.on_ground = False
    hits = pygame.sprite.spritecollide(player, platforms, False)
    for hit in hits:
        if player.speed_y > 0 and player.rect.bottom > hit.rect.top:
            player.rect.bottom = hit.rect.top
            player.on_ground = True
            player.speed_y = 0

    # 检查玩家与敌人的碰撞
    if pygame.sprite.spritecollide(player, enemies, False):
        running = False  # 游戏结束

    # 绘制
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()