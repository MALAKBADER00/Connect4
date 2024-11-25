# Connect 4 Game

An implementation of the classic Connect 4 game featuring two gameplay modes:  
- **Human vs Human**  
- **Human vs AI** (powered by the MiniMax algorithm).  

The game uses **Pygame** for visualization and provides an engaging experience with smooth graphical interactions. The AI leverages adversarial search to make optimal moves, ensuring a challenging and competitive game.

## What is the MiniMax Algorithm?  
The MiniMax algorithm is a decision-making process used in game theory and AI. It evaluates all possible moves to minimize the maximum potential loss (or maximize the minimum gain). In this game, it allows the AI to anticipate the player's strategy and select the best move to win or block the opponent.


## Demo  
Below is a snapshot of the game in action:  
![Connect 4 Demo](pic.jpg)  

## How to Set Up and Run the Game

1. **Clone the Repository**  
   Open your terminal and run the following command:  
   ```bash
   git clone https://github.com/MALAKBADER00/connect4.git
   cd connect4

2. **Set Up the Virtual Environment**
   - for windows
     ```bash
     python -m venv venv
     venv\Scripts\activate
  - for mac
    ```bash
    python -m venv venv
    source venv/bin/activate
   

4. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   

6. **Run the Game**
   ```bash
   python human_vs_human.py
  or 
  ```bash
  python human_vs_ai.py
