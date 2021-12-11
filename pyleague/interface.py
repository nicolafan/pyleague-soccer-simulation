import tkinter as tk
from tkinter import font

gui = tk.Tk()
gui_width = 1024
gui_height = 512
bg_color = '#121212'


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
    canvas.create_text(64, 11, text=cols[0], font=header_font)
    dist = 0
    for i in range(1, len(cols)):
        canvas.create_text(512 + dist, 11, text=cols[i], font=header_font)
        dist += 64

    # drawing rows
    y_top = row_height
    for i in range(20):
        row_color = '#202020'
        if i % 2 == 1:
            row_color = '#383838'
        canvas.create_rectangle(0, y_top, gui_width, y_top + row_height, fill=row_color, outline='')

        # team data in row

        # standing position
        canvas.create_rectangle(6, y_top + 2, 26.5, y_top + 20, fill='white', outline='')
        canvas.create_text(16, y_top + 11, text='{0}'.format(i+1), fill='black', font=row_font)

        # team name
        canvas.create_text(112, y_top + 11, text='Fake Team                     ', fill='white')
        y_top += row_height

    canvas.pack()


def main():
    gui.geometry('1024x512')
    gui.resizable(False, False)
    gui.configure(bg=bg_color)

    show_standings()
    gui.mainloop()


if __name__ == '__main__':
    main()
