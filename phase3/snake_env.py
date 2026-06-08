"""
Snake Eater Environment
Made with PyGame
Last modification in April 2024 by José Luis Perán
Machine Learning Classes - University Carlos III of Madrid
"""


import numpy as np
import random

class SnakeGameEnv:
    def __init__(self, frame_size_x=150, frame_size_y=150, growing_body=True):
        # Initializes the environment with default values
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.growing_body = growing_body
        self.total_score = 0
        self.total_apples_eaten = 0
        self.reset()

    def reset(self):
        # Resets the environment with default values
        self.snake_pos = [50, 50]
        self.snake_body = [[50, 50], [60, 50], [70, 50]]
        self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10, random.randrange(1, (self.frame_size_y // 10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.time_without_food = 0
        self.score = 0
        self.apples_eaten = 0
        self.game_over = False
        return self.get_state()

    def step(self, action):
        # Implements the logic to change the snake's direction based on action
        # Update the snake's head position based on the direction
        # Check for collision with food, walls, or self
        # Update the score and reset food as necessary
        # Determine if the game is over
        self.update_snake_position(action)
        reward = self.calculate_reward()
        self.update_food_position()
        state = self.get_state()
        self.game_over = self.check_game_over()
        return state, reward, self.game_over

    def get_state(self):
        """
        Returns a state tuple including:
        - current direction
        - direction of food
        - danger info (straight, left, right)
        """
        current_direction = self.direction
        direction_of_food = self.direction_of_food()
        danger_ahead, danger_left, danger_right = self.check_dangers()

        return (current_direction, direction_of_food, danger_ahead, danger_left,
        danger_right)



    def direction_of_food(self):
        """
        HECHO POR NOSOTRAS
        """
        food_x, food_y = self.food_pos
        snake_x, snake_y = self.snake_pos

        delta_x = food_x - snake_x
        delta_y = food_y - snake_y

        if abs(delta_x) > abs(delta_y):
            return 'RIGHT' if delta_x > 0 else 'LEFT'
        else:
            return 'DOWN' if delta_y > 0 else 'UP'


    def will_die(self, new_x, new_y):
        """
        HECHO POR NOSOTRAS
        This function returns whether the snake will die if it continues in
        the same direction
        """
        return (([new_x, new_y] in self.snake_body) or
                (new_y < 0 or new_y >= self.frame_size_y or new_x < 0
                 or new_x >= self.frame_size_x))

    def check_dangers(self):
        x, y = self.snake_pos
        direction = self.direction

        if direction == 'UP':
            straight = (x, y - 10)
            left = (x - 10, y)
            right = (x + 10, y)
        elif direction == 'DOWN':
            straight = (x, y + 10)
            left = (x + 10, y)
            right = (x - 10, y)
        elif direction == 'LEFT':
            straight = (x - 10, y)
            left = (x, y + 10)
            right = (x, y - 10)
        elif direction == 'RIGHT':
            straight = (x + 10, y)
            left = (x, y - 10)
            right = (x, y + 10)

        return (
            self.will_die(*straight),
            self.will_die(*left),
            self.will_die(*right)
        )

    def calculate_reward(self):
        """
        HECHO POR NOSOTRAS
        This function calculates and returns the reward based on the game state.
        It uses the internal state of the game (snake position, food position, etc.)
        to compute the reward.
        """

        if self.check_game_over():
            return -20  # Penalty for losing the game

        reward = 0

        # Check if the snake ate food
        ate_food = (self.snake_pos[0] == self.food_pos[0] and self.snake_pos[
            1] == self.food_pos[1])
        if ate_food:
            reward += 15  # Positive reward for eating food
            self.food_spawn = False  # Food is consumed, need to respawn
        else:
            # Calculate distance to the food
            old_distance = abs(self.snake_pos[0] - self.food_pos[0]) + abs(
                self.snake_pos[1] - self.food_pos[1])
            # Calculate the new distance after moving
            x, y = self.snake_pos
            if self.direction == 'UP':
                next_x, next_y = x, y - 10
            elif self.direction == 'DOWN':
                next_x, next_y = x, y + 10
            elif self.direction == 'LEFT':
                next_x, next_y = x - 10, y
            elif self.direction == 'RIGHT':
                next_x, next_y = x + 10, y

            new_distance = (abs(next_x - self.food_pos[0]) +
                            abs(next_y - self.food_pos[1]))

            # Reward based on distance: smaller distance = better
            if new_distance < old_distance:
                reward += 2  # Moving closer to the food
            elif new_distance > old_distance:
                reward -= 1  # Moving farther away from the food

        # Check the time without eating food
        """
        if self.time_without_food > 100:
            reward -= 5  # Penalize if too long without eating food
        """

        return reward


    def check_game_over(self):
        # HECHO POR NOSOTRAS
        # Return True if the game is over, else False
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10:
            return True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10:
            return True
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return True
                
        return False


    def get_body(self):
    	return self.snake_body

    def get_food(self):
    	return self.food_pos


    def update_snake_position(self, action):
        # Updates the snake's position based on the action
        # Map action to direction
        change_to = ''
        direction = self.direction
        if action == 0:
            change_to = 'UP'
        elif action == 1:
            change_to = 'DOWN'
        elif action == 2:
            change_to = 'LEFT'
        elif action == 3:
            change_to = 'RIGHT'
    
        # Move the snake
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
    
        if direction == 'UP':
            self.snake_pos[1] -= 10
        elif direction == 'DOWN':
            self.snake_pos[1] += 10
        elif direction == 'LEFT':
            self.snake_pos[0] -= 10
        elif direction == 'RIGHT':
            self.snake_pos[0] += 10
            
        self.direction = direction
        
        self.snake_body.insert(0, list(self.snake_pos))
        
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 100
            self.total_score += 100
            self.apples_eaten += 1
            self.total_apples_eaten += 1
            self.food_spawn = False
            # If the snake is not growing
            if not self.growing_body:
                self.snake_body.pop()
        else:
            self.score -= 1
            self.total_score -= 1
            self.snake_body.pop()
    
    def update_food_position(self):
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_x//10)) * 10]
        self.food_spawn = True
        
        

