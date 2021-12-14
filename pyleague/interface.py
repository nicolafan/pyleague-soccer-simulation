import tkinter as tk
from pyleague.league import league
from PIL import ImageTk, Image

# globals
bg_color = '#121212'
primary_color = '#bc8044'


class Gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.configure(background=bg_color)
        t = StandingsTable(self)
        t.pack(side="top", fill="x")
        t.set_standings()


class StandingsTable(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background=bg_color)

        self.rows = league.n_participants
        self.logos = None
        self.columns = 12
        header_titles = ('', '', 'TEAM', '', 'Pts', 'PG', 'W', 'D', 'L', 'GF', 'GA', 'DIFF')
        self.header_font = ('Inter', 12, 'bold')
        self.row_font = ('Inter', 12)
        # use black background so it "peeks through" to
        # form grid lines

        self._widgets = []

        column_widths = (3, 3, 30, 20, 5, 5, 5, 5, 5, 5, 5, 5)

        for column in range(self.columns):
            anchor = tk.CENTER
            if column == 2:
                anchor = tk.W
            label = tk.Label(self, text=header_titles[column],
                             borderwidth=0, width=column_widths[column],
                             anchor=anchor, font=self.header_font, bg=primary_color)
            label.grid(row=0, column=column, sticky='nsew')

        for row in range(1, self.rows + 1):
            row_color = '#202020'
            if row % 2 == 1:
                row_color = '#383838'

            current_row = []
            for column in range(self.columns):
                anchor = tk.CENTER
                if 2 <= column <= 3:
                    anchor = tk.W
                label = tk.Label(self, text="%s/%s" % (row, column),
                                 borderwidth=0, width=column_widths[column],
                                 bg=row_color, fg='white', font=self.row_font, anchor=anchor)
                label.grid(row=row, column=column, sticky="nsew")
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)

    def set_standings(self):
        standings = league.get_standings()
        self.logos = []
        for i in range(len(standings)):
            participant = standings[i]
            team = participant.team

            # print position
            widget = self._widgets[i][0]
            widget.configure(text=i + 1)

            # print team-image
            widget = self._widgets[i][1]
            img = Image.open("../logos/" + team.identifier + ".png")
            img = img.resize((20, 20), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.logos.append(img)
            widget.configure(image=img)

            goal_difference = participant.goals_scored - participant.goals_conceded
            if goal_difference > 0:
                goal_difference = '+' + str(goal_difference)

            team_data = ('', '', team.name, team.form_value, participant.points, league.matchday,
                         participant.wins, participant.draws, participant.losses,
                         participant.goals_scored, participant.goals_conceded, goal_difference)

            for j in range(2, self.columns):
                widget = self._widgets[i][j]
                widget.configure(text=team_data[j])


gui = Gui()
gui.mainloop()
