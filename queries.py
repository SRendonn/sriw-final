"""
Para las consultas se utilizó rdflib en vez de SPARQLWrapper, aprovechando las funciones ya existentes de la entrega 2.
Como para hacer consultas con rdflib es necesario iterar sobre todas las tripletas, se hará en cambio una traducción a SPARQL de lo que se hace en cada consulta.
"""

from rdflib import Graph

g = Graph()
g.parse("FCF.owl", format="n3")
fcf = "http://www.FCF.com/"
g = sorted(g)

""" Remueve la URI y cambia '_' por ' '

Args:
    text: str. Texto al que se le aplicará formato.

Returns:
    str
"""


def prettify(text):
    return text[19:].replace('_', ' ')


""" Retorna una lista con el nombre de todos los jugadores

Returns: Lista con el nombre de todos los jugadores
    list[str]
"""


def get_player_names():
    player_helper: list[str] = []
    for s, p, o in g:
        if str(p) == fcf + "has_position":
            player_helper.append(prettify(str(s)))
    return player_helper


""" Retorna una tupla que representa al jugador con el nombre especificado.

Args:
    name: str. Nombre del jugador que se está buscando
    pretty: bool=True. Aplicar prettify sobre la tupla 

SPARQL:
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX fcf: <http://www.fcf.com/>

    SELECT ?player, ?position, ?main_foot, ?birth_country, ?club, ?league
    WHERE {
        ?player a fcf:Football_Player .
        ?player rdfs:label args.name .
        ?player has_position ?position .
        ?player has_main_foot ?main_foot .
        ?player has_birth_country ?birth_country .
        ?player has_club ?club .
        ?club has_league ?league .
    }

Returns:
    tuple[str, str, str, str, str, str]

Example:
    ('Cristiano Ronaldo', 'Forward', 'Right Foot', 'Portugal', 'Manchester United', 'Premier League')
"""


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

    league_helper = ()
    for s, p, o in g:
        club = prettify(str(s)) if pretty else str(s)
        if str(p) == fcf + "has_league":
            if club_helper[4] == club:
                if pretty:
                    league_helper = ((*club_helper, prettify(str(o))))
                else:
                    league_helper.append((*club_helper, str(o)))
                break

    return league_helper


""" Retorna una lista de todos los jugadores como tuplas.

Args:
    pretty: bool=True. Aplicar prettify sobre la tupla 

SPARQL:
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX fcf: <http://www.fcf.com/>

    SELECT ?player, ?position, ?main_foot, ?birth_country, ?club, ?league
    WHERE {
        ?player a fcf:Football_Player .
        ?player has_position ?position .
        ?player has_main_foot ?main_foot .
        ?player has_birth_country ?birth_country .
        ?player has_club ?club .
        ?club has_league ?league .
    }

Returns:
    list[tuple[str, str, str, str, str, str]]

"""


def get_players(pretty=True):
    player_helper: list[str] = []
    for s, p, o in g:
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
            if str(p) == fcf + "has_club":
                if pretty:
                    club_helper.append((*player, prettify(str(o))))
                else:
                    club_helper.append((*player, str(o)))

    league_helper = []
    for s, p, o in g:
        club = prettify(str(s)) if pretty else str(s)
        if str(p) == fcf + "has_league":
            for player in club_helper:
                if player[4] == club:
                    if pretty:
                        league_helper.append((*player, prettify(str(o))))
                    else:
                        league_helper.append((*player, str(o)))

    return league_helper
