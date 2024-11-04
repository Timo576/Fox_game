"""Small program to test strategies against all the possible tile orders of the fox game
Credit Alex Cheddar for exposure of the problem.
I also checked if 5f's, 6o's and 5x's is the worst possible starting configuration.
It is, this was done by looping over all the possible starting tiles and checking.
This code was reverted cos its really slow and makes it confusing to just change strategy."""

import itertools
import numpy as np

FOX_DICT = {0: 'F', 1: 'O', 2: 'X'}
# fail = 0


def simplest(tile_order, current_board, *excess):
    """Places the tiles in the order they were given.
    I use this as an alternative to dice roll so all strategies are deterministic.
    Win rate: 12.6% (0.1265123765123765)
    2.38% with diagonal rule (0.023809523809523808)"""
    output_board = current_board.copy()
    for tile in tile_order:
        for index in range(0, 16):
            if output_board[index] == 'Blank':
                output_board[index] = tile
                break
    return output_board


def cheater(*excess):
    """Wins the game. Mainly for debugging."""
    return np.array(['O',] * 6 + ['F',] * 5 + ['X',] * 5)


def basic_loss_avoid(tile_order, current_board, starting_f, starting_o, starting_x):
    """My first guess at a better strategy, takes more computation than you'd
    normally want but should be proof of concept.
    N.B. Incorporates diagonal rule.
    Important that you can only see previous tiles when testing an actual strategy.
    Input:
        tile_order: tuple of strings (F, O, X) in order of tiles to place
        current_board: np.array of 16 strings (Blank, F, O and X)
        starting_f: int number of F tiles
        starting_o: int number of O tiles
        starting_x: int number of X tiles
    Returns:
        output_board: np.array of 16 strings (Blank, F, O and X)
        after trying the strategy"""
    output_board = current_board.copy()
    initial_f_count = starting_f + current_board.tolist().count('F')
    initial_o_count = starting_o + current_board.tolist().count('O')
    initial_x_count = starting_x + current_board.tolist().count('X')
    for tile in tile_order:
        index = tester_granular(
            initial_f_count, initial_o_count, initial_x_count, output_board)
        output_board[index] = tile
    return output_board


def tester_granular(initial_f_count, initial_o_count, initial_x_count,
                    output_board):
    # only usuable info is new_board (NOT tile)
    current_f_count = initial_f_count - output_board.tolist().count('F')
    current_o_count = initial_o_count - output_board.tolist().count('O')
    current_x_count = initial_x_count - output_board.tolist().count('X')
    # Assume the tile will be the most likely
    most_likely = FOX_DICT[
        np.argmax([current_f_count, current_o_count, current_x_count])]
    # place the tile in the first place that doesn't lose
    for index in range(0, 16):
        if output_board[index] == 'Blank':
            test_board = output_board.copy()
            test_board[index] = most_likely
            if not has_fox(test_board):
                # Must end like this
                return index
    # If search fails
    # print(f"Failed to place {tile}")
    # global fail
    # fail += 1
    for index in reversed(range(0, 16)):
        if output_board[index] == 'Blank':
            return index


def has_fox(output_board):
    """Checks if a given board contains a FOX
    Input:
        output_board: np.array of 16 strings (Blank, F, O and X)
    Returns:
        Boolean: True if FOX is found, False otherwise
    """
    # Can probably also be optmizied significantly for performance and style
    # but this is hopefully readable
    new_board = output_board.copy()
    readable_board = new_board.reshape(4, 4)
    # print(f"Board:\n{readable_board}")
    for row_index in range(0, 4):
        for cell_index in range(0, 4):
            # Skip blank
            if readable_board[row_index][cell_index] == 'Blank':
                continue
            # Check for fox forwards and backwards in 4 directions:
            # down-left, down, down-right, right.
            # I believe this covers all cases
            # Down-left
            if row_index < 2 and cell_index > 1:
                o_down_left = readable_board[row_index + 1][
                                   cell_index - 1] == 'O'
                if o_down_left:
                    if readable_board[row_index][cell_index] == 'F' and \
                            readable_board[row_index + 2][
                                cell_index - 2] == 'X':
                        # print(f"Board:\n{readable_board}")
                        return True
                    if readable_board[row_index][cell_index] == 'X' and \
                            readable_board[row_index + 2][
                                cell_index - 2] == 'F':
                        # print(f"Board:\n{readable_board}")
                        return True
            # Down
            if row_index < 2:
                o_down = readable_board[row_index + 1][cell_index] == 'O'
                if o_down:
                    if readable_board[row_index][cell_index] == 'F' and \
                            readable_board[row_index + 2][cell_index] == 'X':
                        # print(f"Board:\n{readable_board}")
                        return True
                    if readable_board[row_index][cell_index] == 'X' and \
                            readable_board[row_index + 2][cell_index] == 'F':
                        # print(f"Board:\n{readable_board}")
                        return True
            # Down-right
            if row_index < 2 and cell_index < 2:
                o_down_right = readable_board[row_index + 1][
                                  cell_index + 1] == 'O'
                if o_down_right:
                    if readable_board[row_index][cell_index] == 'F' and \
                            readable_board[row_index + 2][
                                cell_index + 2] == 'X':
                        # print(f"Board:\n{readable_board}")
                        return True
                    if readable_board[row_index][cell_index] == 'X' and \
                            readable_board[row_index + 2][
                                cell_index + 2] == 'F':
                        # print(f"Board:\n{readable_board}")
                        return True
            # Right
            if cell_index < 2:
                o_right = readable_board[row_index][cell_index + 1] == 'O'
                if o_right:
                    if readable_board[row_index][cell_index] == 'F' and \
                            readable_board[row_index][cell_index + 2] == 'X':
                        # print(f"Board:\n{readable_board}")
                        return True
                    if readable_board[row_index][cell_index] == 'X' and \
                            readable_board[row_index][cell_index + 2] == 'F':
                        # print(f"Board:\n{readable_board}")
                        return True
    return False


def main():
    """Checks all possible tile combinations to find the chance FOX is found with a
    couple of different strategies"""
    # order_count = 0
    win_count = 0
    rule_order_count = 0
    strategy = simplest
    board_size = 16
    initial_board = np.array(['Blank'] * board_size)
    # Diagonal rule
    initial_board[0] = 'O'
    initial_board[5] = 'O'
    initial_board[10] = 'O'
    initial_board[15] = 'O'
    starting_f = 5
    starting_o = 6
    starting_x = 5
    tiles_to_choose_from = starting_f + starting_o + starting_x
    for tile_order in itertools.product(
            'FOX', repeat=tiles_to_choose_from):
        # If there are too many of one tile, do nothing
        # This was preferable to using permutations because it that
        # creates more duplicates with overhead.
        # There are definitely more efficient ways to generate
        # the tile orders though
        if tile_order.count('F') > starting_f:
            continue
        if tile_order.count('O') > starting_o:
            continue
        if tile_order.count('X') > starting_x:
            continue
        # order_count += 1
        rule_order_count += 1
        output_board = strategy(
            tile_order, initial_board, starting_f, starting_o, starting_x)
        if not has_fox(output_board):
            win_count += 1
            # readable_board = np.array([output_board]).reshape(4, 4)
            # print(f"Board:\n{readable_board}")
    # # print(f"Order count: {order_count}")
    print(f"Win count: {win_count}")
    # print(f"Fail count: {fail}")
    # print(f"Win rate (if no rule): {win_count / order_count}")
    print(f"Rule order count: {rule_order_count}")
    print(f"Win rate (if rule): {win_count / rule_order_count}")


if __name__ == '__main__':
    main()
