#python template
import pygame as pg
import random
import sys
import os

# Variables
HEIGHT=600
WIDTH=800
FPS = 60

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# set up assets folders/font
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
snd_folder = os.path.join(game_folder, "snd")
font_name = pg.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    mob=Mob()
    all_sprites.add(mob)
    mob_sprites.add(mob)

def draw_shield_bar(surf, x, y, pct):
    if pct<0:
        pct=0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct/100)*BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def show_go_screen():
    pg.init()
    pg.mixer.init()
    screen.fill(BLACK)
    draw_text(screen, "Shoot 'em up", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Your SCORE:", 30, WIDTH/2-100, HEIGHT/2)
    draw_text(screen, str(score), 30, WIDTH/2+50, HEIGHT/2)
    draw_text(screen, "Press 'p' to play", 30, WIDTH/2, HEIGHT - 50)
    draw_text(screen, "Use arrows to move and spacebar to shoot 'em up", 30, WIDTH/2, HEIGHT-100)
    pg.display.flip()

    waiting = True
    while waiting:
        pg.init()
        pg.mixer.init()
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            pg.init()
            keystate = pg.key.get_pressed()
            if keystate[pg.K_p]:
                waiting = False

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (50, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2 )
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 100
        self.speedx = 0
        self.shield = 100

    def update(self):
        self.x_speed = 0
        self.y_speed = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_DOWN]:
            self.y_speed = 5
        if keystate[pg.K_UP]:
            self.y_speed = -5
        if keystate[pg.K_LEFT]:
            self.x_speed = -5
        if keystate[pg.K_RIGHT]:
            self.x_speed = 5
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed

        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2 )
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -75)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()


    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = missile_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2 )
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Money(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "money.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.9/2 )
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(0, HEIGHT - self.rect.height)

class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect. center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#init pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Shoot 'em up")
clock = pg.time.Clock()

# Load game images
background = pg.image.load(os.path.join(img_folder, "background.png")).convert()
background_rect = background.get_rect()
player_img = pg.image.load(os.path.join(img_folder, "ship.png")).convert()
missile_img = pg.image.load(os.path.join(img_folder, "missile.png")).convert()
meteor_img = pg.image.load(os.path.join(img_folder, "meteor.png")).convert()
money_img = pg.image.load(os.path.join(img_folder, "money.png")).convert()
meteor_images = []
meteor_list = ['meteor.png', 'meteor1.png', 'meteor2.png', 'meteor3.png',
'meteor4.png', 'meteorBrown1.png', 'meteorBrown2.png', 'meteorBrown3.png',
'meteorGrey1.png', 'meteorGrey1.png']
for img in meteor_list:
    meteor_images.append(pg.image.load(os.path.join(img_folder, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pg.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pg.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pg.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
# Load game sounds
ching_sound = pg.mixer.Sound(os.path.join(snd_folder, 'ching.wav'))
shot_sound = pg.mixer.Sound(os.path.join(snd_folder, 'shot.wav'))
shot_sound.set_volume(0.5)
explode_sound = pg.mixer.Sound(os.path.join(snd_folder, 'explode.wav'))
explode2_sound = pg.mixer.Sound(os.path.join(snd_folder, 'explode2.wav'))
shootrock_sound = pg.mixer.Sound(os.path.join(snd_folder, 'shootrock.wav'))
pg.mixer.music.load(os.path.join(snd_folder, 'background.wav'))
pg.mixer.music.play(loops=-1)

# Game Loop
game_over = True
running = True
score = 0
while running:

    if game_over:
        show_go_screen()
        game_over = False
        money_sprites = pg.sprite.Group()
        mob_sprites = pg.sprite.Group()
        all_sprites = pg.sprite.Group()
        bullets = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        money = Money()
        all_sprites.add(money)
        money_sprites.add(money)
        score=0
        for i in range(15):
            newmob()

    clock.tick(FPS)
    # process input (events)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()
                shot_sound.play()

    # update
    all_sprites.update()
    # check to see collisions
    hits = pg.sprite.spritecollide(player, money_sprites, True, pg.sprite.collide_circle)
    for hit in hits:
        score += 1000
        player.shield = 1.5*player.shield
        if player.shield > 100:
            player.shield = 100
        money = Money()
        all_sprites.add(money)
        money_sprites.add(money)
        ching_sound.play()


    # check to see if a bullet hit a mob
    hits = pg.sprite.groupcollide(mob_sprites, bullets, True, True)
    for hit in hits:
        #lazer_sound.play()
        score += 50 - hit.radius
        newmob()
        shootrock_sound.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()

    #check to see if mob hit player
    hits = pg.sprite.spritecollide(player, mob_sprites, True, pg.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius*1.5
        explode_sound.play()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            explode2_sound.play()
            game_over = True
    # draw/render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    #after drawing everything
    pg.display.flip()
