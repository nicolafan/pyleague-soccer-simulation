import random

from . import models


def get_weight(x: models.Team, is_home: bool) -> int:

    x_weight = x.strength_value
    x_weight += x.attack_power
    x_weight += x.defense_power
    x_weight += x.form_value

    if is_home:
        x_weight += 20

    return x_weight


def get_draw_weight(a_weight: int, b_weight: int) -> int:
    if b_weight > a_weight:
        a_weight, b_weight = b_weight, a_weight

    draw_line_x1 = 0
    draw_line_y1 = 0.35
    draw_line_x2 = 0.18
    draw_line_y2 = 0.3

    if a_weight == 0:
        return 0

    x = (a_weight - b_weight) / a_weight
    y = (draw_line_y2 - draw_line_y1) * (x - draw_line_x1) / (draw_line_x2 - draw_line_x1) + draw_line_y1

    draw_weight = ((y * a_weight) + (y * b_weight)) / (1 - y)
    return int(draw_weight)


def generate_outcome(team_a: models.Team, team_b: models.Team) -> str:
    a_weight = get_weight(team_a, is_home=True)
    b_weight = get_weight(team_b, is_home=False)
    d_weight = get_draw_weight(a_weight, b_weight)
    weights = [a_weight, d_weight, b_weight]
    outcome = random.choices(population=['1', 'X', '2'], weights=weights, k=1)[0]
    if outcome == '1':
        team_a.add_win()
        team_b.add_loss()
    elif outcome == '2':
        team_a.add_loss()
        team_b.add_win()
    else:
        team_a.add_draw()
        team_b.add_draw()
    return outcome
