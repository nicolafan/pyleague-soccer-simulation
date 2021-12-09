import random

from league import Team


def get_weight(x: Team, is_home: bool) -> int:

    x_weight = x.strength_value
    x_weight += x.attack_power
    x_weight += x.defense_power
    x_weight += x.form_value

    if is_home:
        x_weight += 5

    return x_weight


def get_draw_weight(a_weight: int, b_weight: int) -> int:
    if b_weight > a_weight:
        a_weight, b_weight = b_weight, a_weight

    draw_line_x1 = 0
    draw_line_y1 = 0.4
    draw_line_x2 = 0.18
    draw_line_y2 = 0.35

    if a_weight == 0:
        return 0

    x = (a_weight - b_weight) / a_weight
    y = (draw_line_y2 - draw_line_y1) * (x - draw_line_x1) / (draw_line_x2 - draw_line_x1) + draw_line_y1

    draw_weight = ((y * a_weight) + (y * b_weight)) / (1 - y)
    return int(draw_weight)


def generate_outcome(team_a: Team, team_b: Team) -> str:
    a_weight = get_weight(team_a, is_home=True)
    b_weight = get_weight(team_b, is_home=False)
    d_weight = get_draw_weight(a_weight, b_weight)
    weights = [a_weight, d_weight, b_weight]
    outcome = random.choices(population=['1', 'X', '2'], weights=weights, k=1)[0]
    return outcome
