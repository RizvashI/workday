# validators.py (input validation functions)
import re

# Validate that the username is 3–20 characters: letters and digits only
def validate_username(name):
    return bool(re.fullmatch(r"[A-Za-z0-9]{3,20}", name))

# Validate that the guess is a 4-digit string with unique digits from 0–5
def validate_guess(guess):
    return (
        isinstance(guess, str)
        and len(guess) == 4
        and guess.isdigit()
        and all(d in "012345" for d in guess)
        and len(set(guess)) == 4
    )
