# Reinforcement Learning Snake Agent using Q-Learning

## Overview

This project implements a reinforcement learning agent that learns to play the Snake game using Q-learning. The objective was to design a compact and generalizable state representation that allows the agent to perform well across different board sizes.

The work focuses on how incremental improvements in state design and reward shaping affect learning performance, starting from a simple baseline model and progressing to an enhanced version with improved environmental awareness.

---

## Motivation

The purpose of this project is to explore how reinforcement learning agents behave under limited state representations and how reward design affects learning stability.

Unlike deep learning approaches, this project focuses on tabular Q-learning to better understand the fundamentals of decision-making under uncertainty.

## Demo

https://raw.githubusercontent.com/oliviamartinezmartin/reinforcement-learning-snake/main/snake_samplevideo.mp4

> Q-learning agent learning to play Snake through reward-driven exploration.

## Objective

The goal of the project is to train an agent that can:
- Learn to play Snake using Q-learning
- Maximize survival time and food collection
- Generalize across different board sizes
- Balance exploration and exploitation effectively

---

## Methodology

### Phase 1: State and Reward Design

The initial state representation includes three components:
- Current direction of the snake (4 values)
- Relative position of the food (4 values)
- Immediate danger ahead (binary)

This results in a Q-table with 32 possible states, chosen to keep the model simple and efficient for learning.

The reward function is defined as follows:
- +15 for eating food
- -20 for dying
- +1 / -1 depending on whether the snake moves closer or farther from the food
- A penalty for excessive inactivity was initially tested but later removed due to instability during training

---

### Phase 2: Q-learning Implementation

The agent was implemented using a standard Q-learning framework, including:
- State extraction function (`get_state`)
- Reward computation (`calculate_reward`)
- Q-table update rule

The following hyperparameters were used:
- Learning rate (α): 0.1
- Exploration rate (ε): tuned experimentally
- Discount factor (γ): 0.9

These values provided a stable balance between convergence speed and performance.

---

### Phase 3: State Enhancement

The state representation was extended to include additional spatial information:
- Danger on the left
- Danger on the right

This increased the state space to 128 possible states and significantly improved the agent’s ability to avoid collisions and make more informed decisions.

---

## Results

The final model was evaluated across multiple board sizes.

On a 500x500 board:
- Average score: 2406.76
- Average apples per episode: 36.77
- Maximum apples in a single episode: over 100

Key observations:
- Larger boards tend to improve performance due to reduced collision risk near boundaries
- Square boards produce more stable results than highly rectangular ones
- Body growth significantly increases difficulty due to self-collision
- The enhanced state representation improves performance consistently compared to the baseline model

---

## Key Insights

- State representation has a strong impact on learning performance
- Small increases in state complexity can significantly improve results
- Reward shaping is critical for stable convergence
- Simpler models can still perform competitively depending on environment constraints

---

## Tools and Technologies

- Python
- Q-learning
- Custom Snake environment
- NumPy

---

## Project Structure

phase2/
phase3/
SnakeGame.py
snake_env.py
q_learning.py
report.pdf

---

## How to run

python SnakeGame.py

---

## Author

Olivia Martínez
University Carlos III of Madrid
Machine Learning Course
