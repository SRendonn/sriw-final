from random import choice
from collections import defaultdict
import numpy as np
import pandas as pd
import queries

dummie_users = [
    {
        'Gerard Pique': 6,
        'Lionel Messi': 10,
        'Felipe Aguilar': 3,
        'Ter Stegen': 7,
        'Vinicius Jr': 9,
    },
    {
        'Harry Maguire': 5,
        'Pedri': 8,
        'Keylor Navas': 8,
        'Romelo Lukaku': 7,
        'Lautaru Martinez': 7
    },
    {
        'Ansu Fati': 6,
        'Cristiano Ronaldo': 10,
        'Dorlan Pabon': 4,
        'Bruno Fernandes': 9,
        'Carles Perez': 5
    },
]


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

    normalized_dummies_profiles = [
        get_normalized_user_profile(scores) for scores in dummie_users]
    normalized_user_profile = get_normalized_user_profile(players)

    # ? MOCK DATA
    random_name = choice(queries.get_players())[0]
    player = queries.get_player_by_name(random_name)

    return ({
        'label': player[0],
        'position': player[1],
        'foot': player[2],
        'country': player[3],
        'club': player[4],
        'flag': country_codes[player[3]],
    }, 69
    )


def get_encoded_players_matrix():
    players = queries.get_players()
    df = pd.DataFrame(players, columns=[
                      'label', 'position', 'foot', 'country', 'club'])
    df.set_index('label', inplace=True)
    df = pd.get_dummies(df, columns=['position', 'foot', 'country', 'club'])

    return list(df.index.to_numpy()), list(df.to_numpy())


def get_pondered_players_matrix(user_players: dict, impute_scalar):
    players_index, players_encoded = get_encoded_players_matrix()

    pondered_players_encoded = []
    total_user_score = 0

    for i, player in enumerate(players_index):
        current_player = user_players.get(player)
        if current_player:
            total_user_score += current_player
            pondered_players_encoded.append(
                [x * current_player for x in players_encoded[i]])
        else:
            total_user_score += impute_scalar
            pondered_players_encoded.append(
                [x * impute_scalar for x in players_encoded[i]])
    return pondered_players_encoded, total_user_score


def get_normalized_user_profile(user_players, impute_scalar=1):
    pondered_players_encoded, total_user_score = get_pondered_players_matrix(
        user_players, impute_scalar)
    user_profile = list(np.sum(pondered_players_encoded, axis=0))
    pondered_user_profile = [x/total_user_score for x in user_profile]

    # como las variables son categóricas, ya están normalizadas :D
    return pondered_user_profile
