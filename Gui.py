import tkinter as tk

from sys import setrecursionlimit
setrecursionlimit(50000)

def gui_main(sequence_of_states):

    root = tk.Tk()
    root.title("States interface")

    canvas_width = 300
    canvas_height = 600

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack(side=tk.LEFT, fill=tk.Y)

    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    block_color = "blue"
    block_size = 30
    space_above_first_gui = 50
    space_below_last_gui = 50
    space_between_guis = 20

    x_offset = 70
    total_height = space_above_first_gui  # Add space above the first GUI

    canvas.delete("all")
    for gui_obj in sequence_of_states:
        l1 = gui_obj.l1
        l2 = gui_obj.l2
        h1 = gui_obj.h1
        h2 = gui_obj.h2

        # Draw table as sticks
        table_color = "brown"
        table_thickness = 10
        canvas.create_rectangle(x_offset, total_height + 17 * block_size, x_offset + 150,
                                total_height + 17 * block_size + table_thickness, fill=table_color)

        for i, block in enumerate(l1):
            x = block_size + x_offset
            if i == len(l1) - 1:
                if block == "h1":
                    hand(canvas, "green", h1, x, total_height)
                else:
                    hand(canvas, "yellow", h2, x, total_height)
                break

            y = total_height + (16 - i) * block_size
            canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=block_color)
            canvas.create_text(x + block_size / 2, y + block_size / 2, text=block, fill="white")
        for i, block in enumerate(l2):
            x = 3 * block_size + x_offset
            if i == len(l2) - 1:
                if block == "h1":
                    hand(canvas, "green", h1, x, total_height)
                else:
                    hand(canvas, "yellow", h2, x, total_height)
                break

            y = total_height + (16 - i) * block_size
            canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=block_color)
            canvas.create_text(x + block_size / 2, y + block_size / 2, text=block, fill="white")

    # Add space below the last GUI
        total_height += 17*block_size+table_thickness+space_between_guis

    total_height += space_below_last_gui
    canvas.configure(scrollregion=(0, 0, canvas_width, total_height))

    root.mainloop()


def hand(canvas, hand_color, block_name, x, total_height):
    hand_x = x+15
    hand_y = total_height+3*30
    canvas.create_line(hand_x - 30, hand_y, hand_x, hand_y - 30, fill=hand_color, width=2)
    canvas.create_line(hand_x + 30, hand_y, hand_x, hand_y - 30, fill=hand_color, width=2)
    if block_name != "":
        y = hand_y-15
        block_size = 30
        block_color = "blue"
        canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=block_color)
        canvas.create_text(x + block_size / 2, y + block_size / 2, text=block_name, fill="white")
