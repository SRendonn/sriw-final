from random import choice, randint
from collections import defaultdict
import queries

dummie_1 = {
    'Gerard Pique': 6,
    'Lionel Messi': 10,
    'Felipe Aguilar': 3,
    'Ter Stegen': 7,
    'Vinicius Jr': 9,
}

dummie_2 = {
    'Harry Maguire': 5,
    'Pedri': 8,
    'Keylor Navas': 8,
    'Romelo Lukaku': 7,
    'Lautaru Martinez': 7
}

dummie_3 = {
    'Ansu Fati': 6,
    'Cristiano Ronaldo': 10,
    'Dorlan Pabon': 4,
    'Bruno Fernandes': 9,
    'Carles Perez': 5
}


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

    player = queries.get_player_by_name(choice(queries.get_players())[0])

    return {
        'label': player[0][19:].replace('_', ' '),
        'position': player[1][19:].replace('_', ' '),
        'foot': player[2][19:].replace('_', ' '),
        'country': player[3][19:].replace('_', ' '),
        'club': player[4][19:].replace('_', ' '),
        'flag': country_codes[player[3][19:].replace('_', ' ')],
        'value': randint(1, 100)
    }
