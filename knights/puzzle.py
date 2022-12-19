#from ast import Constant
#from itertools import Predicate
#from itertools import Predicate
from unittest.case import _AssertRaisesContext
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

#In each of the above puzzles, each character is either a knight or a knave. 
#Every sentence spoken by a knight is true, and every sentence spoken by a knave is false.

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    And(Or(AKnight,AKnave),Not(And(AKnight,AKnave))),

    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    And(Or(AKnight,AKnave),Not(And(AKnight,AKnave))),
    And(Or(BKnight,BKnave),Not(And(BKnight,BKnave))),

    Implication(AKnight, And(AKnave,BKnave)),
    Implication(AKnave, Not(And(AKnave,BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    And(Or(AKnight,AKnave),Not(And(AKnight,AKnave))),
    And(Or(BKnight,BKnave),Not(And(BKnight,BKnave))),

    Implication(AKnight, And(Biconditional(AKnave,BKnave),Biconditional(AKnight,BKnight))),
    Implication(AKnave, Not(And(Biconditional(AKnave,BKnave),Biconditional(AKnight,BKnight)))),

    Implication(BKnight, And(Biconditional(AKnave,BKnight),Biconditional(AKnight,BKnave))),
    Implication(BKnave, Not(And(Biconditional(AKnave,BKnight),Biconditional(AKnight,BKnave)))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
ASaidKnave = Symbol('A said is a Knave')
ASaidKnight = Not(ASaidKnave)
knowledge3 = And(
    #Each character is either a Knight or a Knave
    And(Or(AKnight,AKnave),Not(And(AKnight,AKnave))),
    And(Or(BKnight,BKnave),Not(And(BKnight,BKnave))),
    And(Or(CKnight,CKnave),Not(And(CKnight,CKnave))),

    #As I dont know what A said 
    Implication(And(ASaidKnight,AKnight), AKnight),
    Implication(And(ASaidKnight,AKnave), AKnave),
    Implication(And(ASaidKnave,AKnight), AKnave), #clearly a contradiction
    Implication(And(ASaidKnave,AKnave), AKnight), #another clear contradiction

    # B says "A said 'I am a knave'."
    Implication(BKnight, ASaidKnave),
    Implication(BKnave, Not(ASaidKnave)),

    # B says "C is a knave."
    Implication(BKnight,CKnave),
    Implication(BKnave,Not(CKnave)),

    # C says "A is a knight."
    Implication(CKnight,AKnight),
    Implication(CKnave,Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        #print(knowledge)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print("    {}".format(symbol))


if __name__ == "__main__":
    main()
