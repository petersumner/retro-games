from objects import Enemy

levels = {
    1: [
        { 'spawn':  35, 'type': 'green', 'size': 5 },
    ],
    2: [
        { 'spawn': 35, 'type': 'green', 'size': 3 },
        { 'spawn': 85, 'type': 'green', 'size': 3 }
    ]
}
    
class Level():
    
    def __init__(self, number, width, buffer):
        self.number = number
        self.width = width
        self.buffer = buffer
        self.enemies = self.load_level()
        
        self.x = 0
        self.dx = 1
        self.dy = 0.0
        
    def load_level(self):
        enemies = []
        enemy_grid = levels[self.number]
        for row in enemy_grid:
            if row['size'] == 1:
                enemies.append(Enemy(row['type'], (self.width - self.buffer*2) / 2, row['spawn']))
            else:
                spacing = (self.width - self.buffer*2) / (row['size']+1)
                for i in range(row['size']):
                    enemies.append(Enemy(None, row['type'], spacing*(i+1), row['spawn']))
        return enemies
    
    def move_enemies(self):
        self.dy = 0.1
        if self.x < -self.buffer:
            self.dx = 1
            self.dy = 1
        if self.x > self.buffer*2+1:
            self.dx = -1
            self.dy = 1
        for enemy in self.enemies:
            enemy.update_position(self.dx, self.dy)
        self.x += self.dx