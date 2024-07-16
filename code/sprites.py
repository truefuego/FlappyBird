import pygame
from settings import *
from random import choice, randint

class BG(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        bg_image = pygame.image.load('FlappyBird/graphics/environment/background.png').convert()
        
        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        
        full_bg = pygame.transform.scale(bg_image,(full_width,full_height))
        self.image = pygame.Surface((full_width*2,full_height))
        self.image.blit(full_bg,(0,0))
        self.image.blit(full_bg,(full_width,0))
        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self,dt):
        self.pos.x -= 300 * dt 
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'

        ground_surf = pygame.image.load('FlappyBird/graphics/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surf,pygame.math.Vector2(ground_surf.get_size()) * scale_factor)
        self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)

class Plane(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)

        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # rect
        self.rect = self.image.get_rect(midleft= (WINDOW_WIDTH / 20,WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.gravity = 800
        self.direction = 0

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # sound
        self.jump_sound = pygame.mixer.Sound('FlappyBird/sounds/jump.wav')
        self.jump_sound.set_volume(0.2)

    def import_frames(self,scale_factor):
        self.frames = []
        for i in range(3):
            surf = pygame.image.load(f'FlappyBird/graphics/player/red{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)

    def update(self,dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

    def apply_gravity(self,dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.jump_sound.play()
        self.direction = -400

    def animate(self,dt): 
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image,-self.direction * 0.03,1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        self.sprite_type = 'obstacle'

        orientation = choice(('up','down'))
        surf = pygame.image.load(f'FlappyBird/graphics/obstacles/{choice((0,1))}.png').convert_alpha()
        x = WINDOW_WIDTH + randint(40,100)
        y = WINDOW_HEIGHT + randint(10,50)
        self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)
        self.rect = self.image.get_rect(midbottom = (x,y))
        if orientation == 'down':
            y = 0 + randint(-50,-10)
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect = self.image.get_rect(midtop = (x,y))

        self.pos = pygame.math.Vector2(self.rect.topleft)
        #mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()
            