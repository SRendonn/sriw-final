from flask import Flask, redirect, render_template, request
import queries
import recommender

app = Flask(__name__)


@app.route('/')
def hello_world():
    positions = ['Goalkeeper', 'Defender', 'Middlefield', 'Forward']
    players = queries.get_player_names()

    return render_template('index.html', positions=positions, players=players)


@app.route('/recommend-player', methods=['POST'])
def recommend_player():
    if request.method != 'POST':
        return redirect('/')
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
            recommended_players, values = recommender.get_recommended_player(
                players=players, position=position)

            key_factors_list = []
            tooltip_factors_list = []

            for recommended_player in recommended_players:
                key_factors = {
                    'position': 0,
                    'country': 0,
                    'club': 0,
                    'league': 0
                }
                tooltip_factors = {
                    'country': [],
                    'club': [],
                    'league': []
                }

                if recommended_player['position'] == position:
                    key_factors['position'] = 1

                for key in players.keys():
                    player = queries.get_player_by_name(key)
                    if player[3] == recommended_player['country']:
                        key_factors['country'] += 1
                        tooltip_factors['country'].append(player[0])
                    if player[4] == recommended_player['club']:
                        key_factors['club'] += 1
                        tooltip_factors['club'].append(player[0])
                    if player[5] == recommended_player['league']:
                        key_factors['league'] += 1
                        tooltip_factors['league'].append(player[0])

                key_factors_list.append(key_factors)
                tooltip_factors_list.append(tooltip_factors)

            return render_template('recommendation.html', recommended_players=recommended_players, values=values, key_factors_list=key_factors_list, tooltip_factors_list=tooltip_factors_list)
        else:
            return redirect('/')
