from src.abnf1.grammars.rfc2616 import Rule


def test_token():
    # exercise rule imported by hand from RFC 2616.
    src = "token"
    assert Rule("token").parse_all(src)
