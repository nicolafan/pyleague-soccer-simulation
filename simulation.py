import random

teams = {}


def get_weight(x, is_home):
    x = teams[x]

    x_weight = x['sv']
    x_weight += x['ap']
    x_weight += x['dp']
    x_weight += x['lr']

    if is_home:
        x_weight += 5

    return x_weight


def get_draw_weight(a_weight, b_weight):
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

    print(y)
    draw_weight = ((y * a_weight) + (y * b_weight)) / (1 - y)
    print(draw_weight)
    return draw_weight


def generate_outcome(a_weight, b_weight):
    d_weight = get_draw_weight(a_weight, b_weight)
    weights = [a_weight, d_weight, b_weight]
    print(weights)
    outcome = random.choices(population=['1', 'X', '2'], weights=weights, k=1)
    print(outcome)
    return outcome


def setup_teams():
    team = ('INT',
            {
                'name': 'Inter',
                'sv': 30,
                'ap': 10,
                'dp': 6,
                'lr': 0
            })
    teams[team[0]] = team[1]
    team = ('JUV',
            {
                'name': 'Juventus',
                'sv': 23,
                'ap': 6,
                'dp': 8,
                'lr': 0
            })
    teams[team[0]] = team[1]
    team = ('SAL',
            {
                'name': 'Salernitana',
                'sv': 2,
                'ap': 2,
                'dp': 2,
                'lr': 0
            })
    teams[team[0]] = team[1]


def main():
    setup_teams()
    outcomes = ""
    for i in range(100000):
        a_weight = get_weight('SAL', True)
        b_weight = get_weight('JUV', False)
        outcomes += generate_outcome(a_weight, b_weight)[0]

    cnt_1 = 0
    cnt_2 = 0
    cnt_X = 0

    for c in outcomes:
        if c == '1':
            cnt_1 += 1
        if c == '2':
            cnt_2 += 1
        if c == 'X':
            cnt_X += 1

    print("1: " + str(cnt_1) + " 2: " + str(cnt_2) + " X: " + str(cnt_X))


if __name__ == '__main__':
    main()
