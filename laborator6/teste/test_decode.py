from arsenal.forensics.decode import desfa


def test_base64():
    strat, rezultat = desfa("U2FsdXQ=")

    assert strat == "base64"
    assert rezultat == b"Salut"