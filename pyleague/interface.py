import tkinter as tk
from pyleague.league import league
from PIL import ImageTk, Image

# globals
bg_color = "#121212"
primary_color = "#bc8044"
app_font = ("Inter", 12)
app_bold_font = ("Inter", 12, "bold")


class Gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.configure(background=bg_color)
        table = StandingsTable(self)
        table.pack(side="top", fill="x")
        table.set_standings()

        def next_game():
            league.generate_matchday()
            table.set_standings()

        next_game_btn = tk.Button(
            self,
            text="Next Game",
            font=app_bold_font,
            bg=primary_color,
            command=next_game,
        )
        next_game_btn.pack(pady=8)


class StandingsTable(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background=bg_color)

        self.rows = league.n_participants
        self.logos = None
        self.columns = 12
        header_titles = (
            "",
            "",
            "TEAM",
            "",
            "Pts",
            "PG",
            "W",
            "D",
            "L",
            "GF",
            "GA",
            "DIFF",
        )
        # use black background so it "peeks through" to
        # form grid lines

        self._widgets = []

        self.column_widths = (3, 3, 30, 20, 5, 5, 5, 5, 5, 5, 5, 5)

        for column in range(self.columns):
            anchor = tk.CENTER
            if column == 2:
                anchor = tk.W
            label = tk.Label(
                self,
                text=header_titles[column],
                borderwidth=0,
                width=self.column_widths[column],
                anchor=anchor,
                font=app_bold_font,
                bg=primary_color,
            )
            label.grid(row=0, column=column, sticky="nsew")

        for row in range(1, self.rows + 1):
            row_color = "#202020"
            if row % 2 == 1:
                row_color = "#383838"

            current_row = []
            for column in range(self.columns):
                anchor = tk.CENTER
                if 2 <= column <= 3:
                    anchor = tk.W
                if column == 0:
                    frame = tk.Frame(
                        self, width=self.column_widths[column], bg=row_color
                    )
                    frame.grid(row=row, column=column, sticky="nsew")
                    widget = tk.Label(
                        frame,
                        bg="grey",
                        text="%s/%s" % (row, column),
                        borderwidth=0,
                        font=app_bold_font,
                        fg="white",
                    )
                    widget.pack(fill="x", padx=4, pady=4)
                    current_row.append(widget)
                elif column == 3:
                    frame = tk.Frame(
                        self, width=self.column_widths[column], bg=row_color
                    )
                    frame.grid(row=row, column=column, sticky="nsew")
                    for i in range(5):
                        label = tk.Label(
                            frame,
                            bg=row_color,
                            text="",
                            borderwidth=0,
                            font=app_bold_font,
                            fg="white",
                            width=3,
                        )
                        label.pack(side=tk.LEFT, padx=4, pady=4)
                        current_row.append(label)
                else:
                    widget = tk.Label(
                        self,
                        text="%s/%s" % (row, column),
                        borderwidth=0,
                        width=self.column_widths[column],
                        bg=row_color,
                        fg="white",
                        font=app_font,
                        anchor=anchor,
                    )
                    widget.grid(row=row, column=column, sticky="nsew")
                    current_row.append(widget)
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

            # print team-name
            widget = self._widgets[i][2]
            widget.configure(text=team.name)

            # print team-form
            results = team.last_results.copy()
            results.reverse()
            for j in range(len(results)):
                widget = self._widgets[i][3 + j]
                widget.configure(text=results[j])
                color = "green"
                if results[j] == "D":
                    color = "grey"
                elif results[j] == "L":
                    color = "red"
                widget.configure(bg=color, font=app_bold_font)

            # print team-data
            goal_difference = participant.goals_scored - participant.goals_conceded
            if goal_difference > 0:
                goal_difference = "+" + str(goal_difference)

            team_data = (
                participant.points,
                league.matchday,
                participant.wins,
                participant.draws,
                participant.losses,
                participant.goals_scored,
                participant.goals_conceded,
                goal_difference,
            )

            for j in range(8, len(self._widgets[0])):
                widget = self._widgets[i][j]
                widget.configure(text=team_data[j - 8])
                if j == 8:
                    widget.configure(fg=primary_color, font=app_bold_font)


gui = Gui()
gui.mainloop()
