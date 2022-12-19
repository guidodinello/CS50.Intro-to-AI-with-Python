import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # More generally, any time the number of cells is equal to the count, we know that all of that sentence’s cells 
        #must be mines.
        if len(self.cells) == self.count:
            return self.cells
        else: return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # More generally, any time we have a sentence whose count is 0, we know that all of that sentence’s cells must 
        #be safe.
        if self.count == 0:
            return self.cells
        else: return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If cell is in the sentence, the function should update the sentence so that cell 
        #is no longer in the sentence, but still represents a logically correct sentence given 
        #that cell is known to be a mine.
        #If cell is not in the sentence, then no action is necessary.

        new_cells = set()
        for elem in self.cells:
            if elem == cell: self.count -=1
            else: new_cells.add(elem)
        self.cells = new_cells

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If cell is in the sentence, the function should update the sentence so that cell 
        #is no longer in the sentence, but still represents a logically correct sentence given 
        #that cell is known to be safe.
        #If cell is not in the sentence, then no action is necessary.
        
        new_cells = set()
        for elem in self.cells:
            if elem != cell: 
                new_cells.add(elem)
                
        self.cells = new_cells
        


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):

        def remove_dups():  #removing duplicates
            unique_knowledge = []
            for s in self.knowledge:
                if s not in unique_knowledge:   #only add if we hadnt added yet
                    unique_knowledge.append(s)
                #else: print(f"removing... {s.cells}={s.count}")
            self.knowledge = unique_knowledge

        def remove_sures(): 
            #if we have something like {A,B}=2 we already know both are mines, so theres no point in leaving them in
            #knowledge
            final_knowledge = []
            for s in self.knowledge:
                final_knowledge.append(s)
                if s.known_mines():
                    print(f"known mines : {s.cells}={s.count}")
                    for mineFound in s.known_mines():
                        self.mark_mine(mineFound)
                    final_knowledge.pop(-1)
                elif s.known_safes():
                    print(f"known safes : {s.cells}={s.count}")
                    for safeFound in s.known_safes():
                        self.mark_safe(safeFound)
                    final_knowledge.pop(-1)
            self.knowledge = final_knowledge

        def find_neighbours(cell, count):
            i,j = cell
            neighbours = []

            def in_margins(x,y):
                return x >= 0 and x < self.height and col >= 0 and col < self.width

            for row in range(i-1, i+2):
                for col in range(j-1, j+2):
                    is_safe = (row, col) in self.safes
                    is_mine = (row,col) in self.mines
                    not_itself = (row, col) != cell 
                    if in_margins(row,col) and not_itself and not is_safe and not is_mine:
                        neighbours.append((row, col))
                    if is_mine:
                        count -= 1

            return neighbours, count

        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1
        self.moves_made.add(cell)
        #2
        self.mark_safe(cell)
        #3
        cells, filtered_count = find_neighbours(cell, count)
        sentence = Sentence(cells, filtered_count)
        self.knowledge.append(sentence)
        #4 and 5
        new_inferences = []
        for s in self.knowledge:
            if s == sentence:   #we already add it
                continue
            elif s.cells.issuperset(sentence.cells):    #sentence is a subset of s
    
        #More generally, any time we have two sentences set1 = count1 and set2 = count2 where set1 is a subset of set2, 
        #then we can construct the new sentence set2 - set1 = count2 - count1. Consider the example above to ensure you 
        #understand why that’s true.

                setDiff = s.cells-sentence.cells
                #set2 - set1 = 0, thus each elem in setdiff is safe 
                #{A,B}=1
                #{A,B,C}=1
                #Then... {A,B,C}-{A,B}=1-1 thus {C}=0
                if s.count == sentence.count:   
                    for safeFound in setDiff:
                        self.mark_safe(safeFound)
                #len(set2 - set1) = count2 - count1, thus each elem in setdiff is a mine
                #{A,B,C}=2
                #{A,B,C,D,E,F}=5
                #Then... {A,B,C,D,E,F}-{A,B,C}=5-2 thus {D,E,F}=3
                elif len(setDiff) == s.count - sentence.count:
                    for mineFound in setDiff:
                        self.mark_mine(mineFound)
                #inference
                #{A,B,C}=1
                #{A,B,C,D,E,F}=2
                #Then... {A,B,C,D,E,F}-{A,B,C}=2-1 thus {D,E,F}=1
                else:
                    new_inferences.append(
                        Sentence(setDiff, s.count - sentence.count)
                    )
            elif sentence.cells.issuperset(s.cells):    #s is a subset of sentence
                setDiff = sentence.cells-s.cells
                # Known safes
                if s.count == sentence.count:
                    for safeFound in setDiff:
                        self.mark_safe(safeFound)
                # Known mines
                elif len(setDiff) == sentence.count - s.count:
                    for mineFound in setDiff:
                        self.mark_mine(mineFound)
                # Known inference
                else:
                    new_inferences.append(
                        Sentence(setDiff, sentence.count - s.count)
                    )

        self.knowledge.extend(new_inferences)
        remove_dups()
        remove_sures()

        def print_actions():
            know = 1
            for items in self.knowledge:
                print(f"{know}:{items.cells} = {items.count}")
                know += 1
            print(f"mines = {self.mines}")
            print(f"safe = {self.safes}")
        #print_actions()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safeCells = self.safes - self.moves_made
        if not safeCells:
            return None
        # print(f"Pool: {safeCells}")
        move = safeCells.pop()
        return move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_moves = []
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.mines and (i,j) not in self.moves_made:
                    all_moves.append((i,j))
        # No moves left
        if len(all_moves) == 0:
            return None
        # Return available
        move = random.choice(all_moves)
        return move
