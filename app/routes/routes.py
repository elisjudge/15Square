from flask import Blueprint, render_template
from app.ai import Game, HumanPlayer

main = Blueprint('main', __name__)

@main.route('/')
def index():
    game = Game(player=HumanPlayer())
    board = game.board.cells.tolist()
    print(game.board)
    return render_template('index.html', board=board)