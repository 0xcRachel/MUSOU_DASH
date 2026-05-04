
<img src="https://i.pinimg.com/736x/29/d2/d2/29d2d258c3da14a6c4b9a1604596987a.jpg" />

# Musou Dash

A simple 2D endless runner game inspired by classic gameplay mechanics similar to Flappy Bird, built using Python and Pygame.

---

## Overview

**Musou Dash** is a lightweight game project developed as a Python course assignment.
The goal is to control a character and survive as long as possible by avoiding obstacles (Remake Flappy Bird).

The project focuses on:

* Core game logic
* Object-oriented design
* Clean project structure
* Basic game physics (gravity, movement, collision)
* Same game (Flappy Bird)
---

## Gameplay

* Press **SPACE** to make the player jump (flap)
* Avoid hitting the pipes
* Pass through gaps to earn points
* The game ends when collision occurs
* Press **R** to restart after Game Over

---

## Core Mechanics

* Gravity-based movement
* Procedural obstacle generation
* Collision detection
* Score tracking system
* Game state handling (Playing / Game Over)

---

## Project Structure

```
MUSOU_DASH/
│
├── assets/
│   ├── fonts/
│   ├── images/
│   └── sounds/
│
├── src/
│   ├── main.py        # Entry point
│   ├── game.py        # Main game loop & logic
│   ├── player.py      # Player behavior
│   ├── pipe.py        # Obstacles (pipes)
│   ├── ui.py          # UI rendering (score, text)
│   └── settings.py    # Configuration
│
├── requirements.txt
├── score.txt
└── README.md
```

---

##  Installation

### 1. Clone project

```bash
git clone <your-repo-url>
cd MUSOU_DASH
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate environment

**Linux / macOS:**

```bash
source venv/bin/activate
```

**Fish shell (Arch Linux):**

```bash
source venv/bin/activate.fish
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Game

```bash
python src/main.py
```

---

## Technologies Used

* Python 3.14
* Pygame
* NeoVim

---

## Future Improvements

* Pixel art sprites & animations
* Background scrolling
* Sound effects
* Start menu & UI polish
* High score saving system

---

##  Learning Objectives

This project was created to:

* Practice Python programming
* Understand game loops and rendering
* Apply OOP principles
* Build a complete small-scale application

---

##  License

This project is for educational purposes, made by 0xcRachel

## Contributors
<a href="https://github.com/0xcRachel/MUSOU_DASH/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=0xcRachel/MUSOU_DASH" />
</a>
