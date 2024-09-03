import pygame

screen_width = 800
screen_height = 600

paddle_width = 6
paddle_height = 100
ball_radius = 10

color_white = (255, 255, 255)

class Game():
    
    def __init__(self):
        self.left_paddle = Paddle(paddle_width/2, screen_height/2 - paddle_height/2)
        self.right_paddle = Paddle(screen_width - paddle_width, screen_height/2 - paddle_height/2)
        self.ball = Ball(self.left_paddle.x + paddle_width + ball_radius, self.left_paddle.y + paddle_height/2)

        self.left_score = 0
        self.right_score = 0
        self.ball_start = 'left'
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pong")
        
    def update_paddles(self, keys_down):
        if 'W' in keys_down and 'S' not in keys_down and self.left_paddle.y > 2:
            self.left_paddle.update_position(-2)
        elif 'S' in keys_down and 'W' not in keys_down and self.left_paddle.y < screen_height - paddle_height - 2:
            self.left_paddle.update_position(2)
        if 'UP' in keys_down and 'DOWN' not in keys_down and self.right_paddle.y > 2:
            self.right_paddle.update_position(-2)
        elif 'DOWN' in keys_down and 'UP' not in keys_down and self.right_paddle.y < screen_height - paddle_height - 2:
            self.right_paddle.update_position(2)
            
    def update_ball(self):
        if self.ball.dx == 0 and self.ball.dy == 0:
            if self.ball_start == 'left' and self.left_paddle.dy != 0:
                self.ball.set_velocity(-self.left_paddle.dy, self.left_paddle.dy)
            elif self.ball_start == 'right' and self.right_paddle.dy != 0:
                self.ball.set_velocity(self.right_paddle.dy, self.right_paddle.dy)
        
        if self.ball.y > screen_height - ball_radius or self.ball.y < ball_radius:
            self.ball.set_velocity(self.ball.dx, -self.ball.dy)
            
        if self.ball.x - self.ball.radius < paddle_width and self.ball.y > self.left_paddle.y and self.ball.y < self.left_paddle.y + paddle_height:
            self.ball.set_velocity(-self.ball.dx, self.ball.dy)
            
        if self.ball.x + self.ball.radius > screen_width - paddle_width and self.ball.y > self.right_paddle.y and self.ball.y < self.right_paddle.y + paddle_height:
            self.ball.set_velocity(-self.ball.dx, self.ball.dy)
            
        self.ball.update_position()

        
    def is_score(self):
        if self.ball.x < 1:
            self.right_score += 1
            self.ball_start = 'left'
        elif self.ball.x > screen_width:
            self.left_score += 1
            self.ball_start = 'right'
        else:
            return False
        return True
        
    def reset(self):
        self.left_paddle.set_position(paddle_width/2, screen_height/2 - paddle_height/2)
        self.left_paddle.dy = 0
        self.right_paddle.set_position(screen_width - paddle_width, screen_height/2 - paddle_height/2)
        self.right_paddle.dy = 0
        self.ball.set_velocity(0, 0)
        if self.ball_start == 'left':
            self.ball.set_position(self.left_paddle.x + paddle_width + self.ball.radius, self.left_paddle.y + paddle_height/2)
        else:
            self.ball.set_position(self.right_paddle.x - paddle_width - self.ball.radius, self.right_paddle.y + paddle_height/2)
        
    def draw_screen(self):
        self.screen.fill((0,0,0))
        self.left_paddle.draw_paddle(self.screen)
        self.right_paddle.draw_paddle(self.screen)
        self.ball.draw_ball(self.screen)
        
        
class Ball():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.dx = 0
        self.dy = 0
        
        self.radius = ball_radius
        self.color = color_white
        
    def set_position(self, x, y):
        self.x = x
        self.y = y
        
    def update_position(self):
        self.x += self.dx
        self.y += self.dy
        
    def set_velocity(self, dx, dy):
        self.dx = dx
        self.dy = dy
        
    def draw_ball(self, screen):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.radius)

        
class Paddle():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.dy = 0
        
        self.height = paddle_height
        self.width = paddle_width
        self.color = color_white        
        
    def set_position(self, x, y):
        self.x = x
        self.y = y
        
    def update_position(self, dy):
        self.dy = dy
        self.y += dy
        
    def draw_paddle(self, screen):
        pygame.draw.line(screen, self.color, (self.x, self.y), (self.x, self.y+self.height), width=self.width)

        