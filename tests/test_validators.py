import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.validators import validate_username, validate_guess

def test_valid_usernames():
    assert validate_username("Alice123")
    assert validate_username("Bob42")
    assert not validate_username("a")            # too short
    assert not validate_username("user@")        # special character
    assert not validate_username("user name")    # space

def test_valid_guesses():
    assert validate_guess("0123")
    assert validate_guess("3450")
    assert not validate_guess("012")
    assert not validate_guess("01234")
    assert not validate_guess("0122")
    assert not validate_guess("0678")
    assert not validate_guess("abcd")
