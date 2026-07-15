# Wand-Warfare: 1v1 Shooter Game

A competitive, local multiplayer (1v1) target-shooting game developed in Python using the Pygame library. This project was designed and implemented as part of our academic programming course.

---

## 🎮 Game Overview
In Wand-Warfare, two players compete simultaneously on a single screen to shoot spawning targets, manage resources, and outscore each other before the timer runs out. The game features interactive items, a combo system, and a persistent local leaderboard.

### Key Features:
- Real-Time 1v1 Local Multiplayer: Fast-paced split-control gameplay on a single screen.
- Combo System: Succeeding shots yield multiplier bonuses, while missing resets the active streak.
- Interactive Targets: 
  - 👻 Normal Target (Ghost): Animates across the screen; points are awarded based on hit precision relative to the target's center.
  - ❄️ Freeze Item: Temporarily penalizes the opponent by drastically slowing down their cursor.
  - 🎒 Ammo Item: Replenishes the shooting player's bullet count upon impact.
- Persistent Leaderboard: High scores are automatically saved to a local SQLite database. Features in-game searching and dynamic filtering.

---

## 🛠️ Prerequisites & Installation

To run this game, make sure you have Python installed on your system. 

Open your terminal in the project's root directory and install the required library (pygame) using the provided dependency file:

`bash
pip install -r requirements.txt

🕹️ Controls
​Player 1 (Red Cursor):
​Movement: W, A, S, D keys
​Shoot: Space bar
​Player 2 (Blue Cursor):
​Movement: Arrow Keys
​Shoot: Enter or Right Control

​📂 Project Structure
​1v1 shooter_main.py: The central game loop and state management.
​player.py & cursor.py: Logic for tracking player stats, inputs, and cursor physics.
​target.py, NormalTarget.py, FreezeItem.py, AmmoItem.py: Object-oriented implementations of destructible entities and power-ups.
​db_manager.py & leaderboard.py: Controls database interactions and the score display board UI.
​btn.py: Custom modular button component handling hover and click states.
​/graphics, /sfx, /fonts: High-quality, optimized 16-bit pixel art assets, audio, and typography.
