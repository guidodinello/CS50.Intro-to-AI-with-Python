from pickle import TRUE
import sys
from wsgiref.validate import IteratorWrapper

from crossword import *

#mine-included=====
import timeit

class time():
    def start():
        return timeit.default_timer()
    
    def end(func, starting):
        end = timeit.default_timer()
        print(f'{func} time: {end-starting}')
    #start = time.start()
    #function()
    #time.end('function', start)
#==================

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        start4 = timeit.default_timer()
        self.enforce_node_consistency()
        end4 = timeit.default_timer()
        print(f'node consistency time: {end4-start4}')
        start5 = timeit.default_timer()
        self.ac3()
        end5 = timeit.default_timer()
        print(f'ac3 time: {end5-start5}')
        start6 = timeit.default_timer()
        sol = self.backtrack(dict())
        end6 = timeit.default_timer()
        print(f'backtrack time: {end6-start6}')
        return sol

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        #for each variable
        for variable in self.domains.keys():
            removeWord = []
            #for each possible value on the variables domain
            for value in self.domains[variable]:
                #if the letters of the word is not the same as the letters required
                if len(value) != variable.length:
                    #we discard that word
                    removeWord.append(value)
            for word in removeWord:
                self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        #if no overlap, no conflict, no revision
        if self.crossword.overlaps[x,y] is None: return False
        else: 
            o1, o2 = self.crossword.overlaps[x,y]
            removeWords = []

        revision = False
        #for each word on x's domain
        for x_word in self.domains[x]:
            coincidence = False
            #for each word on y's domain
            for y_word in self.domains[y]: 
                #if coincidence then no conflict otherwise keep looking
                coincidence = x_word != y_word and x_word[o1] == y_word[o2]
                if coincidence:
                    break
            #if we didnt find a coincidence over all y's domain then theres a conflict
            if not coincidence:
                removeWords.append(x_word)
                revision = True
        #remove
        for word in removeWords:
            self.domains[x].remove(word)

        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            queue = []
            for var in self.domains.keys():
                for neighbor in self.crossword.neighbors(var):
                    queue.append((var,neighbor))
                #I have to do this for n-1 element the nth will give redundant info
        else: 
            queue = arcs

        while queue != []:
            (x,y) = queue.pop()
            start7 = timeit.default_timer()
            revise = self.revise(x,y)
            end7 = timeit.default_timer()
            print(f'revise time: {end7-start7}')
            if revise:
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x)-{y}:
                    queue.insert(0,(neighbor,x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return self.crossword.variables == set(assignment.keys())


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #================METHOD 1==================#
        values = set()  #in operator for set is O(1) average and O(n) for lists
        for key, val in assignment.items():
            #making sure of no duplicates
            if (val in values):
                return False
            else:
                values.add(val)
            #making sure its the correct length
            if (key.length != len(val)):
                return False
            #making sure of no conflicts with neighbors
            neighbourCells = self.crossword.neighbors(key)
            for neighbor in neighbourCells:
                o1, o2 = self.crossword.overlaps[key, neighbor]
                if neighbor in assignment:
                    if val[o1] != assignment[neighbor][o2]:
                        return False
        return True

         #================METHOD 2==================#
        # for variable1 in assignment:
        #     word1 = assignment[variable1]
        #     if variable1.length != len(word1):
        #         # word length doesn't satisfy constraints
        #         return False

        #     for variable2 in assignment:
        #         word2 = assignment[variable2]
        #         if variable1 != variable2:
        #             if word1 == word2:
        #                 # two variables mapped to the same word
        #                 return False

        #             overlap = self.crossword.overlaps[variable1, variable2]
        #             if overlap is not None:
        #                 a, b = overlap
        #                 if word1[a] != word2[b]:
        #                     # words don't satisfy overlap constraints
        #                     return False

        # return True
        
         #================CONCLUSION==================#
         #method 1 and 2 seem to take the same amount of time

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        ordering = dict()
        var_domain = self.domains[var]
        neighbors = self.crossword.neighbors(var)

        #for each value in the domain
        for value in var_domain:
            count = 0
            for neighbor in neighbors:
                #if the value belongs to the var domain and the neighbor domain will be ruled out
                if value in self.domains[neighbor]:
                    count += 1
            ordering[value] = count
        
        #sorting in increasing order
        return sorted(ordering, key=lambda key: ordering[key])


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        degree = 0
        value = float('inf')
        for i in self.domains.keys():
            #variable must not be part of assignment
            if i in assignment:
                continue
            else:
                #if we found a variable with less remaining values than our current best
                if value > len(self.domains[i]):
                    #update properties value,name,degree
                    value = len(self.domains[i])
                    variable = i
                    #get degree
                    if self.crossword.neighbors(i) is None:
                        degree = 0
                    else:
                        degree = len(self.crossword.neighbors(i))
                #if variable has the same rv that our current best, break the tie with degree
                elif value == len(self.domains[i]):
                    #if degree were 0 we could keep what we currently have, otherwise analyze
                    if self.crossword.neighbors(i) is not None:
                        #we found a higher degree
                        if degree < len(self.crossword.neighbors(i)):
                            #update
                            variable = i
                            degree = len(self.crossword.neighbors(i)) 
        return variable    

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        #Base Case
        if self.assignment_complete(assignment):
            return assignment
        #Recursive Case
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            #try value
            assignment[var] = value
            #if its valid
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            #remove value if we ended up in a dead end street
            assignment.pop(var)
        #if no valid values found for var
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    start2 = timeit.default_timer()
    crossword = Crossword(structure, words)
    end2 = timeit.default_timer()
    print(f'crossword time: {end2-start2}')
    start3 = timeit.default_timer()
    creator = CrosswordCreator(crossword)
    end3 = timeit.default_timer()
    print(f'crossword creator time: {end3-start3}')
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    #========
    start1 = timeit.default_timer()
    main()
    end1 = timeit.default_timer()
    print(f'main time: {end1-start1}')
    #========

    #======CONCLUSION=====#
    # Around 81% of the time is spent on the revise calls inside the ac3 algorithm, but this is mainly because we have to make a 
    # nested iteration over self.domain of two variables, and this is quite demanding for big word_dictionaries and variables with
    # a 'common' length (5-4 combination takes around 22% of time) due to weak unary constrainment
    #=====================#

