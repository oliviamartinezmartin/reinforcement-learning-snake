"""
Snake Eater Game
Made with PyGame
Last modification in April 2024 by José Luis Perán
Machine Learning Classes - University Carlos III of Madrid
"""

from snake_env import SnakeGameEnv
from q_learning import QLearning
import pygame
import sys

def main():
    # Window size
    FRAME_SIZE_X = 500
    FRAME_SIZE_Y = 500
    
    # Colors (R, G, B)
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GOLD = pygame.Color(255, 215, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    DARK_BLUE = pygame.Color(0, 0, 139)

    difficulty = 100  # Adjust as needed
    render_game = True # Show the game or not
    growing_body = True # Makes the body of the snake grow
    training = False # Defines if it should train or not

    # Initialize the game window, environment and q_learning algorithm
    # Your code here.
    # You must define the number of possible states.
    # number_states = whatever
    pygame.init()
    env = SnakeGameEnv(FRAME_SIZE_X, FRAME_SIZE_Y, growing_body)

    number_states = 128
    ql = QLearning(n_states=number_states, n_actions=4)  
    # num_episodes = the number of episodes you want for training.
    num_episodes = 500

    if render_game:
        game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))
        fps_controller = pygame.time.Clock()

    def compute_position(state, env):
        """
        New state encoding, considering:
        - Current direction
        - Direction towards the food
        - Danger ahead
        - Danger left
        - Danger right
        """
        current_dir = state[0]
        food_dir = state[1]
        danger_straight, danger_left, danger_right = env.check_dangers()

        dir_idx = ['UP', 'DOWN', 'LEFT', 'RIGHT'].index(current_dir)
        food_idx = ['UP', 'DOWN', 'LEFT', 'RIGHT'].index(food_dir)

        ds = int(danger_straight)
        dl = int(danger_left)
        dr = int(danger_right)

        return dir_idx * 4 * 8 + food_idx * 8 + ds * 4 + dl * 2 + dr


    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0
        game_over = False
        
        while not game_over:
            # Your code here.
            # Choose the best action for the state and possible actions from the q_learning algorithm
            # Call the environment step with that action and get next_state, reward and game_over variables

            # TODO: HECHO POR NOSOTRAS
            state_index = compute_position(state, env)
            allowed_actions = [0, 1, 2, 3]  # up, down, left, right
            action = ql.choose_action(state_index, allowed_actions)

            next_state, reward, game_over = env.step(action)
            next_state_index = compute_position(next_state, env)

            if training:
                # update the q table using those variables.
                ql.update_q_table(state_index, action, reward,
                                  next_state_index)
            # update the state and the total_reward.
            state = next_state
            total_reward += reward

            # Update time without food
            if env.snake_pos == env.food_pos:
                env.time_without_food = 0
            else:
                env.time_without_food += 1
            #TODO: HASTA AQUI

            # Render
            if render_game:
                game_window.fill(DARK_BLUE)
                snake_body = env.get_body()
                food_pos = env.get_food()
                for pos in snake_body:
                    pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        
                pygame.draw.rect(game_window, RED, pygame.Rect(food_pos[0],
                                                             food_pos[1], 10, 10))
            
            if env.check_game_over():
            	break
            	
            if render_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                pygame.display.flip()
                fps_controller.tick(difficulty)
        
        ql.save_q_table()
        print(f"Episode: {episode+1}, Total reward: {total_reward}, "
              f"Score: {env.score}, Apples eaten: {env.apples_eaten}")

    print(f"For the {num_episodes} episodes, the average score was "
          f"{env.total_score / num_episodes} "
          f"and the average number of apples eaten was "
          f"{env.total_apples_eaten / num_episodes}.")

if __name__ == "__main__":
    main()
