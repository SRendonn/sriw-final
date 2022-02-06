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

    weighted_players_matrix, user_scores = get_weighted_players_matrix(
        players)
    normalized_user_profile = get_normalized_user_profile(
        weighted_players_matrix, user_scores)

    # ? PREDICCIÓN SIN COLABORACIÓN
    individual_recommendation = get_self_recommendations(
        weighted_players_matrix, normalized_user_profile)

    # ? PREDICCIÓN CON COLABORACIÓN
    normalized_dummies_profiles = []
    dummies_scores = []
    for scores in dummie_users:
        weighted_dummie_matrix, dummie_scores = get_weighted_players_matrix(
            scores)
        normalized_dummies_profiles.append(
            get_normalized_user_profile(weighted_dummie_matrix, dummie_scores))
        dummies_scores.append(dummie_scores)

    dummies_distances = [get_distance(
        normalized_user_profile, profile) for profile in normalized_dummies_profiles]

    colab_recommendation = get_colab_recommendations(
        dummies_scores, dummies_distances)

    best_recommendation = filter_recommendation(
        colab_recommendation, players, position, method='max')

    return best_recommendation


def get_encoded_players_matrix():
    players = queries.get_players()
    df = pd.DataFrame(players, columns=[
                      'label', 'position', 'foot', 'country', 'club', 'league'])
    df.set_index('label', inplace=True)
    df = pd.get_dummies(
        df, columns=['position', 'foot', 'country', 'club', 'league'])

    return list(df.index.to_numpy()), list(df.to_numpy())


def get_weighted_players_matrix(user_players, impute_scalar=1):
    players_index, players_encoded = get_encoded_players_matrix()

    weighted_players_encoded = []
    user_scores = []

    for i, player in enumerate(players_index):
        current_player = user_players.get(player)
        if current_player:
            user_scores.append(current_player)
            weighted_players_encoded.append(
                [x * current_player for x in players_encoded[i]])
        else:
            user_scores.append(impute_scalar)
            weighted_players_encoded.append(
                [x * impute_scalar for x in players_encoded[i]])
    return weighted_players_encoded, user_scores


def get_normalized_user_profile(weighted_players_matrix, user_scores):
    user_profile = list(np.sum(weighted_players_matrix, axis=0))
    total_user_score = sum(user_scores)
    weighted_user_profile = [x/total_user_score for x in user_profile]

    # como las variables son categóricas, ya están normalizadas :D
    return weighted_user_profile


def get_distance(user_profile_x, user_profile_y):
    np_x = np.array(user_profile_x)
    np_y = np.array(user_profile_y)
    return np.linalg.norm(np_y - np_x)


def get_colab_recommendations(scores, distances):
    user_recommendations = [None] * len(distances)
    for i in range(len(distances)):
        user_recommendations[i] = list(np.array(scores[i]) * distances[i])
    players = queries.get_player_names()
    total_recommendations = list(np.sum(user_recommendations, axis=0))
    # entre más alto mejor, significa que el jugador está mejor calificado ponderado por los usuarios
    return sorted([(total_recommendations[i]/sum(distances), players[i]) for i in range(len(players))], reverse=True)


def get_self_recommendations(weighted_players_matrix, user_profile):
    recommendations = []
    players = queries.get_player_names()
    for i in range(len(weighted_players_matrix)):
        recommendations.append(
            (get_distance(user_profile, weighted_players_matrix[i]), players[i]))
    # entre más bajo mejor, significa que el jugador se distancia menos de lo que busca el usuario
    return sorted(recommendations)


def filter_recommendation(recommendations, user_players, position, method='max'):

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

    best_fit = ()
    if method == 'max':
        best_fit = (-1, '')
        max_score = max(recommendations)[0]
        for r in recommendations:
            if r[1] not in list(user_players.keys()) and queries.get_player_by_name(r[1])[1] == position:
                if r[0]/max_score > best_fit[0]:
                    best_fit = (r[0]/max_score, r[1])
    elif method == 'min':
        best_fit = (100000, '')
        min_score = min(recommendations)[0]
        for r in recommendations:
            if r[1] not in user_players and queries.get_player_by_name(r[1])[1] == position:
                if r[0]/min_score < best_fit[0]:
                    best_fit = (r[0]/min_score, r[1])
    player_info = queries.get_player_by_name(best_fit[1])
    return ({
        'label': player_info[0],
        'position': player_info[1],
        'foot': player_info[2],
        'country': player_info[3],
        'club': player_info[4],
        'league': player_info[5],
        'flag': country_codes[player_info[3]],
    }, best_fit[0]
    )
