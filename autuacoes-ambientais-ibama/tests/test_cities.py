from autuacoes.cities import city_key

def test_city_key_standard():
    """
    Tests standard cases where city names are mapped correctly
    according to the CITY_SPELL_MAP. The expectation is that the
    function returns the correct standardized key for the given
    state and city names.
    """
    assert city_key("CE", "itapage") == "ce_itapaje"
    assert city_key("MA", "governador_edson_lobao") == "ma_governador_edison_lobao"
    assert city_key("MG", "brasopolis") == "mg_brazopolis"
    assert city_key("RJ", "parati") == "rj_paraty"

def test_city_key_with_mappings():
    """
    Tests cases where city names should be transformed using
    the CITY_SPELL_MAP to correct common misspellings.
    The expectation is that the function applies these corrections.
    """
    assert city_key("CE", "itapage") == "ce_itapaje"
    assert city_key("MG", "dona_eusebia") == "mg_dona_euzebia"
    assert city_key("MT", "poxoreo") == "mt_poxoreu"

def test_city_key_with_block_words():
    """
    Tests cases where block words are present in the city name.
    The expectation is that the function removes these block words
    from the city name before slugifying.
    """
    assert city_key("SP", "sao_luis_do_paraitinga") == "sp_sao_luiz_paraitinga"
    assert city_key("TO", "sao_valerio_da_natividade") == "to_sao_valerio"

def test_city_key_edge_cases():
    """
    Tests edge cases with extra spaces and mixed capitalization
    in the input. The expectation is that the function handles
    these cases correctly by trimming spaces and normalizing the
    case.
    """
    assert city_key("  rj  ", " parati ") == "rj_paraty"
    assert city_key("mg", " brasopolis ") == "mg_brazopolis"
    assert city_key("Sc", " passOs_de_torres  ") == "sc_passo_torres"

def test_city_key_empty_input():
    """
    Tests cases with empty state and city inputs. The expectation
    is that the function returns an empty string in these cases.
    """
    assert city_key("", "") == ""
    assert city_key("  ", "  ") == ""

def test_city_key_only_state():
    """
    Tests cases where only the state is provided and the city is
    empty. The expectation is that the function returns the slugified
    state name without any city component.
    """
    assert city_key("SP", "") == "sp"
    assert city_key("RJ", "   ") == "rj"

def test_city_key_only_city():
    """
    Tests cases where only the city is provided and the state is
    empty. The expectation is that the function returns the slugified
    city name without any state component.
    """
    assert city_key("", "moji_mirim") == "moji_mirim"
    assert city_key("   ", "new_york") == "new_york"

def test_city_key_unmapped_city():
    """
    Tests cases for cities that are not present in the CITY_SPELL_MAP.
    The expectation is that the function returns the default slugified
    form of the state and city names.
    """
    assert city_key("WA", "seattle") == "wa_seattle"
    assert city_key("OR", "portland") == "or_portland"