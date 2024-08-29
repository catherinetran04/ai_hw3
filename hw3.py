from random import random
import sys
sys.path.append('aima-python')
from search import *
from games import *
import math

def c4_eval(state):
    '''Example of a bad evaluation function: It gives a high
    score to any state whose board has a lot of Xs in the same
    column. Doesn't account for 'O', doesn't check other things
    that really would make sense.
    '''
    def count_in_line(start, dxy):
        count = 0
        while start in state.board:
            if state.board.get(start) == 'X':
                count += 1
            start = (start[0] + dxy[0], start[1] + dxy[1]) 
        return count

    ev = 0
    for i in range(1,8):
        ev += count_in_line((1,i), (0,1)) * 2
    # scale from -1 to 1
    return ev / 48

def ab_cutoff_player(game, state):
    return alpha_beta_cutoff_search(state, game, eval_fn=c4_eval)


def c4_eval_better(state):
    def count_4_in_row(start, dxy):
        (dx, dy) = dxy
        x, y = start
        count_4 = 0
        in_row = 0
        while state.board.get((x,y)) == 'X':
            in_row += 1
            count_4 += 1
            x, y = x + dx, y + dy
        x,y = start
        
        if in_row >= 4:
            count_4 = 3000
            return count_4

        while state.board.get((x,y)) == 'O':
            count_4 -= 1
            x, y = x + dx, y + dy 
        return count_4

    ev = 0
    for i in state.board:
        # search up (0,1)
        ev += count_4_in_row(i, (0,1))
        # search right (1,0)
        ev += count_4_in_row(i, (1,0))     
        # search diag (1,1)   
        ev += count_4_in_row(i, (1,1))
    # scale
    return ev/3000

def ab_cutoff_player_better(game, state):
    return alpha_beta_cutoff_search(state, game, eval_fn = c4_eval_better)


def gomoku_eval(state):
    # counts and gives higher eval score for 5 in a row
    def count_5_in_row(start, dxy):
        (dx, dy) = dxy
        x, y = start
        count_5 = 0
        in_row = 0
        while state.board.get((x,y)) == 'X':
            in_row += 1
            count_5 += 1
            x, y = x + dx, y + dy
        x,y = start
        
        if in_row >= 5:
            count_5 = 3000
            return count_5

        while state.board.get((x,y)) == 'O':
            count_5 -= 1
            x, y = x + dx, y + dy 
        return count_5

    ev = 0
    for i in state.board:
        # search up (0,1)
        ev += count_5_in_row(i, (0,1))
        # search right (1,0)
        ev += count_5_in_row(i, (1,0))     
        # search diag (1,1)   
        ev += count_5_in_row(i, (1,1))

    # scale
    return ev/3000

def ab_cutoff_player_gomoku(game, state):
    return alpha_beta_cutoff_search(state, game, d= 1, eval_fn= gomoku_eval)

class HW3:
    def __init__(self):
        pass

    def example_problem(self):
        tt = TicTacToe()
        tt.play_game(alpha_beta_player,query_player)

    def example_problem2(self):
        c4 = ConnectFour()
        c4.play_game(ab_cutoff_player,query_player)

    def problem_1d(self):
        c4 = ConnectFour()
        # ab agent set as X
        c4.play_game(ab_cutoff_player_better, random_player)

    def problem_2b(self):
        g = Gomoku()
        # ab agent set as X
        g.play_game(ab_cutoff_player_gomoku, random_player)
    
def main():
    hw3 = HW3()
    # An example for you to follow to get you started on Games
    print('Example Problem result:')
    print('=======================')
    #print(hw3.example_problem())
    #print(hw3.example_problem2())
    print(hw3.problem_1d())
    print(hw3.problem_2b())
    
if __name__ == '__main__':
    main()
