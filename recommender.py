from random import choice
from collections import defaultdict
import numpy as np
import pandas as pd
import queries

dummie_users = [
    {
        'Gerard Pique': 6,
        'Pedri': 8,
        'Ter Stegen': 7,
        'Vinicius Jr': 9,
        'Ansu Fati': 4,
        'Marcelo': 7,
        'Karim Benzema': 7,
        'Ter Stegen': 5,
        'Carles Perez': 4
    },
    {
        'Keylor Navas': 8,
        'Neymar Jr': 9,
        'Lionel Messi': 10,
        'Karim Benzema': 7
    },
    {
        'Lautaro Martinez': 7,
        'Nicolas Barella': 7
    },
    {
        'Harry Maguire': 8,
        'Cristiano Ronaldo': 10,
        'Bruno Fernandes': 8,
        'Romelo Lukaku': 7,
        'Mason Mount': 5
    },
    {
        'Felipe Aguilar': 7,
        'Dorlan Pabon': 7
    }
]


def get_recommended_player(players, position):

    weighted_players_matrix, user_scores = get_weighted_players_matrix(
        players)
    normalized_user_profile = get_normalized_user_profile(
        weighted_players_matrix, user_scores)

    # ? PREDICCIÓN CON COLABORACIÓN
    normalized_dummies_profiles = []
    dummies_scores = []
    individual_dummies_recommendation = []
    for scores in dummie_users:
        weighted_dummie_matrix, dummie_scores = get_weighted_players_matrix(
            scores)
        normalized_dummy_profile = get_normalized_user_profile(
            weighted_dummie_matrix, dummie_scores)
        normalized_dummies_profiles.append(normalized_dummy_profile)
        dummies_scores.append(dummie_scores)
        individual_dummies_recommendation.append(get_self_recommendations(
            weighted_dummie_matrix, normalized_dummy_profile, sort=False))

    dummies_distances = [get_distance(
        normalized_user_profile, profile) for profile in normalized_dummies_profiles]

    weighted_recommendation = get_weighted_recommendation(
        individual_dummies_recommendation, dummies_distances)
    best_recommendation = filter_recommendation(
        weighted_recommendation, players, position, method='min')

    return best_recommendation


def get_ideal_attrs(players, position):
    players_list = [queries.get_player_by_name(
        name) for name in players.keys()]
    df = pd.DataFrame(players_list, columns=[
                      'label', 'position', 'foot', 'country', 'club', 'league'])
    df.set_index('label', inplace=True)

    return {
        'country': df['country'].value_counts().idxmax(),
        'club': df['club'].value_counts().idxmax(),
        'league': df['league'].value_counts().idxmax(),
        'position': position
    }


def get_encoded_players_matrix():
    players = queries.get_players()
    df = pd.DataFrame(players, columns=[
                      'label', 'position', 'foot', 'country', 'club', 'league'])
    df.set_index('label', inplace=True)
    df = pd.get_dummies(
        df, columns=['position', 'foot', 'country', 'club', 'league'])

    return list(df.index.to_numpy()), list(df.to_numpy())


def get_weighted_players_matrix(user_players, impute_scalar=0):
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


def get_self_recommendations(weighted_players_matrix, user_profile, sort=True):
    recommendations = []
    players = queries.get_player_names()
    for i in range(len(weighted_players_matrix)):
        recommendations.append(
            (get_distance(user_profile, weighted_players_matrix[i]), players[i]))
    # entre más bajo mejor, significa que el jugador se distancia menos de lo que busca el usuario
    if sort:
        return sorted(recommendations)
    else:
        return recommendations


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
    ideal_attrs = get_ideal_attrs(user_players, position)

    best_fit = ()
    min_score = min(recommendations)[0]
    max_score = max(recommendations)[0]

    if method == 'max':
        best_fit = (-1, '')
        for r in recommendations:
            if r[1] not in list(user_players.keys()) and queries.get_player_by_name(r[1])[1] == position:
                if r[0] >= best_fit[0]:
                    best_fit = (r[0], r[1])
    elif method == 'min':
        best_fit = (100000, '')
        for r in recommendations:
            if r[1] not in user_players and queries.get_player_by_name(r[1])[1] == position:
                if r[0] <= best_fit[0]:
                    if not best_fit[1]:
                        best_fit = (r[0], r[1])
                    else:
                        p1 = queries.get_player_by_name(best_fit[1])
                        p2 = queries.get_player_by_name(r[1])
                        p1_counter = int(ideal_attrs['country'] == p1[3]) + int(
                            ideal_attrs['club'] == p1[4]) + int(ideal_attrs['league'] == p1[5])
                        p2_counter = int(ideal_attrs['country'] == p2[3]) + int(
                            ideal_attrs['club'] == p2[4]) + int(ideal_attrs['league'] == p2[5])
                        if p2_counter > p1_counter:
                            best_fit = (r[0], r[1])

    player_info = queries.get_player_by_name(best_fit[1])

    return ({
        'label': player_info[0],
        'position': player_info[1],
        'foot': player_info[2],
        'country': player_info[3],
        'club': player_info[4],
        'league': player_info[5],
        'flag': country_codes[player_info[3]],
    }, (best_fit[0] - min_score)/(max_score - min_score)
    )


def get_weighted_recommendation(user_recomendations, user_distances):
    index = [x[1] for x in user_recomendations[0]]
    weighted_recommendation = []
    for i in range(len(user_recomendations)):
        user_values = np.array([x[0] for x in user_recomendations[i]])
        user_distance = (user_distances[i] - min(user_distances)) / \
            (max(user_distances) - min(user_distances))
        weighted_recommendation.append(user_values * user_distance)
    total_recommendation = list(np.sum(weighted_recommendation, axis=0))
    results = []
    for i in range(len(index)):
        results.append((total_recommendation[i], index[i]))
    print(sorted(results))
    return sorted(results)
