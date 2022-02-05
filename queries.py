from rdflib import Graph

g = Graph()
g.parse("FCF.owl", format="n3")
fcf = "http://www.FCF.com/"
g = sorted(g)


def prettify(text):
    return text[19:].replace('_', ' ')


def get_player_names():
    player_helper: list[str] = []
    for s, p, o in g:
        # player fcf:has_position ?position
        if str(p) == fcf + "has_position":
            player_helper.append(prettify(str(s)))
    return player_helper


def get_player_by_name(name, pretty=True):
    player_helper = ()
    for s, p, o in g:
        current_name = prettify(str(s)) if pretty else str(s)
        if current_name == name and str(p) == fcf + "has_position":
            if pretty:
                player_helper = (prettify(str(s)), prettify(str(o)))
            else:
                player_helper = (str(s), str(o))
            break

    foot_helper = ()
    for s, p, o in g:
        current_name = prettify(str(s)) if pretty else str(s)
        if current_name == name and str(p) == fcf + "has_main_foot":
            if pretty:
                foot_helper = (*player_helper, prettify(str(o)))
            else:
                foot_helper = (*player_helper, str(o))
            break

    country_helper = ()
    for s, p, o in g:
        current_name = prettify(str(s)) if pretty else str(s)
        if current_name == name and str(p) == fcf + "has_birth_country":
            if pretty:
                country_helper = (*foot_helper, prettify(str(o)))
            else:
                country_helper = (*foot_helper, str(o))
            break

    club_helper = ()
    for s, p, o in g:
        current_name = prettify(str(s)) if pretty else str(s)
        if current_name == name and str(p) == fcf + "has_club":
            if pretty:
                club_helper = (*country_helper, prettify(str(o)))
            else:
                club_helper = (*country_helper, str(o))
            break

    return club_helper


def get_players(pretty=True):
    player_helper: list[str] = []
    for s, p, o in g:
        # player fcf:has_position ?position
        if str(p) == fcf + "has_position":
            if pretty:
                player_helper.append((prettify(str(s)), prettify(str(o))))
            else:
                player_helper.append((str(s), str(o)))

    foot_helper = []
    for s, p, o in g:
        name = prettify(str(s)) if pretty else str(s)
        if name in dict(player_helper):
            player = next(tup for tup in player_helper if tup[0] == name)
            # player fcf:has_main_foot ?main_foot
            if str(p) == fcf + "has_main_foot":
                if pretty:
                    foot_helper.append((*player, prettify(str(o))))
                else:
                    foot_helper.append((*player, str(o)))

    country_helper = []
    for s, p, o in g:
        name = prettify(str(s)) if pretty else str(s)
        if name in dict(player_helper):
            player = next(tup for tup in foot_helper if tup[0] == name)
            # player fcf:has_birth_country ?birth_country
            if str(p) == fcf + "has_birth_country":
                if pretty:
                    country_helper.append((*player, prettify(str(o))))
                else:
                    country_helper.append((*player, str(o)))

    club_helper = []
    for s, p, o in g:
        name = prettify(str(s)) if pretty else str(s)
        if name in dict(player_helper):
            player = next(tup for tup in country_helper if tup[0] == name)
            # player fcf:has_club ?club
            if str(p) == fcf + "has_club":
                if pretty:
                    club_helper.append((*player, prettify(str(o))))
                else:
                    club_helper.append((*player, str(o)))

    return club_helper


def get_players_by_position(position, pretty=True):
    player_helper: list[str] = []
    for s, p, o in g:
        # player fcf:has_position ?position
        if str(p) == fcf + "has_position":
            if str(o) == position:
                if pretty:
                    player_helper.append((prettify(str(s)), prettify(str(o))))
                else:
                    player_helper.append((str(s), str(o)))

    foot_helper = []
    for s, p, o in g:
        name = prettify(str(s)) if pretty else str(s)
        if name in dict(player_helper):
            player = next(tup for tup in player_helper if tup[0] == name)
            # player fcf:has_main_foot ?main_foot
            if str(p) == fcf + "has_main_foot":
                if pretty:
                    foot_helper.append(
                        (*player, prettify(str(o))))
                else:
                    foot_helper.append((*player, str(o)))

    country_helper = []
    for s, p, o in g:
        name = prettify(str(s)) if pretty else str(s)
        if name in dict(player_helper):
            player = next(tup for tup in foot_helper if tup[0] == name)
            # player fcf:has_birth_country ?birth_country
            if str(p) == fcf + "has_birth_country":
                if pretty:
                    country_helper.append((*player, prettify(str(o))))
                else:
                    country_helper.append((*player, str(o)))

    club_helper = []
    for s, p, o in g:
        name = prettify(str(s)) if pretty else str(s)
        if name in dict(player_helper):
            player = next(tup for tup in country_helper if tup[0] == name)
            # player fcf:has_club ?club
            if str(p) == fcf + "has_club":
                if pretty:
                    club_helper.append((*player, prettify(str(o))))
                else:
                    club_helper.append((*player, str(o)))
    return club_helper
