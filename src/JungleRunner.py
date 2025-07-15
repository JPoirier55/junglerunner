'''Basic platforming game.

Developed for the Intro to Game Programming tutorial at US PyCon 2012.

Copyright 2012 Richard Jones <richard@mechanicalcat.net>
This code is placed in the Public Domain.
'''
import pygame
import tmx
from kezmenu import kezmenu
from pygame.locals import *

#
# Our enemies are quite dumb, just moving from side to side between "reverse"
# map triggers. It's game over if they hit the player.
#

class Gate(pygame.sprite.Sprite):
    image = pygame.image.load('gate.png')
    image2 = pygame.image.load('gate1.png')
    def __init__(self, location, *groups):
        super(Gate, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        
        self.frame = 0

class Flame(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Flame, self).__init__(*groups)
        self.images = []
        flame1 = pygame.image.load('Sprites/flamedark.png')
        flame3 = pygame.image.load('Sprites/flamedark1.png')
        flame2 = pygame.image.load('Sprites/flamedark.png')
        flame4 = pygame.image.load('Sprites/flamedark1.png')
        self.images.append(flame1)
        self.images.append(flame2)
        self.images.append(flame3)
        self.images.append(flame4)
        self.image = self.images[0]
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.frame = 0
        
    def update(self, dt, game):
            self.frame += 1
            if self.frame >3:
                self.frame = 0
            self.image = self.images[self.frame]

class Enemy(pygame.sprite.Sprite):
    
    frame = 0 
    def __init__(self, location, *groups):
        super(Enemy, self).__init__(*groups)
        
        # movement in the X direction; postive is right, negative is left
        self.direction = 1
        self.attack = 1
        self.images =[]
        enemy1 = pygame.image.load('Sprites/enemy1.png')
        enemy2 = pygame.image.load('Sprites/enemy2.png')
        enemy3 = pygame.image.load('Sprites/enemy3.png')
        enemy4 = pygame.image.load('Sprites/enemy4.png')
        self.images.append(enemy1)
        self.images.append(enemy1)
        self.images.append(enemy2)
        self.images.append(enemy2)
        self.images.append(enemy3)
        self.images.append(enemy3)
        self.images.append(enemy4)
        self.images.append(enemy4)
        self.image = self.images[0]
        self.rect = pygame.rect.Rect(location, self.image.get_size())  
        
        
    def update(self, dt, game):
        # move the enemy by 100 pixels per second in the movement direction
        self.rect.x += self.direction * 75 * dt
        
            
        self.attack -= .1
        
        if self.attack <= 0:
            self.attack = 1
            
        
        
        if self.direction == 1:
            self.frame += 1
            if self.frame >3:
                self.frame = 0
            self.image = self.images[self.frame]
        if self.direction == -1:
            
            self.frame += 1
            if self.frame >3:
                self.frame = 0
                
            self.image = self.images[self.frame+4]
    
        # check all reverse triggers in the map to see whether this enemy has
        # touched one
        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'reverse'):
            # reverse movement direction; make sure to move the enemy out of the
            # collision so it doesn't collide again immediately next update
            if self.direction > 0:
                self.rect.right = cell.left
                
            else:
                self.rect.left = cell.right
                
            self.direction *= -1
            break
        
        # check for collision with the player; on collision mark the flag on the
        # player to indicate game over (a health level could be decremented here
        # instead)
        if self.rect.colliderect(game.player.rect) and self.attack == 1:
            print(' hit')
            if game.player.direction == 1:
                game.player.attackedAnimate(-1)
            if game.player.direction == -1:
                game.player.attackedAnimate(1)
            game.player.life -= 1
            

#
# Bullets fired by the player move in one direction until their lifespan runs
# out or they hit an enemy. This could be extended to allow for enemy bullets.
#
class Bullet(pygame.sprite.Sprite):
    image = pygame.image.load('Sprites/bullet.png')
    def __init__(self, location, direction, *groups):
        super(Bullet, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        # movement in the X direction; postive is right, negative is left;
        # inherited from the player (shooter)
        self.direction = direction
        # time this bullet will live for in seconds
        self.lifespan = 1

    def update(self, dt, game):
        # decrement the lifespan of the bullet by the amount of time passed and
        # remove it from the game if its time runs out
        self.lifespan -= dt
        if self.lifespan < 0:
            self.kill()
            return

        # move the enemy by 400 pixels per second in the movement direction
        self.rect.x += self.direction * 400 * dt

        # check for collision with any of the enemy sprites; we pass the "kill
        # if collided" flag as True so any collided enemies are removed from the
        # game
        if pygame.sprite.spritecollide(self, game.enemies, True):
            
            game.explosion.play()
            # we also remove the bullet from the game or it will continue on
            # until its lifespan expires
            
            self.kill()

#
# Our player of the game represented as a sprite with many attributes and user
# control.
#

class Coin(pygame.sprite.Sprite):
    frame = 0
    def __init__(self, location, *groups):
        super(Coin, self).__init__(*groups)
        self.images = []
        for i in range(1,10):
            img = pygame.image.load("Sprites/goldCoin"+str(i)+".png")
            self.images.append(img)
            self.image = self.images[0]
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        
    def update(self, dt, game):
        self.frame +=1
        
        if self.frame > 8:
            self.frame = 0
        self.image = self.images[self.frame]

class Gear(pygame.sprite.Sprite):
    frame = 0
    def __init__(self, location, *groups):
        super(Gear, self).__init__(*groups)
        self.images = []
        
        img1 = pygame.image.load("Sprites/gear1.png")
        img2 = pygame.image.load("Sprites/gear2.png")
        self.images.append(img1)
        self.images.append(img2)
        self.images.append(img2)
        self.images.append(img1)
        
        self.image = self.images[0]
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        
    def update(self, dt, game):
        self.frame +=1
        
        if self.frame > 3:
            self.frame = 0
        self.image = self.images[self.frame]


class Player(pygame.sprite.Sprite):
    frame = 0
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.images = []
        for i in range(1,13):
            img = pygame.image.load("Sprites/guy"+str(i)+".png")
            self.images.append(img)
        
        self.guyleft = pygame.image.load('Sprites/guyhitleft.png')
        self.guyright = pygame.image.load('Sprites/guyhitright.png')
        self.image = self.images[0]
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        # is the player resting on a surface and able to jump?
        self.resting = False
        # player's velocity in the Y direction
        self.score = 0
        self.dy = 0
        self.life = 5
        self.keynum = 1
        # is the player dead?
        self.is_dead = False
        self.is_new = False
        # movement in the X direction; postive is right, negative is left
        self.direction = 1
        # time since the player last shot
        self.gun_cooldown = 0
        self.hit = pygame.mixer.Sound('Audio/boom2.wav')
        self.keyHoldlist = [] 
        
    def attackedAnimate(self, direction):
        
        if direction == -1:
            self.hit.play()
            self.image = self.guyright
            self.rect.left -= 100
            self.dy = -400
        else:
            self.hit.play()
            self.image = self.guyleft
            self.rect.right += 100
            self.dy = -400
    def update(self, dt, game):
        # take a copy of the current position of the player before movement for
        # use in movement collision response
        last = self.rect.copy()

        # handle the player movement left/right keys
        key = pygame.key.get_pressed()
        
        if self.life <= 0:
            self.is_dead = True
            
        if key[pygame.K_LEFT]:
            if key[pygame.K_LCTRL]:
                    self.image = self.images[10]
            if key[pygame.K_SPACE]:
                self.frame = 12
            self.rect.x -= 300 * dt
            self.frame += 1
            if self.frame > 5:
                self.frame = 0

            self.image = self.images[self.frame//2+5]
            self.direction = -1
        if key[pygame.K_RIGHT]:
            if key[pygame.K_LCTRL]:
                    self.image = self.images[11]
            if key[pygame.K_SPACE]:
                self.frame = 13
            self.rect.x += 300 * dt
            self.frame += 1
             
            if self.frame > 5:
                self.frame = 0
            self.image = self.images[self.frame//2]
            self.direction = 1

        # handle the player shooting key
        if key[pygame.K_LCTRL] and not self.gun_cooldown:
            
            # create a bullet at an appropriate position (the side of the player
            # sprite) and travelling in the correct direction
            if self.direction > 0:
                self.image = self.images[11]
                Bullet(self.rect.midright, 1, game.sprites)
            else:
                self.image = self.images[10]
                Bullet(self.rect.midleft, -1, game.sprites)
            # set the amount of time until the player can shoot again
            self.gun_cooldown = .3
            game.shoot.play()

        # decrement the time since the player last shot to a minimum of 0 (so
        # boolean checks work)
        self.gun_cooldown = max(0, self.gun_cooldown - dt)

        # if the player's allowed to let them jump with the spacebar; note that
        # wall-jumping could be allowed with an additional "touching a wall"
        # flag
        if self.resting and key[pygame.K_SPACE]:
            game.jump.play()
            # we jump by setting the player's velocity to something large going
            # up (positive Y is down the screen)
            self.dy = -500

        # add gravity on to the currect vertical speed
        self.dy = min(400, self.dy + 40)

        # now add the distance travelled for this update to the player position
        self.rect.y += self.dy * dt

        # collide the player with the map's blockers
        new = self.rect
        # reset the resting trigger; if we are at rest it'll be set again in the
        # loop; this prevents the player from being able to jump if they walk
        # off the edge of a platform
        self.resting = False
        
        
        # look up the tilemap triggers layer for all cells marked "blockers"
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            # find the actual value of the blockers property
            blockers = cell['blockers']
            # now for each side set in the blocker check for collision; only
            # collide if we transition through the blocker side (to avoid
            # false-positives) and align the player with the side collided to
            # make things neater
            if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if 't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
                # reset the vertical speed if we land or hit the roof; this
                # avoids strange additional vertical speed if there's a
                # collision and the player then leaves the platform
                self.dy = 0
            if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0
                
        for cell in game.tilemap.layers['triggers'].collide(new, 'key'):
            # find the actual value of the blockers property
            key = cell['key']
            
            for i in range(10):
                if key == i:
                    self.keyHoldlist.append(i)
                    
                    
        
        
        for cell in game.tilemap.layers['triggers'].collide(new, 'gate'):
            
            gate = cell['gate']
            
            for i in range(10):
                if gate == i:
                    if i in self.keyHoldlist:
                        return
                        
                    
                    elif last.right <= cell.left and new.right > cell.left:
                        new.right = cell.left
                        self.needkey1 = True
                        self.keynum = i
                        
        if pygame.sprite.spritecollide(self, game.coins, True):
            self.score += 1        
                        
                        
#                         back = pygame.image.load('tiles.png')
#                         self.is_new = True
#                         Game().main(screen, 'map%s.tmx'%i, back )
            
        # re-focus the tilemap viewport on the play     er's new position
        game.tilemap.set_focus(new.x, new.y)
        
    def needkey(self, keynum):
        key = pygame.image.load('Images/needkey%s.png'%keynum)
        if self.needkey1:            
            screen.blit(key, (200, 200))
        self.needkey1 = False
# Our game class represents one loaded level of the game and stores all the
# actors and other game-level state.
#

class Menu(object):
    running = True
    def main(self, screen):
        clock = pygame.time.Clock()
        background = pygame.image.load('Images/intro.png')

        menu = kezmenu.KezMenu(
            ['Play!', lambda: Game().main(screen, 'kaylasmap.tmx', background)],
            ['Quit', lambda: setattr(self, 'running', False)],
        )
        menu.x = 275
        menu.y = 350
        menu.color = (83,47,32)
        menu.focus_color = (108,210,0)
        menu.font = pygame.font.SysFont("constantia", 50)
        menu.enableEffect('raise-col-padding-on-focus', enlarge_time=0.1)
    
        while self.running:
            menu.update(pygame.event.get(), clock.tick(30)/1000.)
            screen.blit(background, (0, 0))
            menu.draw(screen)
            pygame.display.flip()



class Game(object):
    def main(self, screen, level, background):
        # grab a clock so we can limit and measure the passing of time
        clock = pygame.time.Clock()
        # we draw the background as a static image so we can just load it in the
        # main loop
        background = pygame.image.load('Images/image4.png')
        
        # load our tilemap and set the viewport for rendering to the screen's
        # size
        self.tilemap = tmx.load(level, screen.get_size())
        print(self.tilemap)
        
        # add a layer for our sprites controlled by the tilemap scrolling
        self.sprites = tmx.SpriteLayer()
        self.tilemap.layers.append(self.sprites)
        # fine the player start cell in the triggers layer
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        # use the "pixel" x and y coordinates for the player start
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        
        # add a separate layer for enemies so we can find them more easily later
        self.enemies = tmx.SpriteLayer()
        self.levelstuff = tmx.SpriteLayer()
        self.gates = tmx.SpriteLayer()
        self.coins = tmx.SpriteLayer()
        self.gears = tmx.SpriteLayer()
        self.tilemap.layers.append(self.enemies)
        self.tilemap.layers.append(self.levelstuff)
        self.tilemap.layers.append(self.gates)
        self.tilemap.layers.append(self.coins)
        self.tilemap.layers.append(self.gears)
        # add an enemy for each "enemy" trigger in the map
        for enemy in self.tilemap.layers['triggers'].find('enemy'):
            Enemy((enemy.px, enemy.py), self.enemies)
        for flame in self.tilemap.layers['triggers'].find('flame'):
            Flame((flame.px,flame.py), self.levelstuff)
        for coin in self.tilemap.layers['triggers'].find('coin'):
            Coin((coin.px,coin.py), self.coins)
        for gate in self.tilemap.layers['triggers'].find('gate'):
            Gate((gate.px,gate.py), self.gates)
        for gear in self.tilemap.layers['triggers'].find('gear'):
            Gear((gear.px,gear.py), self.gears)
        
        # load the sound effects used in playing a level of the game
        self.jump = pygame.mixer.Sound('Audio/jump.wav')
        self.shoot = pygame.mixer.Sound('Audio/shoot.wav')
        self.explosion = pygame.mixer.Sound('Audio/explosion.wav')
        self.player.needkey1 = False
        while 1:
            # limit updates to 30 times per second and determine how much time
            # passed since the last update
            dt = clock.tick(30)
            
            # handle basic game events; terminate this main loop if the window
            # is closed or the escape key is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                
  
            # update the tilemap and everything in it passing the elapsed time
            # since the last update (in seconds) and this Game object
            self.tilemap.update(dt / 1000., self)
            # construct the scene by drawing the background and then the rest of
            # the game imagery over the top
            screen.blit(background, (0, 0))
            self.tilemap.draw(screen)
            self.player.needkey(self.player.keynum)
            pygame.display.flip()
            
            # terminate this main loop if the player dies; a simple change here
            # could be to replace the "print" with the invocation of a simple
            # "game over" scene
            if self.player.is_dead:
                print('YOU DIED')
                return
            
            if self.tilemap.layers['triggers'].collide(self.player.rect, 'exit'):
                print('YOU WIN')
                return
            if self.player.is_new:
                break
            
            
                   

if __name__ == '__main__':
    # if we're invoked as a program then initialise pygame, create a window and
    # run the game
    print('woo')
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Menu().main(screen)

    

