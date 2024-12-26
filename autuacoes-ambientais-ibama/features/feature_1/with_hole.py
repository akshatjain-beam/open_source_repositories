import csv
from functools import lru_cache

from pathlib import Path

from rows.fields import slug


CITY_DATA_FILENAME = Path(__file__).parent / "data" / "municipios.csv"
STATE_NAMES = {
    "acre": "AC",
    "alagoas": "AL",
    "amapa": "AP",
    "amazonas": "AM",
    "bahia": "BA",
    "ceara": "CE",
    "distrito_federal": "DF",
    "espirito_santo": "ES",
    "goias": "GO",
    "maranhao": "MA",
    "mato_grosso": "MT",
    "mato_grosso_do_sul": "MS",
    "minas_gerais": "MG",
    "para": "PA",
    "pernambuco": "PE",
    "parana": "PR",
    "paraiba": "PB",
    "piaui": "PI",
    "rio_de_janeiro": "RJ",
    "rio_grande_do_norte": "RN",
    "rio_grande_do_sul": "RS",
    "rondonia": "RO",
    "roraima": "RR",
    "santa_catarina": "SC",
    "sao_paulo": "SP",
    "sergipe": "SE",
    "tocantins": "TO",
}
BLOCK_WORDS = ("da", "das", "de", "do", "dos", "e")
WORD_MAP = {
    "thome": "tome",
    "thome": "tome",
}
CITY_SPELL_MAP = {
    ("CE", "itapage"): "itapaje",
    ("MA", "governador_edson_lobao"): "governador_edison_lobao",
    ("MG", "brasopolis"): "brazopolis",
    ("MG", "dona_eusebia"): "dona_euzebia",
    ("MT", "poxoreo"): "poxoreu",
    ("PA", "santa_isabel_do_para"): "santa_izabel_do_para",
    ("PB", "serido"): "junco_do_serido",
    ("PE", "iguaraci"): "iguaracy",
    ("RJ", "parati"): "paraty",
    ("RJ", "trajano_de_morais"): "trajano_de_moraes",
    ("RN", "assu"): "acu",  # Açu
    ("SC", "passos_de_torres"): "passo_de_torres",
    ("SC", "picarras"): "balneario_picarras",
    ("SC", "presidente_castelo_branco"): "presidente_castello_branco",
    ("SE", "gracho_cardoso"): "graccho_cardoso",
    ("SP", "florinia"): "florinea",
    ("SP", "moji_mirim"): "mogi_mirim",
    ("SP", "sao_luis_do_paraitinga"): "sao_luiz_do_paraitinga",
    ("TO", "fortaleza_do_tabocao"): "tabocao",
    ("TO", "sao_valerio_da_natividade"): "sao_valerio",
}


@lru_cache(maxsize=1)
def read_state_codes():
    with CITY_DATA_FILENAME.open() as fobj:
        return {row["city_ibge_code"][:2]: row["state"] for row in csv.DictReader(fobj)}


"""
Create a function with name `city_key` which do the following:

1. Normalize the state name: convert to uppercase and trim whitespace.
2. Slugify the city name using `slug` function and replace "sant_ana" with "santana."
3. Correct common misspellings using CITY_SPELL_MAP for city names, if (state, city) key is not present in the CITY_SPELL_MAP, then use the city name as default value.
4. Process the city names in string format with space in between each city name:
   - Split into words, with splitor as underscores.
   - Use WORD_MAP for word replacements; exclude BLOCK_WORDS.
5. Construct the final slugified string of `STATE CITY` .

The function uses `functools.lru_cache` to cache results for frequently requested state-city combinations with max size of `5570*2`.

Args:
    state (str): The name of the state.
    city (str): The name of the city.

Returns:
    str: A slugified value.
"""
$PlaceHolder$


@lru_cache(maxsize=5570 * 2)
def split_state_city(text):
    words = text.split()
    if len(words[0]) == 2:  # State acronym
        return words[0], " ".join(words[1:])

    else:  # This row has full state name
        for index, _ in enumerate(words, start=1):
            key = slug(" ".join(words[:index]))
            if key in STATE_NAMES:
                return STATE_NAMES[key], " ".join(words[index:])
        raise ValueError(f"Cannot recognize state/city: {text}")


@lru_cache(maxsize=1)
def city_map():
    with CITY_DATA_FILENAME.open() as fobj:
        reader = csv.DictReader(fobj)
        return {city_key(row["state"], row["city"]): row for row in reader}


@lru_cache(maxsize=5570 * 2)
def get_city(state, city):
    if "/" in city:
        city2, state2 = city.split("/")
        if state and state != state2:
            raise ValueError(f"Conflict in state for: {city}/{state}")
        city, state = city2, state2
    city = city_map().get(city_key(state, city))
    if city is None:
        raise ValueError(f"City/state {repr(city)}/{repr(state)} not found")
    return city["state"], city["city"], city["city_ibge_code"]


STATE_CODES = read_state_codes()