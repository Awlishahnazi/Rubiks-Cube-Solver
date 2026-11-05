import random
import threading
from collections import deque
import tkinter as tk
from tkinter import messagebox

Colors = ['white', 'red', 'green', 'yellow', 'orange', 'blue']
Rotates = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]

class RubiksCube:
    def __init__(self, size=3):
        self.size = size
        self.state = {color: [[color] * size for _ in range(size)] for color in Colors}

    def apply_move(self, move):
        def rotate_clockwise(face):
            return [list(row) for row in zip(*face[::-1])]

        def rotate_counterclockwise(face):
            return [list(row) for row in zip(*face)][::-1]

        if move == "U":
            self.state['white'] = rotate_clockwise(self.state['white'])
            temp = self.state['green'][0][:]
            self.state['green'][0] = self.state['red'][0]
            self.state['red'][0] = self.state['blue'][0]
            self.state['blue'][0] = self.state['orange'][0]
            self.state['orange'][0] = temp
        elif move == "U'":
            self.state['white'] = rotate_counterclockwise(self.state['white'])
            temp = self.state['green'][0][:]
            self.state['green'][0] = self.state['orange'][0]
            self.state['orange'][0] = self.state['blue'][0]
            self.state['blue'][0] = self.state['red'][0]
            self.state['red'][0] = temp
        elif move == "D":
            self.state['yellow'] = rotate_clockwise(self.state['yellow'])
            temp = self.state['green'][-1][:]
            self.state['green'][-1] = self.state['orange'][-1]
            self.state['orange'][-1] = self.state['blue'][-1]
            self.state['blue'][-1] = self.state['red'][-1]
            self.state['red'][-1] = temp
        elif move == "D'":
            self.state['yellow'] = rotate_counterclockwise(self.state['yellow'])
            temp = self.state['green'][-1][:]
            self.state['green'][-1] = self.state['red'][-1]
            self.state['red'][-1] = self.state['blue'][-1]
            self.state['blue'][-1] = self.state['orange'][-1]
            self.state['orange'][-1] = temp
        elif move == "L":
            self.state['orange'] = rotate_clockwise(self.state['orange'])
            temp = [row[0] for row in self.state['white']]
            for i in range(self.size):
                self.state['white'][i][0] = self.state['blue'][self.size - 1 - i][-1]
                self.state['blue'][self.size - 1 - i][-1] = self.state['yellow'][i][0]
                self.state['yellow'][i][0] = self.state['green'][i][0]
                self.state['green'][i][0] = temp[i]
        elif move == "L'":
            self.state['orange'] = rotate_counterclockwise(self.state['orange'])
            temp = [row[0] for row in self.state['white']]
            for i in range(self.size):
                self.state['white'][i][0] = self.state['green'][i][0]
                self.state['green'][i][0] = self.state['yellow'][i][0]
                self.state['yellow'][i][0] = self.state['blue'][self.size - 1 - i][-1]
                self.state['blue'][self.size - 1 - i][-1] = temp[i]
        elif move == "R":
            self.state['red'] = rotate_clockwise(self.state['red'])
            temp = [row[-1] for row in self.state['white']]
            for i in range(self.size):
                self.state['white'][i][-1] = self.state['green'][i][-1]
                self.state['green'][i][-1] = self.state['yellow'][i][-1]
                self.state['yellow'][i][-1] = self.state['blue'][self.size - 1 - i][0]
                self.state['blue'][self.size - 1 - i][0] = temp[i]
        elif move == "R'":
            self.state['red'] = rotate_counterclockwise(self.state['red'])
            temp = [row[-1] for row in self.state['white']]
            for i in range(self.size):
                self.state['white'][i][-1] = self.state['blue'][self.size - 1 - i][0]
                self.state['blue'][self.size - 1 - i][0] = self.state['yellow'][i][-1]
                self.state['yellow'][i][-1] = self.state['green'][i][-1]
                self.state['green'][i][-1] = temp[i]
        elif move == "F":
            self.state['green'] = rotate_clockwise(self.state['green'])
            temp = self.state['white'][-1][:]
            self.state['white'][-1] = [row[0] for row in self.state['orange']][::-1]
            for i in range(self.size):
                self.state['orange'][i][0] = self.state['yellow'][0][i]
            self.state['yellow'][0] = [row[-1] for row in self.state['red']][::-1]
            for i in range(self.size):
                self.state['red'][i][-1] = temp[i]
        elif move == "F'":
            self.state['green'] = rotate_counterclockwise(self.state['green'])
            temp = self.state['white'][-1][:]
            self.state['white'][-1] = [row[-1] for row in self.state['red']]
            for i in range(self.size):
                self.state['red'][i][-1] = self.state['yellow'][0][::-1][i]
            self.state['yellow'][0] = [row[0] for row in self.state['orange']]
            for i in range(self.size):
                self.state['orange'][i][0] = temp[::-1][i]
        elif move == "B":
            self.state['blue'] = rotate_clockwise(self.state['blue'])
            temp = self.state['white'][0][:]
            self.state['white'][0] = [row[-1] for row in self.state['red']]
            for i in range(self.size):
                self.state['red'][i][-1] = self.state['yellow'][-1][::-1][i]
            self.state['yellow'][-1] = [row[0] for row in self.state['orange']]
            for i in range(self.size):
                self.state['orange'][i][0] = temp[::-1][i]
        elif move == "B'":
            self.state['blue'] = rotate_counterclockwise(self.state['blue'])
            temp = self.state['white'][0][:]
            self.state['white'][0] = [row[0] for row in self.state['orange']][::-1]
            for i in range(self.size):
                self.state['orange'][i][0] = self.state['yellow'][-1][i]
            self.state['yellow'][-1] = [row[-1] for row in self.state['red']][::-1]
            for i in range(self.size):
                self.state['red'][i][-1] = temp[i]

    def is_solved(self):
        return all(all(row == [color] * self.size for row in grid) for color, grid in self.state.items())

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move

    def reconstruct_path(self):
        path = []
        current = self
        while current.parent is not None:
            path.append(current.move)
            current = current.parent
        return path[::-1]

def depth_limited_search(cube, limit):
    def recursive_dls(node, depth):
        current_cube = RubiksCube(cube.size)
        current_cube.state = {face: [row[:] for row in rows] for face, rows in node.state.items()}

        if current_cube.is_solved():
            return node.reconstruct_path()
        if depth == 0:
            return None

        for move in Rotates:
            new_cube = RubiksCube(cube.size)
            new_cube.state = {face: [row[:] for row in rows] for face, rows in current_cube.state.items()}
            new_cube.apply_move(move)
            child_node = Node(new_cube.state, node, move)
            result = recursive_dls(child_node, depth - 1)
            if result is not None:
                return result
        return None

    return recursive_dls(Node(cube.state), limit)

def iterative_deepening_search(cube, update_ui_callback = None):
    depth = 0
    while True:
        result = depth_limited_search(cube, depth)
        if result is not None:
            return result
        depth += 1

class RubiksCubeUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rubik's Cube Solver")

        self.start_button = tk.Button(self.root, text="Start", command=self.start, font=("Arial", 16), relief="solid", width=15, height=2)
        self.start_button.pack(pady=10)

        self.scramble_button = None
        self.solve_button = None
        self.cube_frame = tk.Frame(self.root)
        self.cube_frame.pack(fill="both", expand=True)

        self.manual_controls_frame = None
        self.cube = RubiksCube()

        self.loading_label = None

    def start(self):
        self.start_button.pack_forget()

        # Split the screen into two halves
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Left half for Rubik's Cube visualization
        self.left_frame = tk.Frame(main_frame, width=self.root.winfo_screenwidth() // 2)
        self.left_frame.pack(side="left", fill="both", expand=True)

        # Right half for manual controls
        self.right_frame = tk.Frame(main_frame, width=self.root.winfo_screenwidth() // 2)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Scramble and solve buttons
        button_frame = tk.Frame(self.right_frame)
        button_frame.pack(pady=10, fill="x")

        self.scramble_button = tk.Button(button_frame, text="Scramble Cube", command=self.scramble_cube, font=("Arial", 14), relief="solid",bg="#f5d442", activebackground="#f5ce42",border=2, width=20, height=2,bd="3")
        self.scramble_button.grid(row=0, column=0, padx=5, pady=10)

        self.solve_button = tk.Button(button_frame, text="Solve Cube", command=self.solve_cube, font=("Arial", 14), relief="solid",bg="#42f593", activebackground="#42f5bc", width=20, height=2, bd="3")
        self.solve_button.grid(row=0, column=1, padx=10, pady=10)

        # Add manual controls for rotating faces
        self.manual_controls_frame = tk.Frame(self.right_frame)
        self.manual_controls_frame.pack(pady=10, fill="x")

        # Create the manual rotation buttons
        self.create_manual_controls()

        # Update the cube visualization on the left side
        self.update_ui()

    def create_manual_controls(self):
        moves = [
            ("U", "Up"), ("U'", "Up'"), ("D", "Down"), ("D'", "Down'"),
            ("L", "Left"), ("L'", "Left'"), ("R", "Right"), ("R'", "Right'"),
            ("F", "Front"), ("F'", "Front'"), ("B", "Back"), ("B'", "Back'")
        ]
        
        # Removed the canvas and scrollbar section to save space
        manual_controls_inner_frame = tk.Frame(self.manual_controls_frame)

        for i, (move, name) in enumerate(moves):
            button = tk.Button(manual_controls_inner_frame, text=name, command=lambda m=move: self.apply_manual_move(m), font=("Arial", 12), bg="light gray", width=12, height=2)
            button.grid(row=i // 3, column=i % 3, padx=20, pady=10)

        manual_controls_inner_frame.pack(pady=10, fill="x")


    def apply_manual_move(self, move):
        self.cube.apply_move(move)
        self.update_ui()  

    def scramble_cube(self):
        scramble_moves = random.choices(Rotates, k=6)
        for move in scramble_moves:
            self.cube.apply_move(move)

        messagebox.showinfo("Scramble", f"Cube has been scrambled!\nMoves: {' '.join(scramble_moves)}")
        self.update_ui()

    def solve_cube(self):
        if self.cube.is_solved():
            messagebox.showinfo("Solution", "The cube is already solved!")
            return

        self.loading_label = tk.Label(self.root, text="Solving... Please wait...", font=("Arial", 14))
        self.loading_label.pack()

        self.solve_button.config(state="disabled")

        def update_ui_real_time(cube):
            self.cube = cube
            self.update_ui()

        def solve_in_thread():
            solution = iterative_deepening_search(self.cube, update_ui_real_time)
            if solution:
                for move in solution:
                    self.cube.apply_move(move)
                messagebox.showinfo("Solution", f"Solution found!\nMoves: {' '.join(solution)}")
            else:
                messagebox.showerror("Error", "No solution found.")

            self.loading_label.destroy()
            self.solve_button.config(state="normal")
            self.update_ui()

        threading.Thread(target=solve_in_thread).start()

    def update_ui(self):
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        face_grid = tk.Frame(self.left_frame, bg="#333333")
        face_grid.pack(pady=5, fill="both", expand=True)

        color_map = {
            'white': "#FFFFFF",
            'red': "#FF0000",
            'green': "#00FF00",
            'yellow': "#FFFF00",
            'orange': "#FFA500",
            'blue': "#0000FF"
        }

        white_frame = tk.Frame(face_grid, bg="#333333")
        white_frame.grid(row=0, column=1)  
        self._create_face_ui(white_frame, 'white', color_map)

        middle_frame = tk.Frame(face_grid, bg="#333333")
        middle_frame.grid(row=1, column=0, columnspan=4)  
        for idx, face in enumerate(['orange', 'green', 'red', 'blue']):
            frame = tk.Frame(middle_frame, bg="#333333", padx=10, pady=10)
            frame.grid(row=0, column=idx)
            self._create_face_ui(frame, face, color_map)

        yellow_frame = tk.Frame(face_grid, bg="#333333")
        yellow_frame.grid(row=2, column=1)  
        self._create_face_ui(yellow_frame, 'yellow', color_map)

    def _create_face_ui(self, parent_frame, face, color_map):
        face_label = tk.Label(parent_frame, text=f"{face.capitalize()} face:", font=("Arial", 14, "bold"), bg="#333333", fg="white")
        face_label.pack(pady=5)

        for row in self.cube.state[face]:
            row_frame = tk.Frame(parent_frame, bg="#333333")
            row_frame.pack()
            for cell in row:
                cell_label = tk.Label(
                    row_frame,
                    bg=color_map[cell],
                    width=6,
                    height=3,
                    borderwidth=2,
                    relief="solid",
                    highlightbackground="black",
                    highlightthickness=1
                )
                cell_label.pack(side="left", padx=1, pady=1)

    def run(self):
        self.root.mainloop()

def main():
    ui = RubiksCubeUI()
    ui.run()

if __name__ == "__main__":
    main()