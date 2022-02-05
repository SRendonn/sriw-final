from rdflib import Graph

g = Graph()
g.parse("FCF.owl", format="n3")
fcf = "http://www.FCF.com/"
g = sorted(g)


def get_player_names():
    player_helper: list[str] = []
    for s, p, o in g:
        # player fcf:has_position ?position
        if str(p) == fcf + "has_position":
            player_helper.append(str(s)[19:].replace('_', ' '))
    return player_helper


def get_player_by_name(name):
    player_helper = ()
    for s, p, o in g:
        # player fcf:has_position ?position
        if str(s) == name and str(p) == fcf + "has_position":
            player_helper = (str(s), str(o))

    foot_helper = ()
    for s, p, o in g:
        if str(s) == name and str(p) == fcf + "has_main_foot":
            foot_helper = (*player_helper, str(o))

    country_helper = ()
    for s, p, o in g:
        if str(s) == name and str(p) == fcf + "has_birth_country":
            country_helper = (*foot_helper, str(o))

    club_helper = ()
    for s, p, o in g:
        if str(s) == name and str(p) == fcf + "has_club":
            club_helper = (*country_helper, str(o))

    return club_helper


def get_players():
    player_helper: list[str] = []
    for s, p, o in g:
        # player fcf:has_position ?position
        if str(p) == fcf + "has_position":
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


def get_players_by_position(position):
    player_helper: list[str] = []
    for s, p, o in g:
        # player fcf:has_position ?position
        if str(p) == fcf + "has_position":
            if str(o) == position:
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
