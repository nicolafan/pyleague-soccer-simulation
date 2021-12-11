import tkinter as tk
from tkinter import font, PhotoImage
from PIL import ImageTk, Image

from pyleague.league import league

gui = tk.Tk()
gui_width = 1024
gui_height = 512
bg_color = '#121212'

logos = []


def show_standings():
    cols = ('TEAM', 'Pts', 'PG', 'W', 'D', 'L', 'GF', 'GA', 'DIFF')
    header_font = ('Inter', 12, 'bold')
    row_font = ('Inter', 12)
    canvas_height = 462
    row_height = 22
    canvas = tk.Canvas(gui, width=gui_width, height=canvas_height, bg=bg_color)
    canvas.configure(borderwidth=0, highlightthickness=0)

    # drawing header
    canvas.create_rectangle(0, 0, gui_width, row_height, fill='#bc8044', outline='')
    canvas.create_text(40, 11, text=cols[0], anchor='w', font=header_font)
    dist = 0
    for i in range(1, len(cols)):
        canvas.create_text(512 + dist, 11, text=cols[i], font=header_font)
        dist += 64

    # drawing rows
    y_top = row_height
    standings = league.get_standings()
    for i in range(20):
        row_color = '#202020'
        if i % 2 == 1:
            row_color = '#383838'
        canvas.create_rectangle(0, y_top, gui_width, y_top + row_height, fill=row_color, outline='')

        # team data in row
        participant = standings[i]
        team = participant.team

        # standing position
        canvas.create_rectangle(6, y_top + 2, 26.5, y_top + 20, fill='white', outline='')
        canvas.create_text(16, y_top + 11, text='{0}'.format(i + 1), fill='black', font=row_font)

        # team image
        img = Image.open('../logos/' + team.identifier + '.png')
        img = img.resize((18, 18))
        team_image = ImageTk.PhotoImage(img)
        logos.append(team_image)
        canvas.create_image(40, y_top + 11, image=team_image, anchor='w')

        # team name
        canvas.create_text(66, y_top + 11, text=team.name, anchor='w', fill='white')

        # team points
        dist = 0
        canvas.create_text(512, y_top + 11, text=participant.points, fill='white')
        dist += 64
        canvas.create_text(512 + dist, y_top + 11, text=league.matchday, fill='white')
        dist += 64
        canvas.create_text(512 + dist, y_top + 11, text=participant.wins, fill='white')
        dist += 64
        canvas.create_text(512 + dist, y_top + 11, text=participant.draws, fill='white')
        dist += 64
        canvas.create_text(512 + dist, y_top + 11, text=participant.losses, fill='white')
        dist += 64
        canvas.create_text(512 + dist, y_top + 11, text=participant.goals_scored, fill='white')
        dist += 64
        canvas.create_text(512 + dist, y_top + 11, text=participant.goals_scored, fill='white')
        dist += 64
        goal_difference = participant.goals_scored - participant.goals_conceded
        if goal_difference > 0:
            goal_difference = '+' + str(goal_difference)
        canvas.create_text(512 + dist, y_top + 11, text=goal_difference, fill='white')
        y_top += row_height

    canvas.pack()


gui.geometry('1024x512')
gui.resizable(False, False)
gui.configure(bg=bg_color)

show_standings()
gui.mainloop()
