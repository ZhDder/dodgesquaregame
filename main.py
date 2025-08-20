import pygame
import random
import sys
import numpy as np
from agent import Agent
from debug import ScrollingText
import matplotlib.pyplot as plt

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FPS = 120
BG = (90,90,90)
pygame.display.set_caption("DodgeballUltra")
screen_rect = pygame.rect.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
top_edge_rect = pygame.rect.Rect(0,0,SCREEN_WIDTH,1)
down_edge_rect = pygame.rect.Rect(0,SCREEN_HEIGHT,SCREEN_WIDTH,1)
left_edge_rect = pygame.rect.Rect(0,0,1,SCREEN_HEIGHT)
right_edge_rect = pygame.rect.Rect(SCREEN_WIDTH,0,1,SCREEN_HEIGHT)

score_font = pygame.font.Font(None, 25)
title_font = pygame.font.Font(None, 400)
title_font1 = pygame.font.Font(None, 295)
medium_font = pygame.font.Font(None, 40)

action_text_object = ScrollingText(medium_font, screen)

def draw_bg():
    screen.fill(BG)

class Player:
    def __init__(self):
        self.rect = pygame.rect.Rect(640,360,60,60)  
        self.pos = pygame.Vector2(640, 360)
        self.spd = 15
        self.dest = self.pos
        self.height = self.rect.height
        self.width = self.rect.width
        self.x = self.rect.x
        self.y = self.rect.y

        self.hp = 3

    def set_dest(self, pos):
        x = max(self.width//2 , min(pos[0], SCREEN_WIDTH - self.width//2))
        y = max(self.height//2, min(pos[1], SCREEN_HEIGHT - self.height//2))
        self.dest = pygame.Vector2((x,y))

    def check_edge(self):
        return self.collision(top_edge_rect) or self.collision(down_edge_rect) or self.collision(left_edge_rect) or self.collision(right_edge_rect)
    
    def move(self):

        vect = self.dest - self.pos
        move_length = vect.length()

        if move_length < self.spd:
            self.pos = self.dest

        elif move_length != 0:
            vect.normalize_ip()
            self.pos = self.pos + vect * self.spd

        self.rect.center = list(int(a) for a in self.pos)


    def collision(self, rect):
        return self.rect.colliderect(rect)
        """
        x = rect.x
        y = rect.y
        height = rect.height
        width = rect.width

        if x + width > self.x and y + height > self.y and y < self.y + self.height:
            return True
        
        elif x < self.x + self.width and y + height > self.y and self.y + self.height > y:
            return True
        
        elif y + height > self.y and x + width > x and x < self.x + self.width:
            return True
        
        elif y < self.y + self.height and x + width > self.x and x > self.x + self.width:
            return True

        return False"""


    def draw(self):
        pygame.draw.rect(screen, (0,0,0), self.rect)

        for i in range(1, self.hp+1):
            pygame.draw.rect(screen, (0,255,0), pygame.rect.Rect(25*i,25, 10, 5))

class Enemy:
    def __init__(self):
        self.code = random.randint(0,1)
        self.spd = 10

        if self.code == 0:
            self.rect = random.choice([pygame.rect.Rect(0, random.randint(0, 720), 20, 20),
                                      pygame.rect.Rect(1280, random.randint(0, 720), 20, 20)])

        else:
            self.rect = random.choice([pygame.rect.Rect(random.randint(0, 1280), 0, 20, 20),
                                      pygame.rect.Rect(random.randint(0, 1280), 720, 20, 20)])

        self.pos = pygame.Vector2(self.rect.topleft)
        self.target = self.pos

    def set_target(self, pos):
        self.target = pygame.Vector2(pos)
        self.dir_vect = self.target - self.pos
        self.dir_vect.normalize_ip()


    def move(self):
        self.pos = self.pos + self.dir_vect * self.spd
        self.rect.center = list(int(a) for a in self.pos)
    
    def out_of_screen(self):
        return not self.rect.colliderect(screen_rect)


def game_loop():
    player = Player()
    enemies = []
    score = 0
    starting = True
    running = True
    n_enemies = 1
    frames_passed = 0

    while running:
        draw_bg()

        if starting:

            start_text1 = title_font1.render(f"DODGEBALL", True, (145,200,255))
            start_text2 = title_font.render(f"ULTRA", True, (145,200,255))
            start_text3 = medium_font.render(f"Start", True, (0,0,0))
            start_text4 = medium_font.render(f"Exit", True, (0,0,0))
            start_button = pygame.rect.Rect(1000, 500, 200, 75)
            exit_button = pygame.rect.Rect(1000, 600, 200, 75)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if (event.pos[0] > start_button.x and event.pos[1] > start_button.y) and (event.pos[0] < start_button.x + start_button.width and event.pos[1] < start_button.y + start_button.height):
                        starting = False
                    
                    elif (event.pos[0] > exit_button.x and event.pos[1] > exit_button.y) and (event.pos[0] < exit_button.x + exit_button.width and event.pos[1] < exit_button.y + exit_button.height):
                        pygame.quit()
                        sys.exit()
                

            pygame.draw.rect(screen, (240,230,220), start_button)
            pygame.draw.rect(screen, (240,230,220), exit_button)

            screen.blit(start_text1, screen_rect.topleft)
            screen.blit(start_text2, (screen_rect.topleft[0], screen_rect.topleft[1]+200))
            screen.blit(start_text3, (1065, 525))
            screen.blit(start_text4, (1072, 625))

        elif player.hp > 0:
            draw_bg()
            player.draw()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    player.set_dest(pygame.mouse.get_pos())
            
            if len(enemies) < n_enemies:
                obj = Enemy()
                obj.set_target(player.pos)
                enemies.append(obj)
            frames_passed = frames_passed + 1

            if frames_passed > 60 and n_enemies < 20:
                n_enemies = n_enemies + 1
                frames_passed = 0
                score = score + 1

            for enemy in enemies:
                pygame.draw.rect(screen, (156,156,156), enemy.rect)
                if player.collision(enemy.rect):
                    enemies.remove(enemy)
                    player.hp = player.hp - 1

                else:
                    enemy.move()
                
                if enemy.out_of_screen():
                    enemies.remove(enemy)

            score_text = score_font.render(f"SCORE:{score}", True, (255,255,255))
            screen.blit(score_text, (1150, 25))


            player.move()
        
        elif player.hp == 0:
            draw_bg()

            exit_button = pygame.rect.Rect(1000, 600, 200, 75)
            restart_button = pygame.rect.Rect(1000, 500, 200, 75)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (event.pos[0] > exit_button.x and event.pos[1] > exit_button.y) and (event.pos[0] < exit_button.x + exit_button.width and event.pos[1] < exit_button.y + exit_button.height):
                        pygame.quit()
                        sys.exit()
                    if (event.pos[0] > restart_button.x and event.pos[1] > restart_button.y) and (event.pos[0] < restart_button.x + restart_button.width and event.pos[1] < restart_button.y + restart_button.height):
                        player.hp = 3
                        enemies = []
                        score = 0
                        player.pos = pygame.Vector2(640, 360)


            end_text1 = title_font.render(f"GAME", True, (255,100,70))
            end_text2 = title_font.render(f"OVER...", True, (255,100,70))
            end_text3 = medium_font.render(f"Your final score: {score}", True, (255,0,0))
            end_text4 = medium_font.render(f"Exit", True, (0,0,0))
            restart_text = medium_font.render(f"Restart", True, (0,0,0))

            pygame.draw.rect(screen, (240,230,220), exit_button)
            pygame.draw.rect(screen, (240,230,220), restart_button)
            screen.blit(end_text1, screen_rect.topleft)
            screen.blit(end_text2, (screen_rect.topleft[0],screen_rect.topleft[1]+250))
            screen.blit(end_text3, (screen_rect.topleft[0]+100, screen_rect.topleft[1] + 600))
            screen.blit(end_text4, (1072, 625))
            screen.blit(restart_text, (1056, 525))

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


#########################################################################################################
##########################          Agent training          #############################################
#########################################################################################################


def step(player, action, enemies): #Number of possible actions: up, down, left, right, top_left, top_right, down_right, down_left = 8
    done = False
    reward = 0

    if action == 0:
        player.set_dest((player.pos[0] - player.spd, player.pos[1]))
    elif action == 1:
        player.set_dest((player.pos[0] + player.spd, player.pos[1]))
    elif action == 2:
        player.set_dest((player.pos[0], player.pos[1] - player.spd))
    elif action == 3:
        player.set_dest((player.pos[0], player.pos[1] + player.spd))
    elif action == 4:
        player.set_dest((player.pos[0] - player.spd, player.pos[1] - player.spd))
    elif action == 5:
        player.set_dest((player.pos[0] - player.spd, player.pos[1] + player.spd))
    elif action == 6:
        player.set_dest((player.pos[0] + player.spd, player.pos[1] + player.spd))
    elif action == 7:
        player.set_dest((player.pos[0] + player.spd, player.pos[1] - player.spd))

    player.move()

    if player.check_edge():
        reward -= 10

    state = []
    state.append(player.pos[0])
    state.append(player.pos[1])
    
    sum_distance_from_player = 0
    enemies_to_remove = []
    for enemy in enemies:
        pygame.draw.rect(screen, (156,156,156), enemy.rect)
        if player.collision(enemy.rect):
            enemies.remove(enemy)
            player.hp = player.hp - 1
            reward -= 50

            if player.hp == 0:
                done = True
        else:
            enemy.move()
            
            if enemy.out_of_screen():
                enemies_to_remove.append(enemy)
        
        sum_distance_from_player += np.sqrt((player.pos[0] - enemy.pos[0]) ** 2 + (player.pos[1] - enemy.pos[1]) ** 2)

        state.append(enemy.pos[0])
        state.append(enemy.pos[1])
    
    reward += 1
    
    for enemy in enemies_to_remove:
        enemies.remove(enemy)

    while len(state) < 42:
        state.append(-1.0)

    if enemies:
        avg_distance_from_player = sum_distance_from_player / len(enemies)

        if avg_distance_from_player > 100:
            reward += 2

        elif avg_distance_from_player < 50:
            reward -= 2

    return normalize_array(np.array(state, dtype=np.float64)), reward, done

def env_reset():
    player = Player()
    enemies = []
    n_enemies = 20
    frames_passed = 0
    reward = 0
    done = False

    state = [player.pos[0], player.pos[1]]

    while len(state) < (n_enemies * 2 + 2):
        state.append(-1.0)


    return player, enemies, n_enemies, frames_passed, normalize_array(np.array(state, dtype=np.float64)), reward, done

def normalize_array(array):
    return (array - array.min()) / (array.max() - array.min())


action_map = {
        0 : 'UP',
        1 : 'DOWN',
        2 : 'LEFT',
        3 : 'RIGHT',
        4 : 'TOP_LEFT',
        5 : 'TOP_RIGHT',
        6 : 'DOWN_RIGHT',
        7 : 'DOWN_LEFT'
    }
def show_action(action_code):

    action_taken = action_map[action_code]
    action_text_object.add_text(action_taken)
    action_text_object.render()


def agent_training_loop(n_episodes = 1000):
    agent = Agent()
    eps_losses = []
    eps_rewards = []

    for eps in range(n_episodes):
        player, enemies, n_enemies, frames_passed, current_state, reward, done = env_reset()
        eps_loss = []
        eps_reward = 0
        eps_text = score_font.render(f"EPISODE:{eps}", True, (255,255,255))
        screen.blit(eps_text, (1150, 50))

        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
                    sys.exit()

            draw_bg()
            player.draw()

            if len(enemies) < n_enemies and frames_passed > 60:
                enemy = Enemy()
                enemy.set_target(player.pos)
                enemies.append(enemy)
                frames_passed = 0
            frames_passed = frames_passed + 1

            action = agent.select_action(current_state)
            next_state, reward, done = step(player, action, enemies)

            screen.blit(eps_text, (1150, 50))
            show_action(action)

            agent.remember(current_state, action, reward, next_state, done)
            current_state = next_state
            eps_reward += reward
            loss = agent.replay()

            if loss is not None:
                eps_loss.append(loss)

            pygame.display.flip()
            clock.tick(FPS)
        
        if eps_loss:
            eps_losses.append(np.mean(eps_loss))
        eps_rewards.append(eps_reward)


    return eps_losses, eps_rewards
            
losses, rewards = agent_training_loop()
fig, ax = plt.subplots(1, 2)

ax[0].plot(losses)
ax[0].set_title('Losses')
ax[1].plot(rewards)
ax[1].set_title('Rewards')
plt.show()