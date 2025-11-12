import tkinter
from tkinter import *
from tkinter import messagebox
import random, time
from itertools import product

class minesweeper():
    def __init__(self, size, density):
        self._size = size
        self._density = density
        self._mines = round(density*(size**2))
        self._minesleft = [self._mines, None] #[Mines left, Label that displays mines left]
        temp = [0 for i in range(size)]
        self._array = [temp*1 for j in range(size)]
        self._firstclick = True
        self._solveractive = False
        self._boards = []
        #print(self._array)
        
        self._board = tkinter.Tk()
        self._board.title("Minesweeper")
        
        
        
        
        # Creates buttons for the board
        def create_buttons(board=[]):
            grid_frame = tkinter.Frame(self._board, width=400, height=400)
            grid_frame.grid(row=0, column=0, sticky="nsew")
            grid_frame.grid_propagate(False)  # Prevent resizing to fit contents

            for i in range(size):
                grid_frame.grid_rowconfigure(i, weight=1, uniform="row")
                grid_frame.grid_columnconfigure(i, weight=1, uniform="col")
                
                row = []
                for j in range(size):
                    button = tkinter.Button(
                        grid_frame,
                        bd=1,
                        font=("DejaVu Sans", 10),
                        relief="raised"  # or "raised", or dynamic based on logic
                    )
                    button.grid(row=i, column=j, sticky="nsew", padx=0, pady=0)
                    button.bind("<Button-3>", lambda event, b=button: self.flag(event, b, False))
                    row.append(button)
                board.append(row)
            return board
        
        
        self._boards = create_buttons()   
        for i in range(size):
            for j in range(size):
                self._boards[i][j].config(command=lambda temp=self._boards[i][j], pos=[i,j]:self.button_click(temp, pos))
        
        self._minesleft[1] = tkinter.Label(self._board, text=f"Mines left: {self._minesleft[0]}", font=("Arial", 14))
        button = tkinter.Button(self._board, height=2, width=10, text="Solver", font=("DejaVu Sans", 12))
        self._minesleft[1].grid(row=1, column=0, pady=10)
        button.grid(row=2, column=0, pady=10)
        button.config(command=lambda temp=button:self.solver_button(temp))
        
        self._board.mainloop()
        
        
    #Generates value of each button (-1 = Mine)
    def create_board(self, clicked_row, clicked_col):
        squares_left = self._size**2
        mines_left = self._mines
        #print(squares_left, mines_left)
        for i in range(self._size):
            for j in range(self._size):
                if mines_left <= 0:
                    break
                
                #generate mine
                elif random.randint(1, squares_left) <= mines_left:
                    #Ensures first opened square is a 0
                    max_col = min(clicked_col + 1, self._size - 1)
                    min_col = max(clicked_col - 1, 0)
                    max_row = min(clicked_row + 1, self._size - 1)
                    min_row = max(clicked_row - 1, 0)
                    if (max_col < j or j < min_col) or (max_row < i or i < min_row):
                            self._array[i][j] = -1
                            mines_left -= 1
                    
                squares_left -= 1
                
        #add numbers in
        def add_count(row, col):
            for rows in [-1, 0, 1]:
                for cols in [-1, 0, 1]:
                    adjusted_row = row + rows
                    adjusted_col = col + cols
                    if 0 <= adjusted_col < self._size and 0 <= adjusted_row < self._size:              
                        if self._array[adjusted_row][adjusted_col] != -1:
                            self._array[adjusted_row][adjusted_col] += 1
        
        for i in range(self._size):
            for j in range(self._size):
                if self._array[i][j] == -1:
                    add_count(i,j)
    
    
    
    #Executes commands when button is clicked
    def button_click(self, button, pos):
        #first click must be 0
        if self._firstclick:
            self.create_board(pos[0],pos[1])
            
        val = self._array[pos[0]][pos[1]]
            
        #check win
        def check_state(val):
            if val == -1:
                return "LOSE"
            else:
                win = "WIN"
                for i in range(self._size):
                    for j in range(self._size):
                        if self._boards[i][j]["relief"] != "sunken" and self._array[i][j] != -1:
                            win = ""
                return win
                
        #open up the 0s
        def open_space(i, j, check_list = []):
            if not (0 <= i < self._size and 0 <= j < self._size):
                return
            elif self._array[i][j] != 0:
                button = self._boards[i][j]
                button.config(relief='sunken', state = DISABLED)
                button.config(text=self._array[i][j])
                return
            elif [i,j] not in check_list:
                button = self._boards[i][j]
                button.config(relief='sunken', state = DISABLED)
                button.config(text="")
                check_list.append([i,j])
                open_space(i+1, j, check_list)
                open_space(i-1, j, check_list)
                open_space(i, j+1, check_list)
                open_space(i, j-1, check_list)
                open_space(i+1, j-1, check_list)
                open_space(i-1, j-1, check_list)
                open_space(i+1, j+1, check_list)
                open_space(i-1, j+1, check_list)
                return

        #reset board
        def restart():
            self._board.destroy()
            minesweeper(self._size, self._density)
                       
        #Show button on click, end game if win/lose    
        button.config(relief='sunken', state = DISABLED)
        state = check_state(val)
        self._firstclick = False
        if val == 0:
                open_space(pos[0], pos[1], [])
                button.config(text="")
        if state == "LOSE":
            button.config(text="M")
            messagebox.showinfo("GG", "Game over!")
            restart()
        elif state == "WIN":
            button.config(text=val)
            messagebox.showinfo("GG", "You won!")
            restart()
        elif val != 0:
            button.config(text=val)
    
    
    
    #Flag buttons
    def flag(self, event, button, solver_mode):
        if button['relief'] != "sunken":
            if button['text'] == "":
                button.config(text="🚩", fg="red")
                self._minesleft[0] -= 1
                
            elif not solver_mode:
                button.config(text="")
                self._minesleft[0] += 1
            
            self._minesleft[1].config(text=f"Mines left: {self._minesleft[0]}")
    
    
    def solver_button(self, button):
        
        #actl solver
        def solver():
            known_board = []
            #initialise known board
            for i in range(self._size):
                temp = []
                for j in range(self._size):
                    if self._boards[i][j]['relief'] == "sunken":
                        temp.append(self._array[i][j])
                    else:
                        temp.append(-2)
                known_board.append(temp)    
            
            def in_range(val1, val2):
                if 0 <= val1 < self._size and 0 <= val2 < self._size:
                    return True
                return False
            
            def solver_step():
                
                #reinit known_board if open_board() is executed
                for i in range(self._size):
                    temp = []
                    for j in range(self._size):
                        if self._boards[i][j]['relief'] == "sunken":
                            temp.append(self._array[i][j])
                        #flagged mines are kept the same in the reinit known_board
                        elif known_board[i][j] == -1:
                            temp.append(-1)
                        else:
                            temp.append(-2)
                    known_board[i] = temp
                  
                
                # print("Known Board ")
                # for lst in known_board:
                #     print(lst)
                # print("\n")
                
                #Dict {Coords of opened tile: {Tple of unopened adj tiles}}
                adj_slots = {}
                
                #Solves basic cases + update adj_slots
                for i in range(self._size):
                    for j in range(self._size):
                        if known_board[i][j] > 0:
                            poss_loc = []
                            mine_count = 0
                            empty_count = 0

                            for num in [1, 0, -1]:
                                for nums in [1, 0, -1]:
                                    newi = i + num
                                    newj = j + nums

                                    if not (num == 0 and nums == 0):
                                        if in_range(newi, newj):
                                            if known_board[newi][newj] == -1:
                                                mine_count += 1
                                            elif known_board[newi][newj] == -2:
                                                empty_count += 1
                                                poss_loc.append((newi, newj))
                            
                            #Open unopened squares if all mines for that tile is flagged
                            if mine_count != known_board[i][j] and \
                            mine_count + empty_count != known_board[i][j]:
                                adj_slots[f"({i},{j})_{known_board[i][j]-mine_count}"] = set(poss_loc)
                                
                            elif mine_count == known_board[i][j]:
                                for newi, newj in poss_loc:
                                    self.button_click(self._boards[newi][newj], [newi, newj])
                                    known_board[newi][newj] = self._array[newi][newj]
                                    self._board.after(50, solver_step)
                                    return
                                    
                            #Flag the remaining unopened tiles for that tile
                            elif mine_count + empty_count == known_board[i][j]:
                                for newi, newj in poss_loc:
                                    if known_board[newi][newj] == -2:
                                        known_board[newi][newj] = -1
                                        self.flag(None, self._boards[newi][newj], True)
                                        self._board.after(50, solver_step)
                                        return
                                

                            ##adj_slots[f"({i},{j})_{known_board[i][j]-mine_count}"] = set(poss_loc)

                
                #Solves complex cases
                update, changes, A_ptr, B_ptr = True, False, 1, 0
                while update:
                    adj_slot_key, adj_slot_val = list(adj_slots.keys()), list(adj_slots.values()) #so i can index the dict with a ptr
                    if A_ptr >= len(adj_slots):
                        A_ptr = 0
                        B_ptr += 1
                    if B_ptr >= len(adj_slots):
                        B_ptr = 0
                        if not changes:
                            update = False
                        else:
                            changes = False
                    
                    #Trying to solve 2 tiles that share a border
                    if A_ptr != B_ptr and adj_slot_val[A_ptr].intersection(adj_slot_val[B_ptr]):
                        # compiles list of all unique unknown tiles between the 2 opened tiles
                        unknown_tiles = list(adj_slot_val[A_ptr].union(adj_slot_val[B_ptr]))
                        num_vars = len(unknown_tiles)
                        
                        #create each eqn
                        A_coef = [1 if tile in adj_slot_val[A_ptr] else 0 for tile in unknown_tiles]
                        B_coef = [1 if tile in adj_slot_val[B_ptr] else 0 for tile in unknown_tiles]
                        countA, countB = int(adj_slot_key[A_ptr][-1]), int(list(adj_slots.keys())[B_ptr][-1])
                        
                        solutions = []
                        for vals in product([0, 1], repeat=num_vars):
                            if sum(c*v for c,v in zip(A_coef, vals)) == countA and \
                            sum(c*v for c,v in zip(B_coef, vals)) == countB:
                                solutions.append(vals)
                                
                        #the constant val in each solution is the correct ans
                        solution = {}
                        for i in range(num_vars):
                            val = solutions[0][i]
                            corr_sol = True
                            for sol in solutions:
                                if sol[i] != val:
                                    corr_sol = False
                                    break
                            
                            if corr_sol:
                                solution[unknown_tiles[i]] = val
                                update = False
                        
                        #put the correct solution on the board
                        for sol in solution:
                            i, j = sol
                            if solution[sol]:
                                self.flag(None, self._boards[i][j], True)
                                known_board[i][j] = -1
                                self._board.after(50, solver_step)
            
                            else:
                                self.button_click(self._boards[i][j], [i, j])
                                known_board[i][j] = self._array[i][j]
                                self._board.after(50, solver_step)
                            return
                        
                        #Adds in additional deduced info from the 2 tiles if no unknown tile is solved
                        if not solution and adj_slot_val[A_ptr] != (adj_slot_val[B_ptr]):
                            diff, count_diff = {}, 0
                            if adj_slot_val[A_ptr].issubset(adj_slot_val[B_ptr]):
                                diff = adj_slot_val[B_ptr] - adj_slot_val[A_ptr]
                                count_diff = int(adj_slot_key[B_ptr][-1]) - int(adj_slot_key[A_ptr][-1])
                            elif adj_slot_val[B_ptr].issubset(adj_slot_val[A_ptr]):
                                diff = adj_slot_val[A_ptr] - adj_slot_val[B_ptr]
                                count_diff = int(adj_slot_key[A_ptr][-1]) - int(adj_slot_key[B_ptr][-1])
                                
                            if diff and (adj_slot_key[A_ptr][:-1] + str(count_diff)) not in adj_slots:
                                #print((adj_slot_key[A_ptr][:-1] + str(count_diff)) not in adj_slots)
                                adj_slots[adj_slot_key[A_ptr][:-1] + str(count_diff)] = diff
                                changes = True
                                
                    A_ptr += 1
                
                #Mine Count Solver
                BestCombi, adj_slot_key, adj_slot_val = {frozenset():0}, [int(key[-1]) for key in list(adj_slots.keys())], list(adj_slots.values())
                
                #Add the best combination for each set into BestCombi (Max Mines possible)
                #print(adj_slot_key)
                #print(adj_slot_val)
                for i in range(len(adj_slot_val)):
                    Combi_keys = list(BestCombi.keys())
                    BestCombi[frozenset({i})] = adj_slot_key[i]
                    for j in range(len(Combi_keys)-1):
                        result = set().union(*(adj_slot_val[k] for k in Combi_keys[j]))
                        if not adj_slot_val[i].intersection(result):
                            new_key = frozenset(set(Combi_keys[j]).union({i}))
                            new_value = adj_slot_key[i] + BestCombi[Combi_keys[j]]
                            BestCombi[new_key] = new_value
                
                max_val = max(BestCombi.values())
                max_key = [k for k, v in BestCombi.items() if v == max_val]
                for i in range(len(max_key)):
                    max_key[i] = set().union(*(adj_slot_val[k] for k in max_key[i]))
                
                #Solve using the info deduced
                unopened = [(i, j) for i in range(self._size) for j in range(self._size)
                if known_board[i][j] == -2]
                openable, flaggable = [], []
                
                #Generate lst of openable/flaggable tiles
                for keys in max_key:
                    if max_val == self._minesleft[0] and len(keys) != len(unopened):
                        openable = [coord for coord in unopened if coord not in keys]               
                        #if there is coords to click
                        if openable:
                            break
                        
                    elif max_val < self._minesleft[0] and \
                    len(keys) + (self._minesleft[0]-max_val) == len(unopened):
                        flaggable = [coord for coord in unopened if coord not in keys]
                        
                #Open/flag remaining squares    
                for i, j in openable:
                    self.button_click(self._boards[i][j], [i, j])
                    known_board[i][j] = self._array[i][j]
                    self._board.after(50, solver_step)
                    return
                for i, j in flaggable:
                    self.flag(None, self._boards[i][j], True)
                    known_board[i][j] = -1
                    self._board.after(50, solver_step)
                    return
                
                                           
                
            self._board.after(50, solver_step)
                                        
                                    
        self._solveractive = not self._solveractive
        if self._solveractive:
            if self._firstclick:
                messagebox.showinfo("Error", "Click the board first!")
                
            else:
                button.config(relief="sunken")
                solver()
                
        else:
            button.config(relief="raised")
            
            
        

        
game = minesweeper(20, 0.18)