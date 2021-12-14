import random
import string

import pyleague.models


def get_random_string(length: int) -> str:
    letters = string.ascii_letters
    digits = string.digits

    return "".join(random.choice(letters.join(digits)) for i in range(length))


def get_random_team():
    identifier = get_random_string(3)
    name = get_random_string(10)
    sv = random.randint(15, 100)
    ap = random.randint(1, 40)
    dp = random.randint(1, 40)

    team = pyleague.models.Team(identifier, name, sv, ap, dp)
    return team
