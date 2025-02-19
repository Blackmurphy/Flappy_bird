import pygame as pg
import sys, time, random
from bird import Bird
from pipe import Pipe
pg.init()

class Game:
    def __init__(self):
        # Setting window config
        self.width = 600
        self.height = 768
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.move_speed = 250
        self.bird = Bird(self.scale_factor)

        self.is_enter_pressed = False
        self.pipes = []
        self.pipe_generate_counter = 715
        self.score = 0
        self.font = pg.font.SysFont("Arial", 30)
        self.game_over = False  # Add game_over attribute
        self.setUpBgAndGround()
        
        self.gameLoop()
    
    def gameLoop(self):
        last_time = time.time()
        while True:
            # Calculating delta time
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.is_enter_pressed = True
                        self.bird.update_on = True
                    if event.key == pg.K_SPACE and self.is_enter_pressed:
                        self.bird.flap(dt)
                    if event.key == pg.K_r and not self.is_enter_pressed:
                        self.restart_game()  # Call the restart method

            self.updateEverything(dt)
            self.checkCollisions()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def checkCollisions(self):
        if len(self.pipes):
            if self.bird.rect.bottom > 568:  # Bird hits the ground
                self.game_over = True
                self.is_enter_pressed = False
                self.bird.update_on = False
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
            self.bird.rect.colliderect(self.pipes[0].rect_up)):  # Bird hits a pipe
                self.game_over = True
                self.is_enter_pressed = False
                self.bird.update_on = False

            # Check if the bird passed the pipe
            if self.pipes and self.bird.rect.left > self.pipes[0].rect_up.right and not self.pipes[0].passed:
                self.score += 1
                self.pipes[0].passed = True  # Mark this pipe as passed

    def updateEverything(self, dt):
        if self.is_enter_pressed:
            # Moving the ground
            self.ground1_rect.x -= int(self.move_speed * dt)
            self.ground2_rect.x -= int(self.move_speed * dt)

            if self.ground1_rect.right < 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right < 0:
                self.ground2_rect.x = self.ground1_rect.right

            # Generating pipes
            if self.pipe_generate_counter > 70:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0
                
            self.pipe_generate_counter += 1

            # Moving the pipes
            for pipe in self.pipes:
                pipe.update(dt)
            
            # Removing pipes if out of screen
            if len(self.pipes) != 0:
                if self.pipes[0].rect_up.right < 0:
                    self.pipes.pop(0)
                  
            # Moving the bird
        self.bird.update(dt)

    def drawEverything(self):
        self.win.blit(self.bg_img, (0, -300))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)

        # Draw the score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.win.blit(score_text, (10, 10))

        # Draw restart message if game over
        if self.game_over:
            restart_text = self.font.render("Press R to Restart", True, (0, 0, 0))
            self.win.blit(restart_text, (self.width // 2 - 100, self.height // 2))

    def setUpBgAndGround(self):
        # Loading images for bg and ground
        self.bg_img = pg.transform.scale_by(pg.image.load("assets/bg.png").convert(), self.scale_factor)
        self.ground1_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor)
        self.ground2_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor)
        
        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568

    def restart_game(self):
        # Reset game state
        self.is_enter_pressed = False
        self.bird = Bird(self.scale_factor)  # Reset the bird
        self.pipes = []  # Clear the pipes
        self.pipe_generate_counter = 71  # Reset pipe generation counter
        self.score = 0  # Reset the score
        self.game_over = False  # Reset game over state

game = Game()