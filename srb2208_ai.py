#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: Sam Beaulieu, srb2208
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move


# Dictionary to map boards to utility values
board_utilities = {}


def compute_utility(board, color):

    dark, light = get_score(board)

    if color == 2:
        return light - dark
    else:
        return dark - light


############ MINIMAX ###############################

def minimax_min_node(board, color):

    # Get the color of the next player
    if color == 1:
        other_color = 2
    else:
        other_color = 1

    # Get the allowed moves
    all_moves = get_possible_moves(board, other_color)

    # If there are no moves left, return the utility
    if len(all_moves) == 0:
        return None, compute_utility(board, color)

    # Else if there are moves, get their utility and return the min
    else:  
        # Get the maximum utility possible to use as a starting point for min  
        min_utility = len(board)*len(board)
        min_move = None

        # For each possible move, get the max utiltiy
        for each in all_moves:

            # Get the next board from that move
            next_board = play_move(board, other_color, each[0], each[1])

            # First check the cache for the board
            if next_board in board_utilities:
                move, new_utiltiy = board_utilities[next_board]

            else:
                # If the new utility is less than the current min, update min_utiltiy
                move, new_utiltiy = minimax_max_node(next_board, color)
                board_utilities[next_board] = (move, new_utiltiy)

            if new_utiltiy < min_utility:
                min_utility = new_utiltiy
                min_move = each

        # After checking every move, return the minimum utility
        return min_move, min_utility

    # Default return - should never be called
    return None, None


def minimax_max_node(board, color):

    # Get the allowed moves
    all_moves = get_possible_moves(board, color)

    # If there are no moves left, return the utility
    if len(all_moves) == 0:
        return None, compute_utility(board, color)

    # Else if there are moves, get their utility and return the min
    else:  
        # Store the minimum utility possible to use as a starting point for min  
        max_utility = -1 * len(board)*len(board)
        max_move = None

        # For each possible move, get the min utiltiy
        for each in all_moves:

            # Get the next board from that move
            next_board = play_move(board, color, each[0], each[1])

            # First check the cache for the board
            if next_board in board_utilities:
                move, new_utiltiy = board_utilities[next_board]

            else:
                # If the new utility is greater than the current max, update max_utility
                move, new_utiltiy = minimax_min_node(next_board, color)
                board_utilities[next_board] = (move, new_utiltiy)

            if new_utiltiy > max_utility:
                max_utility = new_utiltiy
                max_move = each

        # After checking every move, return the maximum utility
        return max_move, max_utility

    # Default return - should never be called
    return None, None

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """

    # Get the best move according to the max utiltiy
    move, utiltiy = minimax_max_node(board, color)
    return move
    
############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level, limit): 

    # Get the color of the next player
    if color == 1:
        other_color = 2
    else:
        other_color = 1

    # Get the allowed moves
    all_moves = get_possible_moves(board, other_color)

    # If there are no moves left, return the utility
    if len(all_moves) == 0 or level == limit:
        return None, compute_utility(board, color)

    # Else if there are moves, get their utility and return the min
    else:  
        # Get the maximum utility possible to use as a starting point for min  
        min_utility = len(board)*len(board)
        min_move = None

        all_moves_sorted = []

        # Get the utility of all the moves
        for each in all_moves:

            # Get the next board from that move
            next_board = play_move(board, other_color, each[0], each[1])

            # Add the moves to the list
            all_moves_sorted.append((each, next_board))

        # Sort the list by utility
        all_moves_sorted.sort(key = lambda util: compute_utility(util[1], color))

        # For each possible move, get the max utiltiy
        for each in all_moves_sorted:

            # First check the cache for the board
            if each[1] in board_utilities:
                move, new_utiltiy = board_utilities[each[1]]

            else:
                # If the new utility is less than the current min, update min_utiltiy
                move, new_utiltiy = alphabeta_max_node(each[1], color, alpha, beta, level + 1, limit)
                board_utilities[each[1]] = (move, new_utiltiy)

            if new_utiltiy < min_utility:
                min_utility = new_utiltiy
                min_move = each[0]

            if min_utility <= alpha:
                return min_move, min_utility 

            if min_utility < beta:
                beta = min_utility

        # After checking every move, return the minimum utility
        return min_move, min_utility

    # Default return - should never be called
    return None, None


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):
    # Get the allowed moves
    all_moves = get_possible_moves(board, color)

    # If there are no moves left, return the utility
    if len(all_moves) == 0 or level == limit:
        return None, compute_utility(board, color)

    # Else if there are moves, get their utility and return the min
    else:  
        # Store the minimum utility possible to use as a starting point for min  
        max_utility = -1 * len(board)*len(board)
        max_move = None

        all_moves_sorted = []

        # Get the utility of all the moves
        for each in all_moves:

            # Get the next board from that move
            next_board = play_move(board, color, each[0], each[1])

            # Add the moves to the list
            all_moves_sorted.append((each, next_board))

        # Sort the list by utility (reversed so when iterated, it starts at the greatest value)
        all_moves_sorted.sort(key = lambda util: compute_utility(util[1], color), reverse=True)

        # For each possible move, get the min utiltiy
        for each in all_moves_sorted:

            # First check the cache for the board
            if each[1] in board_utilities:
                move, new_utiltiy = board_utilities[each[1]]

            else:
                # If the new utility is greater than the current max, update max_utility
                move, new_utiltiy = alphabeta_min_node(each[1], color, alpha, beta, level + 1, limit)
                board_utilities[each[1]] = (move, new_utiltiy)

            if new_utiltiy > max_utility:
                max_utility = new_utiltiy
                max_move = each[0]

            if max_utility >= beta:
                return max_move, max_utility

            if max_utility > alpha:
                alpha = max_utility

        # After checking every move, return the maximum utility
        return max_move, max_utility

    # Default return - should never be called
    return None, None


def select_move_alphabeta(board, color): 

    # Get the maximum and minimum utility values
    alpha = -1 * len(board) * len(board)
    beta = -1 * alpha

    # Depth limit that seems to be the maximum for an 8x8 board is 6. Anywhere over and 
    #	when playing the random ai or itself, there are a lot of timeouts.

    # Get the best move according to the max utiltiy
    move, utiltiy = alphabeta_max_node(board, color, alpha, beta, 0, 6)
    return move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Srb2208's AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
