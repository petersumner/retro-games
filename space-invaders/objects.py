player_height = 30
player_width = 60
player_cooldown = 40

enemy_height = 32
enemy_width = 40
enemy_cooldown = 80

player_bullet_speed = -8
player_bullet_height = 15
player_bullet_width = 4

enemy_bullet_speed = 2
enemy_bullet_height = 6
enemy_bullet_width = 6

color_white = (255, 255, 255)

class Object():
    
    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y
        
        self.set_spawn()
        
    def update_position(self, x, y):
        self.x += x
        self.y += y
        
    def set_spawn(self):
        self.spawn_point = [self.x, self.y]


class Player(Object):
    
    def __init__(self, img, x, y):
        self.type = 'player'
        self.img = img
        self.x = x
        self.y = y
        self.height = player_height
        self.width = player_width
        self.cooldown = player_cooldown
        
        self.reset_lives()
        
    def reset_lives(self):
        self.lives = 3
        
class Enemy(Object):
    
    def __init__(self, img, color, x, y):
        self.type = 'enemy'
        self.color = color
        self.img = img
        self.x = x
        self.y = y
        self.height = enemy_height
        self.width = enemy_width
        self.cooldown = enemy_cooldown
        
        self.dx = 0
        self.dy = 0
        
        match self.color:
            case 'green':
                self.points = 100
                self.dx = 1
                self.dy = 0.1
            case 'yellow':
                self.points = 250
            case 'red':
                self.points = 500
            case _:
                self.points = 0
                
        
class Bullet(Object):
    
    def __init__(self, type, x, y):
        self.x = x
        self.y = y
        self.type = type
        
        if self.type == 'player':
            self.speed = player_bullet_speed
            self.height = player_bullet_height
            self.width = player_bullet_width
        elif self.type == 'enemy':
            self.speed = enemy_bullet_speed
            self.height = enemy_bullet_height
            self.width = enemy_bullet_width
        else:
            self.speed = 0
            self.height = 0
            self.width = 0
