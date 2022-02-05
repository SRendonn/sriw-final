from flask import Flask, redirect, render_template, request
import queries
import recommender

app = Flask(__name__)


@app.route('/')
def hello_world():
    positions = ['Portero', 'Defensa', 'Mediocampista', 'Delantero']
    players = queries.get_player_names()

    return render_template('index.html', positions=positions, players=players)


@app.route('/recommend-player', methods=['POST'])
def recommend_player():
    if request.method != 'POST':
        return '', 405
    else:
        data = request.form
        players = {}
        position = data.get('position')

        for i in range(1, 6):
            player = data.get('player{}'.format(i))
            value = data.get('valueplayer{}'.format(i))
            if player and value:
                players[player] = int(value)

        if position and len(players) == 5:
            recommended_player = recommender.get_recommended_player(
                players=players, position=position)
            return render_template('recommendation.html', recommended_player=recommended_player)
        else:
            return redirect('/')
