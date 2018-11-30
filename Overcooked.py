import Intro
import PlayGame
import Rules
import GameModeSelection
import GameOver
         
Intro.intro()
players = GameModeSelection.gameModeSelection()
Rules.rules()
score = PlayGame.playGame(1)
GameOver.gameover(score)

