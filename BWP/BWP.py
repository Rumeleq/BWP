import pygame
from sys import exit
import math
import random 


class LevelManager:
    def __init__(self, current_level):
        pygame.mixer.init()
        self.current_level = current_level
        self.objects_created = False
        self.horde_playing = False
        self.horde_sound = pygame.mixer.Sound("data/audio/ZombieHorde.ogg")
        self.horde_sound.set_volume(0.5)
        self.channel = pygame.mixer.Channel(0)
        self.level_1_transition = False

        self.transition_static = 0
        self.transition_current = 0

        self.level_1_zombie_amount = 15
        self.level_1_zombie_interval = 5500
        self.level_1_zombie_amount_per_spawn = 2

        self.level_2_zombie_amount = 50
        self.level_2_zombie_interval = 5000
        self.level_2_zombie_amount_per_spawn = 3

        self.level_3_zombie_amount = 100
        self.level_3_zombie_interval = 4000
        self.level_3_zombie_amount_per_spawn = 3
        
        self.level_4_zombie_amount = 150
        self.level_4_zombie_interval = 3750
        self.level_4_zombie_amount_per_spawn = 4
        
        self.level_5_zombie_amount = 200
        self.level_5_zombie_interval = 3000
        self.level_5_zombie_amount_per_spawn = 5

    def check_zombies_dead(self, zombie_group):
        for zombie in zombie_group:
            if zombie.alive:
                return False
        return True

    def level_up(self, level):
        if self.check_zombies_dead(zombie_group) and self.zombie_spawner.zombie_amount <= 0 and self.player.alive:
            self.player.kill()
            self.gun.kill()
            del self.zombie_spawner
            for zombie in dead_zombie_group:
                zombie.kill()
            for zombie in zombie_group:
                zombie.kill()
            for bullet in bullet_group:
                bullet.kill()
            zombie_group.empty()
            dead_zombie_group.empty()
            bullet_group.empty()
            player_group.empty()
            self.objects_created = False
            self.current_level = "level_" + str(level)
            print(self.current_level)
            pygame.mixer.pause()
            play_sound("data/audio/Win.ogg")
            self.transition(level)
            self.horde_playing = False

    def repetitive_levels(self):
        self.zombie_spawner.spawn_zombies()

        screen.blit(background, (0, 0))

        bullet_group.update(zombie_group)
        bullet_group.draw(screen)

        dead_zombie_group.draw(screen)
        dead_zombie_group.update(bullet_group)

        zombie_group.draw(screen)
        zombie_group.update(bullet_group)

        player_group.draw(screen)
        player_group.update()

        self.player.health_bar.create(screen)
        self.player.ammo_display.draw()

        cursor_group.update()
        cursor_group.draw(screen)
        
        if not self.channel.get_busy() or not self.horde_playing:
            self.horde_playing = True
            self.horde_sound.play(-1)

        if not self.player.alive:
            self.player_death()

        pygame.display.flip()

    def player_death(self):
        self.player.kill()
        self.gun.kill()
        del self.zombie_spawner
        for zombie in dead_zombie_group:
            zombie.kill()
        for zombie in zombie_group:
            zombie.kill()
        self.objects_created = False

        pygame.mixer.pause()
        play_sound("data/audio/Death.ogg")
        self.horde_playing = False

        screen.fill((0, 0, 0))

        font = pygame.font.Font("data/font/pixeleum.ttf", 60)
        text = font.render("deduwa, beka z ciebie", False, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

        screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.wait(5000)

    def transition(self, level):
        background = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        background.fill((0, 0, 0))

        for alpha in range(0, 100, 3):
            background.set_alpha(alpha)
            screen.blit(background, (0, 0))
            pygame.display.flip()
            pygame.time.delay(50)

        font = pygame.font.Font("data/font/pixeleum.ttf", 60)
        
        if self.current_level != "level_7":
            text = font.render("O krok bliżej Stolicy Piotrowej...", False, (255, 255, 255))
            level_text = font.render(f"Level {level}", False, (255, 255, 255))
            
        else:
            text = font.render(f"ubitych trupów: {kills}", False, (255, 255, 255))
            level_text = font.render("Good Ending oguem", False, (255, 255, 255))
        
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        level_text_rect = level_text.get_rect(center=(screen_width // 2, screen_height // 2-100))

        screen.blit(background, (0, 0))
        screen.blit(text, text_rect)

        screen.blit(background, (0, 0))
        screen.blit(level_text, level_text_rect)

        pygame.display.flip()
        pygame.time.delay(8000)

    def level_1(self):
        if not self.objects_created:
            self.objects_created = True
            self.zombie_spawner = ZombieSpawner(self.level_1_zombie_amount, self.level_1_zombie_interval, self.level_1_zombie_amount_per_spawn)
            self.gun = Gun()
            self.player = Player(self.gun, self.gun.rect)
            player_group.add(self.player)

        if not self.level_1_transition:
            self.level_1_transition = True
            self.transition(1)
        
        self.repetitive_levels()
        if self.player.alive:
            self.level_up(2)
            
    def level_2(self):
        if not self.objects_created:
            self.objects_created = True
            self.zombie_spawner = ZombieSpawner(self.level_2_zombie_amount, self.level_2_zombie_interval, self.level_2_zombie_amount_per_spawn)
            self.gun = Gun()
            self.player = Player(self.gun, self.gun.rect)
            player_group.add(self.player)

        self.repetitive_levels()
        if self.player.alive:
            self.level_up(3)

    def level_3(self):
        if not self.objects_created:
            self.objects_created = True
            self.zombie_spawner = ZombieSpawner(self.level_3_zombie_amount, self.level_3_zombie_interval, self.level_3_zombie_amount_per_spawn)
            self.gun = Gun()
            self.player = Player(self.gun, self.gun.rect)
            player_group.add(self.player)

        self.repetitive_levels()
        if self.player.alive:
            self.level_up(4)

    def level_4(self):
        if not self.objects_created:
            self.objects_created = True
            self.zombie_spawner = ZombieSpawner(self.level_4_zombie_amount, self.level_4_zombie_interval, self.level_4_zombie_amount_per_spawn)
            self.gun = Gun()
            self.player = Player(self.gun, self.gun.rect)
            player_group.add(self.player)

        self.repetitive_levels()
        if self.player.alive:
            self.level_up(5)

    def level_5(self):
        if not self.objects_created:
            self.objects_created = True
            self.zombie_spawner = ZombieSpawner(self.level_5_zombie_amount, self.level_5_zombie_interval, self.level_5_zombie_amount_per_spawn)
            self.gun = Gun()
            self.player = Player(self.gun, self.gun.rect)
            player_group.add(self.player)

        self.repetitive_levels()
        self.level_up(7)

    
class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data/assets/interface/kursor.png").convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, width, height, max_hp, current_hp, x_pos, y_pos, outline_width, heart):
        super().__init__()
        self.heart_image = pygame.image.load("data/assets/interface/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (43, 63))
        self.heart_image_rect = self.heart_image.get_rect()
        self.width = width
        self.height = height
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.health_ratio = self.current_hp / self.max_hp
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.heart = heart
        self.outline_width = outline_width
        self.current_health_color = 118, 160, 80
        self.max_health_color = 49.8, 48.6, 40.8
        self.border_color = 40, 40, 50

        self.max_health_rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.outline_rect = pygame.Rect(self.x_pos, self.y_pos, self.width + self.outline_width, self.height + self.outline_width)
        self.outline_rect.center = self.max_health_rect.center
        self.current_health_rect = pygame.Rect(self.x_pos, self.y_pos, int(self.width * self.health_ratio), self.height)
        self.heart_image_rect.center = self.outline_rect.midleft

    def create(self, screen):
        if 0 < self.current_hp < self.max_hp or self.heart is True:
            pygame.draw.rect(screen, self.border_color, self.outline_rect, self.outline_width)
            pygame.draw.rect(screen, self.max_health_color, self.max_health_rect)
            pygame.draw.rect(screen, self.current_health_color, self.current_health_rect)
            if self.heart:    
                screen.blit(self.heart_image, self.heart_image_rect)

    def update(self, current_hp, x_pos, y_pos, update):
        self.current_hp = current_hp
        if update:
            self.max_health_rect.center = (x_pos, y_pos - 15)
            self.current_health_rect.topleft = self.max_health_rect.topleft
            self.outline_rect.center = self.max_health_rect.center

        self.health_ratio = self.current_hp / self.max_hp
        self.current_health_rect.width = int(self.width * self.health_ratio)


class AmmoDisplay(pygame.sprite.Sprite):
    def __init__(self, player_healthbar_outline_rect, player_ammo_amount):
        super().__init__()
        self.player_max_ammo = player_ammo_amount
        self.font = pygame.font.Font("data/font/pixeleum.ttf", 30)
        self.ammo_image = pygame.image.load("data/assets/interface/ammo_icon.png")
        self.ammo_image_rect = self.ammo_image.get_rect()
        self.pos = player_healthbar_outline_rect.topright
        self.pos = (self.pos[0] + 25, self.pos[1])
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 78, 38)
        self.ammo_image_rect = self.rect
        self.ammo_count_text = self.font.render(f"{player_ammo_amount}", False, (255, 255, 255))
        self.ammo_count_rect = self.ammo_count_text.get_rect()
        self.ammo_count_rect.midleft = (self.ammo_image_rect.centerx+2, self.ammo_image_rect.top+15)
    
    def draw(self):
        screen.blit(self.ammo_image, self.ammo_image_rect)
        screen.blit(self.ammo_count_text, self.ammo_count_rect)

    def update(self, player_ammo_amount):
        if player_ammo_amount > 0 and player_ammo_amount > self.player_max_ammo / 5:
            self.ammo_count_text = self.font.render(f"{player_ammo_amount}", False, (255, 255, 255))
        elif self.player_max_ammo / 5 >= player_ammo_amount > 0:
            self.ammo_count_text = self.font.render(f"{player_ammo_amount}", False, (255, 255, 0))
        else:
            self.ammo_count_text = self.font.render(f"{player_ammo_amount}", False, (200, 0, 0))


class Player(pygame.sprite.Sprite):
    def __init__(self, gun, gun_rect):
        super().__init__()
        self.alive = True
        self.walking = False
        self.speed = 5
        self.sprites = []
        self.sprites_index = 0
        self.sprites.append(pygame.image.load("data/assets/sprites/player_sprites/stand.png").convert_alpha())
        self.sprites.append(pygame.image.load("data/assets/sprites/player_sprites/1.png").convert_alpha())
        self.sprites.append(pygame.image.load("data/assets/sprites/player_sprites/2.png").convert_alpha())
        self.sprites.append(pygame.image.load("data/assets/sprites/player_sprites/3.png").convert_alpha())
        self.sprites.append(pygame.image.load("data/assets/sprites/player_sprites/4.png").convert_alpha())
        self.sprites.append(pygame.image.load("data/assets/sprites/player_sprites/5.png").convert_alpha())
        self.image = pygame.image.load("data/assets/sprites/player_sprites/2x.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.image = self.sprites[self.sprites_index]
        self.gun = gun
        self.rect.center = (screen_width/2, screen_height/2)
        self.gun_rect = gun_rect
        self.shadow = pygame.image.load("data/assets/sprites/player_sprites/shadow.png").convert_alpha()
        self.shadow_rect = self.shadow.get_rect()
        self.max_hp = 100
        self.current_hp = self.max_hp
        if level_manager.current_level == "level_1":
            self.ammo_amount = 100
        elif level_manager.current_level == "level_2":
            self.ammo_amount = 250
        elif level_manager.current_level == "level_3":
            self.ammo_amount = 500
        elif level_manager.current_level == "level_4":
            self.ammo_amount = 750
        elif level_manager.current_level == "level_5":
            self.ammo_amount = 1000
        self.health_bar_x = 50
        self.health_bar_y = 25
        self.health_bar = HealthBar(250, 30, self.max_hp, self.current_hp, self.health_bar_x, self.health_bar_y, 6, True)
        self.ammo_display = AmmoDisplay(self.health_bar.outline_rect, self.ammo_amount)
        self.last_time_healed = 0
        self.current_heal_time = 0
        self.hp_last_value = self.current_hp
        self.current_bullet_time = 0
        self.last_bullet_time = 0
        self.bullet_sound = pygame.mixer.Sound("data/audio/Rifle.ogg")
        self.empty_sound = pygame.mixer.Sound("data/audio/EmptyGun.ogg")

    def moving(self):
        keys = pygame.key.get_pressed()
        x_direction = 0
        y_direction = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            y_direction -= 1
            self.walking = True    
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            y_direction += 1
            self.walking = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            x_direction -= 1
            self.walking = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            x_direction += 1
            self.walking = True

        if x_direction != 0 and y_direction != 0:
            x_direction /= math.sqrt(2)
            y_direction /= math.sqrt(2)

        self.rect.x += int(self.speed * x_direction)
        self.rect.y += int(self.speed * y_direction)

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
        
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.walking = False
            self.sprites_index = 0

    def healing(self):
        if self.max_hp > self.current_hp == self.hp_last_value and self.current_heal_time - self.last_time_healed >= 1000:
            self.last_time_healed = pygame.time.get_ticks()
            self.current_hp += 2
            self.hp_last_value = self.current_hp
        elif self.current_heal_time - self.last_time_healed >= 5000:
            self.hp_last_value = self.current_hp
        self.current_heal_time = pygame.time.get_ticks()

    def animation(self):
        if self.walking:
            self.sprites_index += 0.25
            if int(self.sprites_index) >= len(self.sprites):
                self.sprites_index = 0
        self.image = self.sprites[int(self.sprites_index)]

    def shoot(self):
        if not level_manager.current_level == "intro" and not level_manager.current_level == "transition" and not level_manager.current_level == "ending":
            if pygame.mouse.get_pressed()[0] and self.current_bullet_time - self.last_bullet_time >= 100:
                if self.ammo_amount > 0:
                    self.last_bullet_time = pygame.time.get_ticks()
                    target_x, target_y = pygame.mouse.get_pos()
                    bullet = Bullet(level_manager.gun.rect.centerx, level_manager.gun.rect.centery, target_x, target_y, self.rect.centerx)
                    bullet_group.add(bullet)
                    self.ammo_amount -= 1
                    self.bullet_sound.play()
                elif self.current_bullet_time - self.last_bullet_time >= 500:
                    self.last_bullet_time = pygame.time.get_ticks()
                    self.empty_sound.play()
            self.current_bullet_time = pygame.time.get_ticks()

    def update(self):
        if self.current_hp <= 0:
            self.alive = False
        if self.alive:
            self.shoot()
            self.moving()
            self.animation()
            self.healing()
            self.health_bar.update(self.current_hp, None, None, False)
            self.ammo_display.update(self.ammo_amount)
            self.gun.image = pygame.image.load("data/assets/gun/gun.png").convert_alpha()
            self.gun.image = pygame.transform.scale2x(self.gun.image)

            if pygame.mouse.get_pos()[0] < self.rect.centerx:
                self.image = pygame.transform.flip(self.image, True, False)
                self.gun.image = pygame.transform.flip(self.gun.image, False, True)
                self.shadow = pygame.transform.flip(self.shadow, True, False)
                self.gun_rect.center = (self.rect.centerx + self.rect.width/4, self.rect.centery + self.rect.height/15)
            else:
                self.gun_rect.center = (self.rect.centerx - self.rect.width/4, self.rect.centery + self.rect.height/15)

            dx = pygame.mouse.get_pos()[0] - self.gun_rect.centerx
            dy = -(pygame.mouse.get_pos()[1] - self.gun_rect.centery)
            angle = math.degrees(math.atan2(dy, dx))
            rotated_gun_image = pygame.transform.rotate(self.gun.image, angle)
            rotated_gun_rect = rotated_gun_image.get_rect(center=(self.gun_rect.centerx, self.gun_rect.centery))
            self.shadow_rect.center = self.rect.midbottom
            screen.blit(self.shadow, self.shadow_rect)
            screen.blit(rotated_gun_image, rotated_gun_rect)
                
            self.image = pygame.transform.scale2x(self.image)
        

class Gun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data/assets/gun/gun2x.png").convert_alpha()
        self.rect = self.image.get_rect()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y, player_centerx):
        super().__init__()
        self.player_centerx = player_centerx
        self.damage = random.randint(4, 6)
        self.speed = 30
        self.image = pygame.image.load("data/assets/gun/bullet.png").convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()

        if target_x < self.player_centerx:
            self.image = pygame.transform.flip(self.image, False, True)

        dx = target_x - start_x
        dy = target_y - start_y
        rotate_angle = math.degrees(math.atan2(-dy, dx))

        self.image = pygame.transform.rotate(self.image, rotate_angle)
        self.rect = self.image.get_rect(center=(start_x, start_y))

        shoot_angle = math.atan2(dy, dx)
        self.dx = math.cos(shoot_angle) * self.speed
        self.dy = math.sin(shoot_angle) * self.speed
        self.x = start_x
        self.y = start_y

    def update(self, zombie_group):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()


class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.alive = True
        self.death_animation_played = False
        self.healthbar_visible = False
        self.speed = random.randint(1, 2)
        if self.speed == 1:
            self.damage = random.randint(10, 12)
            self.max_hp = random.randint(10, 15)
        else:
            self.damage = random.randint(8, 10)
            self.max_hp = random.randint(5, 10)
        self.current_hp = self.max_hp

        self.sprites = []
        self.death_sprites = []
        self.attack_sprites = []
        self.sprites_index = 0
        self.death_sprites_index = 0
        self.attack_sprites_index = 0

        self.sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/1.png").convert_alpha())
        self.sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/2_death1.png").convert_alpha())
        self.sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/3.png").convert_alpha())
        self.sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/4.png").convert_alpha())
        self.sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/5.png").convert_alpha())
        self.sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/6.png").convert_alpha())
        self.image = pygame.image.load("data/assets/sprites/zombie_sprites/2x.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.image = self.sprites[self.sprites_index]

        self.death_sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/2_death1.png").convert_alpha())
        self.death_sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/death2.png").convert_alpha())
        self.death_sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/death3.png").convert_alpha())

        self.attack_sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/attack1.png").convert_alpha())
        self.attack_sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/attack2.png").convert_alpha())
        self.attack_sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/attack3.png").convert_alpha())
        self.attack_sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/attack4.png").convert_alpha())
        self.attack_sprites.append(pygame.image.load("data/assets/sprites/zombie_sprites/attack5.png").convert_alpha())

        self.health_bar = HealthBar(50, 8, self.max_hp, self.current_hp, self.rect.centerx, self.rect.centery, 3, False)
        self.death_frame_static = 0
        self.death_frame_current = 0
        self.last_attack = 0
        self.attack_current = 500
        self.flag = True
        self.flag2 = False
        self.flag3 = False
        death_sounds = ["ZombieDeath.ogg", "ZombieDeath2.ogg"]
        self.death_sound = random.choice(death_sounds)
        if level_manager.current_level == "level_1":
            self.side = 1
            self.start_pos = (random.randint(300, 900), random.randint(-40, -20))
            self.rect.bottomleft = self.start_pos
        elif level_manager.current_level == "level_2":
            self.side = random.randint(1, 2)
            if self.side == 1:
                self.start_pos = (random.randint(300, 900), random.randint(-40, -20))
                self.rect.bottomleft = self.start_pos
            else:
                self.start_pos = (random.randint(0, 1200), random.randint(740, 760))
                self.rect.topleft = self.start_pos
        else:
            self.side = random.randint(1, 4)
            if self.side == 1:
                self.start_pos = (random.randint(300, 900), random.randint(-40, -20))
                self.rect.bottomleft = self.start_pos
            elif self.side == 2:
                self.start_pos = (random.randint(0, 1200), random.randint(740, 760))
                self.rect.topleft = self.start_pos
            elif self.side == 3:
                self.start_pos = (random.randint(-40, -20), random.randint(200, 670))
                self.rect.bottomright = self.start_pos
            else:
                self.start_pos = (random.randint(1300, 1320), random.randint(200, 670))
                self.rect.bottomleft = self.start_pos

    def attack(self):
        self.attack_sprites_index += 0.15
        if int(self.attack_sprites_index) >= len(self.attack_sprites):
            self.attack_sprites_index = 0
        self.image = self.attack_sprites[int(self.attack_sprites_index)-1]
        if self.attack_current - self.last_attack >= 1000:
            self.last_attack = pygame.time.get_ticks()
            level_manager.player.current_hp -= self.damage
            self.attack_sprites_index += self.speed / 10
        self.attack_current = pygame.time.get_ticks()

    def get_shot(self, bullet_group):
        global kills
        if self.alive:
            collided_bullets = pygame.sprite.spritecollide(self, bullet_group, True)            
            for bullet in collided_bullets:
                self.current_hp -= bullet.damage
                self.healthbar_visible = True
            if self.current_hp <= 0:
                self.alive = False
                kills += 1

    def animation(self):
        if self.alive:
            if not self.rect.collidepoint(level_manager.player.rect.center):
                self.sprites_index += self.speed / 10
                if int(self.sprites_index) >= len(self.sprites):
                    self.sprites_index = 0
                self.image = self.sprites[int(self.sprites_index)]
        else:
            if not int(self.death_sprites_index) >= len(self.death_sprites)-1:
                self.death_sprites_index += 0.1
            else:
                if not self.flag3:
                    play_sound("data/audio/" + self.death_sound)
                    self.flag3 = True
                self.flag2 = True
                if self.flag:
                    self.death_frame_static = pygame.time.get_ticks()
                    self.flag = False
                if self.death_frame_current - self.death_frame_static >= 45000:
                    self.kill()
                self.death_frame_current = pygame.time.get_ticks()

            self.image = self.death_sprites[int(self.death_sprites_index)]
            if not self.flag2:
                dx = level_manager.player.rect.centerx - self.rect.centerx
                dy = level_manager.player.rect.centery - self.rect.centery
                walk_angle = math.atan2(dy, dx)
                walk_dx = math.cos(walk_angle) * self.speed
                if abs(walk_dx) == walk_dx:
                    self.image = pygame.transform.flip(self.image, True, False)

    def walk(self):
        if self.rect.left > 0 and self.rect.top > 0 and self.rect.bottom < screen_height and self.rect.right < screen_width:
            dx = level_manager.player.rect.centerx - self.rect.centerx
            dy = level_manager.player.rect.centery - self.rect.centery
            walk_angle = math.atan2(dy, dx)
            walk_dx = math.cos(walk_angle) * self.speed
            walk_dy = math.sin(walk_angle) * self.speed
            self.rect.centerx += walk_dx
            self.rect.centery += walk_dy
            if abs(walk_dx) == walk_dx:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            if self.side == 1:
                self.rect.bottom += self.speed
            elif self.side == 2:
                self.rect.top -= self.speed
            elif self.side == 3:
                self.rect.right += self.speed
            else:
                self.rect.left -= self.speed

    def update(self, bullet_group):
        if self.alive:
            if self.rect.collidepoint(level_manager.player.rect.center):
                self.attack()
            else:
                self.walk()
                self.animation()

            self.get_shot(bullet_group)
        else:
            self.animation()

        if not self.alive and zombie_group.has(self):
            zombie_group.remove(self)
            dead_zombie_group.add(self)
        self.health_bar.update(self.current_hp, self.rect.midtop[0], self.rect.midtop[1], True)
        self.health_bar.create(screen)

        dx = level_manager.player.rect.centerx - self.rect.centerx
        dy = level_manager.player.rect.centery - self.rect.centery
        walk_angle = math.atan2(dy, dx)
        walk_dx = math.cos(walk_angle)
        if abs(walk_dx) == walk_dx and self.alive:
            self.image = pygame.transform.flip(self.image, True, False)
        if not self.rect.collidepoint(level_manager.player.rect.center) or dead_zombie_group.has(self):
            self.image = pygame.transform.scale2x(self.image)


class ZombieSpawner:
    def __init__(self, zombie_amount, zombie_interval, zombie_amount_per_spawn):
        self.zombie_amount = zombie_amount
        self.zombie_interval = zombie_interval
        self.zombie_amount_per_spawn = zombie_amount_per_spawn
        self.current_zombie_time = 0
        self.last_zombie_time = 0

    def spawn_zombies(self):
        if self.current_zombie_time - self.last_zombie_time >= random.randint(self.zombie_interval-100, self.zombie_interval+100) and self.zombie_amount > 0:
            zombie_amount_per_spawn = random.randint(self.zombie_amount_per_spawn-1, self.zombie_amount_per_spawn+1)
            self.zombie_amount -= zombie_amount_per_spawn
            self.last_zombie_time = pygame.time.get_ticks()
            for i in range(zombie_amount_per_spawn):
                zombie = Zombie()
                zombie_group.add(zombie)
        self.current_zombie_time = pygame.time.get_ticks()


def play_sound(path):
    sound = pygame.mixer.Sound(path)
    sound.play()


# Config
pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bizarne Wojaże Papaja")
favicon = pygame.image.load("data/assets/logo/favicon.png").convert_alpha()
pygame.display.set_icon(favicon)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
# Config

# Levele i kille
try:
    with open("data/txt/save.txt", "r") as file:
        current_level = file.readline().strip()
        kills = int(file.readline())
except IOError:
    current_level = "intro"
    kills = 0
# Levele i kille

# Grupy i instancje
level_manager = LevelManager(current_level)
cursor_group = pygame.sprite.GroupSingle()
bullet_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
dead_zombie_group = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
cursor = Cursor()
cursor_group.add(cursor)
# Grupy i instancje

# Grafika
background = pygame.image.load("data/assets/background/tło.png")
background = pygame.transform.scale(background, (screen_width, screen_height))
# Grafika

# intro
lines = [
    "Dawno, dawno temu,",
    # "",
    "w odległych Wadowicach",
    # "",
    "narodził się Karol zwany Wojtyłą,",
    # "",
    "który nie tylko poszedł na kremówki po maturze,",
    # "",
    "ale też zasiadł na tronie Stolicy Apostolskiej.",
    "",
    "",
    "Roku pańskiego 2137 wybuchła zainicjowana",
    # "",
    "przez nieznanego z imienia dyrektora z Międzychodu",
    # "",
    "epidemia nieumarłych trupów.",
    # "",
    "Wkrótce cała Ziemia została podbita",
    # "",
    "przez zastępy nieumarłych...",
    "",
    "",
    "Cała?",
    # "",
    "Nie!",
    "",
    "",
    "Jedna, jedyna osada,",
    # "",
    "zamieszkana przez nieugiętych Polaków,",
    # "",
    "wciąż stawia opór najeźdźcom",
    # "",
    "i uprzykrza życie hordom truposzy.",
    "",
    "",
    "Są to właśnie Wadowice,",
    # "",
    "rodzinne miasto Karola,",
    # "",
    "w którym zebrał on wszystkich,",
    # "",
    "których zdołał ocalić i którymi teraz przewodził.",
    "",
    "",
    "Zdawało się, że cała nadzieja na powrót człowieka",
    # "",
    "na szczyt łańcucha pokarmowego byłą stracona,",
    # "",
    "a gniew boży nieprzebłagany.",
    "",
    "",
    "Papież Polak, syn Polskiej ziemi, Jan Paweł II,",
    # "",
    "wiary jednak nie stracił i przyrzekł odbicie",
    # "",
    "Stolicy Piotrowej i Królestwa Bożego na Ziemi",
    # "",
    "oraz wyzwolenie tych, którzy przetrwali.",
    "",
    "",
    "Ale czy mu się to uda?"
]
font = pygame.font.Font("data/font/pixeleum.ttf", 30)
intro_logo = pygame.image.load("data/assets/logo/logo.png").convert_alpha()
intro_logo_rect = intro_logo.get_rect()
intro_logo_rect.center = (screen_width/2, screen_height/10)

intro_black_surface = pygame.Surface((screen_width, screen_height/5))
intro_black_surface.fill((0, 0, 0))

text_rendered = []
line_height = font.get_linesize()

for line in lines:
    rendered_line = font.render(line, True, (255, 255, 255))
    text_rendered.append(rendered_line)

text_rects = []
y_pos = screen_height // 2 - (len(text_rendered) * line_height) // 2

for rendered_line in text_rendered:
    text_rect = rendered_line.get_rect(center=(screen_width // 2, y_pos+1300))
    text_rects.append(text_rect)
    y_pos += line_height

star_play = False

# intro
while level_manager.current_level == "intro":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("data/txt/save.txt", "w") as file:
                file.write(str(current_level) + "\n")
                file.write(str(kills))
            pygame.quit()
            exit()
    if not star_play:
        star_play = True
        play_sound("data/audio/StarWars.ogg")

    screen.fill((0, 0, 0))
    
    for rendered_line, text_rect in zip(text_rendered, text_rects):
        screen.blit(rendered_line, text_rect)
        text_rect.y -= 1

    screen.blit(intro_black_surface, (0, 0))
    screen.blit(intro_logo, intro_logo_rect)
    
    if text_rects[-1].bottom <= -150:
        pygame.time.delay(2000)
        level_manager.current_level = "level_1"
    pygame.display.flip()
    clock.tick(60)

if current_level == "intro":
    del level_manager
    pygame.mixer.quit()
    current_level = "level_1"
    level_manager = LevelManager(current_level)

while level_manager.current_level == "level_1":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("data/txt/save.txt", "w") as file:
                file.write(str(current_level) + "\n")
                file.write(str(kills))
            pygame.quit()
            exit()
    level_manager.level_1()
    clock.tick(60)

if current_level == "level_1":
    del level_manager
    pygame.mixer.quit()
    current_level = "level_2"
    level_manager = LevelManager(current_level)

while level_manager.current_level == "level_2":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("data/txt/save.txt", "w") as file:
                file.write(str(current_level) + "\n")
                file.write(str(kills))
            pygame.quit()
            exit()

    level_manager.level_2()
    clock.tick(60)

if current_level == "level_2":
    del level_manager
    pygame.mixer.quit()
    current_level = "level_3"
    level_manager = LevelManager(current_level)

while level_manager.current_level == "level_3":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("data/txt/save.txt", "w") as file:
                file.write(str(current_level) + "\n")
                file.write(str(kills))
            pygame.quit()
            exit()

    level_manager.level_3()
    clock.tick(60)

if current_level == "level_3":
    del level_manager
    pygame.mixer.quit()
    current_level = "level_4"
    level_manager = LevelManager(current_level)

while level_manager.current_level == "level_4":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("data/txt/save.txt", "w") as file:
                file.write(str(current_level) + "\n")
                file.write(str(kills))
            pygame.quit()
            exit()

    level_manager.level_4()
    clock.tick(60)

if current_level == "level_4":
    del level_manager
    pygame.mixer.quit()
    current_level = "level_5"
    level_manager = LevelManager(current_level)

while level_manager.current_level == "level_5":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("data/txt/save.txt", "w") as file:
                file.write(str(current_level) + "\n")
                file.write(str(kills))
            pygame.quit()
            exit()

    level_manager.level_5()
    clock.tick(60)

if current_level == "level_5" or current_level == "level_7":
    current_level = "level_7"
    del level_manager
    pygame.mixer.quit()
    pygame.mixer.init()
    calm_sound = pygame.mixer.Sound("data/audio/TheCalm.ogg")
    calm_sound.play(-1)
    calm_sound.set_volume(0.75)
    pope_speech = pygame.mixer.Sound("data/audio/PopeSpeech.ogg")
    pope_speech.play(-1)
    papa_image = pygame.image.load("data/assets/sprites/player_sprites/1.png")
    papa_image = pygame.transform.scale2x(papa_image)
    papa_image_rect = papa_image.get_rect()
    ending_background = pygame.image.load("data/assets/background/watikan.png")
    ending_background_rect = ending_background.get_rect()
    ending_background_rect.bottomleft = (0, screen_height)
    papa_image_rect.bottomright = (ending_background_rect.midbottom[0]-80, ending_background_rect.midbottom[1])
    intro_logo_rect.x -= 35

while current_level == "level_7":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("data/txt/save.txt", "w") as file:
                file.write("intro" + "\n")
                file.write(str(kills))
            pygame.quit()
            exit()

    screen.blit(ending_background, ending_background_rect)
    screen.blit(papa_image, papa_image_rect)
    screen.blit(intro_logo, intro_logo_rect)
    pygame.display.flip()
