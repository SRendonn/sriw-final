from collections import defaultdict
from flask import Flask, render_template, request
from rdflib import Graph, URIRef

app = Flask(__name__)
g = Graph()
g.parse("FCF.owl", format="n3")
fcf = "http://www.FCF.com/"
g = sorted(g)


@app.route("/")
def hello_world():
    positions = ['Portero', 'Defensa', 'Mediocampista', 'Delantero']
    players = ['Ansu Fati', 'Bruno Fernandes', 'Carles Perez', 'Cristiano Ronaldo', 'Dorlan Pabón', 'Felipe Aguilar', 'Gerad Piqué',
               'Harry Maguire', 'Julian Barrera', 'Karim Benzema', 'Keylor Navas', 'Lautaro Martínez', 'Lionel Messi', 'Marc-André ter Stegen',
               'Marcelo', 'Mason Mount', 'Neymar', 'Nicolò Barella', 'Pedri', 'Romelu Lukaku', 'Vinícius Júnior']

    return render_template('index.html', positions=positions, players=players)


@app.route('/recommend-player', methods=['POST'])
def recommend_player():
    if request.method != 'POST':
        return '', 405
    else:
        data = request.form
        players = [data.get('player{}'.format(i)) for i in range(1, 6)]
        position = data.get('position')
        recommended_player = get_recommended_player(
            players=players, position=position)
        return render_template('recommendation.html', recommended_player=recommended_player)


def get_recommended_player(players, position):

    country_codes = defaultdict(lambda: '&#127758;', {
        'Colombia': '&#127464;&#127476;',
        'Spain': '&#127466;&#127480;',
        'Portugal': '&#127477;&#127481;',
        'England': '&#127468;&#127463;',
        'United Kingdom': '&#127468;&#127463;',
        'France': '&#127467;&#127479;',
        'Costa Rica': '&#127464;&#127479;',
        'Argentina': '&#127462;&#127479;',
        'Germany': '&#127465;&#127466;',
        'Brazil': '&#127463;&#127479;',
        'Italy': '&#127470;&#127481;',
        'Belgium': '&#127463;&#127466;',
        'Netherlands': '&#127475;&#127473;',
        'United States': '&#127482;&#127480;',
        'Chile': '&#127464;&#127473;',
        'Canada': '&#127464;&#127462;',
        'Senegal': '&#127480;&#127475;'
    })

    player = {
        'label': 'Carlitos Jaramillo',
        'position': 'Defensa',
        'country': 'Colombia',
        'club': 'Marinilla FC',
        'foot': 'Derecho',
        'value': 75,
    }

    return {
        'label': player['label'],
        'position': player['position'],
        'country': player['country'],
        'club': player['club'],
        'foot': player['foot'],
        'flag': country_codes[player['country']],
        'value': player['value']
    }


def get_players(positions = True):
    player_helper: list[str] = []
    for s, p, o in g:
        # player fcf:has_position ?position
        if str(p) == fcf + "has_position":
            if type(positions) is bool:
                player_helper.append((str(s), str(o)))
            elif type(positions) is list and str(o) in positions:
                player_helper.append((str(s), str(o)))

    foot_helper = []
    for s, p, o in g:
        if str(s) in dict(player_helper):
            player = next(tup for tup in player_helper if tup[0] == str(s))
            # player fcf:has_main_foot ?main_foot
            if str(p) == fcf + "has_main_foot":
                foot_helper.append((*player, str(o)))

    country_helper = []
    for s, p, o in g:
        if str(s) in dict(player_helper):
            player = next(tup for tup in foot_helper if tup[0] == str(s))
            # player fcf:has_birth_country ?birth_country
            if str(p) == fcf + "has_birth_country":
                country_helper.append((*player, str(o)))

    club_helper = []
    for s, p, o in g:
        if str(s) in dict(player_helper):
            player = next(tup for tup in country_helper if tup[0] == str(s))
            # player fcf:has_club ?club
            if str(p) == fcf + "has_club":
                club_helper.append((*player, str(o)))


    return club_helper


print(get_players())


