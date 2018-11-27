import Intro
import PlayGame
import Rules
import GameModeSelection
import GameOver
         
Intro.intro()
players = GameModeSelection.gameModeSelection()
Rules.rules()
score = PlayGame.playGame(players)
GameOver.gameover(score)

