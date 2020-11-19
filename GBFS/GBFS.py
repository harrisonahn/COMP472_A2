import csv
import os
import time
import timeit
import numpy
import math
import decimal
import pandas as pd
from queue import PriorityQueue
from heapq import *

# path to input file of puzzles
filename = 'samplePuzzles.txt'
""" Change the heuristics_option variable to 0 for h0, 1 for hamming distance, 2 for permutation inversions"""
heuristics_option = 2


def output_pathmoves_to_file(filename, finalpath, finaltime):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        if (finalpath == "no solution"):
            writer.writerow([finalpath])

        else:
            i = 0
            initialn = finalpath[i][1]
            initial_string = "0 0 " + str(initialn)
            writer.writerow([initial_string])
            while i + 1 < len(finalpath):
                currentn = finalpath[i]
                currentnlist = list(currentn[1].split(" "))
                current_index_of_empty = currentnlist.index('0')
                nextn = finalpath[i + 1]
                nextnlist = list(nextn[1].split(" "))
                next_index_of_empty = nextnlist.index('0')

                """determine cost of move"""
                if (current_index_of_empty != 3 and current_index_of_empty != 7) and next_index_of_empty - current_index_of_empty == 1:
                    # this moves the tile right with a cost of 1
                    t_string = str(currentnlist[next_index_of_empty]) + " 1 " + str(nextn[1])

                elif (current_index_of_empty != 0 and current_index_of_empty != 4) and next_index_of_empty - current_index_of_empty == -1:
                    # this tile moved left with a cost of 1
                    t_string = str(currentnlist[next_index_of_empty]) + " 1 " + str(nextn[1])

                elif (current_index_of_empty != 0 and current_index_of_empty != 1 and current_index_of_empty != 2 and current_index_of_empty != 3) and next_index_of_empty - current_index_of_empty == -4:
                    # this tile moved up with a cost of 1
                    t_string = str(currentnlist[next_index_of_empty]) + " 1 " + str(nextn[1])

                elif (current_index_of_empty != 4 and current_index_of_empty != 5 and current_index_of_empty != 6 and current_index_of_empty != 7) and next_index_of_empty - current_index_of_empty == 4:
                    # this tile moved down with a cost of 1
                    t_string = str(currentnlist[next_index_of_empty]) + " 1 " + str(nextn[1])

                elif (current_index_of_empty == 0 or current_index_of_empty == 4) and next_index_of_empty - current_index_of_empty == 3:
                    # this tile did a wrap move with a cost of 2
                    t_string = str(currentnlist[next_index_of_empty]) + " 2 " + str(nextn[1])

                elif (current_index_of_empty == 3 or current_index_of_empty == 7) and next_index_of_empty - current_index_of_empty == -3:
                    # this tile did a wrap move with a cost of 2
                    t_string = str(currentnlist[next_index_of_empty]) + " 2 " + str(nextn[1])

                else:  # tile did a diagonal move with a cost of 3
                    t_string = str(currentnlist[next_index_of_empty]) + " 3 " + str(nextn[1])

                writer.writerow([t_string])
                i += 1
            writer.writerow([finaltime])


def output_searchpath_to_file(filename, searchpath):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        if (searchpath == "no solution"):
            writer.writerow([searchpath])
        else:
            for node in searchpath:
                f_score = 0
                h_score = node[0]
                g_score = node[2]
                t_string = str(f_score) + " " + str(g_score) + " " + str(h_score) + " " + str(node[1])
                writer.writerow([t_string])


# reading contents of a file
def getPuzzleFromCSV(filename):
    with open(filename, 'r') as file:
        content = file.read()
        puzzle = content.splitlines()
        file.close()
    return puzzle


def GoalPuzzle(solution):
    solution1 = '1 2 3 4 5 6 7 0'
    solution2 = '1 3 5 7 2 4 6 0'
    if solution == solution1 or solution == solution2:
        return True
    else:
        return False


def checkIfStateExists(node, list):
    if node in list:
        return True
    else:
        return False


def isInQueue(x, q):
    for element in q:
        if x in element:
            return True
    return False


def renewQueue(node, list1):
    queue1 = PriorityQueue()
    for item in list1:
        if (item[1] == node[1] and item[0] > node[0]):
            list1.remove(item)
            list1.append(node)
            for item in range(len(list1)):
                queue1.put(item)
    return queue1, list1


# empty tile moving to the left
def move_left(node):
    li = list(node[1].split(" "))
    index_of_empty = li.index('0')
    newboard = li
    newNode = (node[0], node[1], node[2])   # hscore, newboard, gscore

    if (index_of_empty != 3 and index_of_empty != 7):
        possible = True
        newboard[index_of_empty], newboard[index_of_empty + 1] = newboard[index_of_empty + 1], newboard[index_of_empty]
        space = ' '
        newboard = space.join(newboard)

        h_score = get_h_score(heuristics_option, newboard)
        newNode = (node[0] + h_score, newboard, node[2] + 1)
    else:
        possible = False

    return possible, newNode


# empty tile moving to the right
def move_right(node):
    newboard = list(node[1].split(" "))
    index_of_empty = newboard.index('0')
    newNode = (node[0], node[1], node[2])
    if index_of_empty != 0 and index_of_empty != 4:
        possible = True
        newboard[index_of_empty], newboard[index_of_empty - 1] = newboard[index_of_empty - 1], newboard[index_of_empty]
        space = ' '
        newboard = space.join(newboard)
        h_score = get_h_score(heuristics_option, newboard)
        newNode = (node[0] + h_score, newboard, node[2] + 1)
    else:
        possible = False

    return possible, newNode


# empty tile moving up
def move_up(node):
    newboard = list(node[1].split(" "))
    index_of_empty = newboard.index('0')
    newNode = (node[0], node[1], node[2])
    if (index_of_empty != 4 and index_of_empty != 5 and index_of_empty != 6 and index_of_empty != 7):
        possible = True
        newboard[index_of_empty], newboard[index_of_empty + 4] = newboard[index_of_empty + 4], newboard[index_of_empty]
        space = ' '
        newboard = space.join(newboard)
        h_score = get_h_score(heuristics_option, newboard)
        newNode = (node[0] + h_score, newboard, node[2] + 1)
    else:
        possible = False

    return possible, newNode


# empty tile moving down
def move_down(node):
    newboard = list(node[1].split(" "))
    index_of_empty = newboard.index('0')
    newNode = (node[0], node[1], node[2])
    if (index_of_empty != 0 and index_of_empty != 1 and index_of_empty != 2 and index_of_empty != 3):
        possible = True
        newboard[index_of_empty], newboard[index_of_empty - 4] = newboard[index_of_empty - 4], newboard[index_of_empty]
        space = ' '
        newboard = space.join(newboard)
        h_score = get_h_score(heuristics_option, newboard)
        newNode = (node[0] + h_score, newboard, node[2] + 1)
    else:
        possible = False

    return possible, newNode


def move_wrap(node):
    newboard = list(node[1].split(" "))
    index_of_empty = newboard.index('0')
    newNode = (node[0], node[1], node[2])

    if (index_of_empty == 0 or index_of_empty == 4):
        possible = True
        newboard[index_of_empty], newboard[index_of_empty + 3] = newboard[index_of_empty + 3], newboard[index_of_empty]
        space = ' '
        newboard = space.join(newboard)
        h_score = get_h_score(heuristics_option, newboard)
        newNode = (node[0] + h_score, newboard, node[2] + 1)

    elif (index_of_empty == 3 or index_of_empty == 7):
        possible = True
        newboard[index_of_empty], newboard[index_of_empty - 3] = newboard[index_of_empty - 3], newboard[index_of_empty]
        space = ' '
        newboard = space.join(newboard)
        h_score = get_h_score(heuristics_option, newboard)
        newNode = (node[0] + h_score, newboard, node[2] + 1)
    else:
        possible = False

    return possible, newNode


# empty tile moving diagonally
def move_diagonal(node):
    li = list(node[1].split(" "))
    li2 = list(li)
    index_of_empty = li.index('0')
    newboard1 = li
    newboard2 = li2
    newNode1 = (node[0], node[1], node[2])
    newNode2 = (node[0], node[1], node[2])

    if (index_of_empty == 0):
        possible = True
        newboard1[index_of_empty], newboard1[index_of_empty + 5] = newboard1[index_of_empty + 5], newboard1[
            index_of_empty]
        space = ' '
        newboard1 = space.join(newboard1)
        h_score = get_h_score(heuristics_option, newboard1)
        newNode1 = (node[0] + h_score, newboard1, node[2] + 1)

        newboard2[index_of_empty], newboard2[index_of_empty + 7] = newboard2[index_of_empty + 7], newboard2[
            index_of_empty]
        space = ' '
        newboard2 = space.join(newboard2)
        h_score = get_h_score(heuristics_option, newboard2)
        newNode2 = (node[0] + h_score, newboard2, node[2] + 1)

    elif (index_of_empty == 3):
        possible = True
        newboard1[index_of_empty], newboard1[index_of_empty + 3] = newboard1[index_of_empty + 3], newboard1[
            index_of_empty]
        space = ' '
        newboard1 = space.join(newboard1)
        h_score = get_h_score(heuristics_option, newboard1)
        newNode1 = (node[0] + h_score, newboard1, node[2] + 1)

        newboard2[index_of_empty], newboard2[index_of_empty + 1] = newboard2[index_of_empty + 1], newboard2[
            index_of_empty]
        space = ' '
        newboard2 = space.join(newboard2)
        h_score = get_h_score(heuristics_option, newboard2)
        newNode2 = (node[0] + h_score, newboard2, node[2] + 1)

    elif (index_of_empty == 4):
        possible = True
        newboard1[index_of_empty], newboard1[index_of_empty - 3] = newboard1[index_of_empty - 3], newboard1[
            index_of_empty]
        space = ' '
        newboard1 = space.join(newboard1)
        h_score = get_h_score(heuristics_option, newboard1)
        newNode1 = (node[0] + h_score, newboard1, node[2] + 1)

        newboard2[index_of_empty], newboard2[index_of_empty - 1] = newboard2[index_of_empty - 1], newboard2[
            index_of_empty]
        space = ' '
        newboard2 = space.join(newboard2)
        h_score = get_h_score(heuristics_option, newboard2)
        newNode2 = (node[0] + h_score, newboard2, node[2] + 1)

    elif (index_of_empty == 7):
        possible = True
        newboard1[index_of_empty], newboard1[index_of_empty - 5] = newboard1[index_of_empty - 5], newboard1[
            index_of_empty]
        space = ' '
        newboard1 = space.join(newboard1)
        h_score = get_h_score(heuristics_option, newboard1)
        newNode1 = (node[0] + h_score, newboard1, node[2] + 1)

        newboard2[index_of_empty], newboard2[index_of_empty - 7] = newboard2[index_of_empty - 7], newboard2[
            index_of_empty]
        space = ' '
        newboard2 = space.join(newboard2)
        h_score = get_h_score(heuristics_option, newboard2)
        newNode2 = (node[0] + h_score, newboard2, node[2] + 1)
    else:
        possible = False

    return possible, newNode1, newNode2


def get_possible_moves(node):
    possible_moves = []

    return_tuple_left = move_left(node)
    return_tuple_right = move_right(node)
    return_tuple_up = move_up(node)
    return_tuple_down = move_down(node)
    return_tuple_wrap = move_wrap(node)
    return_tuple_diagonal = move_diagonal(node)

    if return_tuple_left[0]:
        possible_moves.append(return_tuple_left[1])
    if return_tuple_right[0]:
        possible_moves.append(return_tuple_right[1])
    if return_tuple_up[0]:
        possible_moves.append(return_tuple_up[1])
    if return_tuple_down[0]:
        possible_moves.append(return_tuple_down[1])
    if return_tuple_wrap[0]:
        possible_moves.append(return_tuple_wrap[1])
    if return_tuple_diagonal[0]:
        possible_moves.append(return_tuple_diagonal[1])
        possible_moves.append(return_tuple_diagonal[2])

    return possible_moves


# Heuristic 0
def get_heuristic_zero(board):
    result = 0
    li = list(board.split(" "))

    index_of_empty = li.index('0')
    if (index_of_empty == 7):
        result = 0
    elif (index_of_empty != 7):
        result += 1

    return result


# Heuristic 1
# Hamming Distance
def get_hamming_distance(board):
    hamming_distance1 = 0
    hamming_distance2 = 0
    solution1 = [1, 2, 3, 4, 5, 6, 7, 0]
    solution2 = [1, 3, 5, 7, 2, 4, 6, 0]

    tempboard = []
    li = list(board.split(" "))

    for x in range(len(li)):
        t = int(li[x])
        tempboard.append(t)

    for x in range(8):
        # Hamming distance for solution 1
        if (tempboard[x] != 0 and tempboard.index(tempboard[x]) != solution1.index(tempboard[x])):
            hamming_distance1 += 1

        # Hamming distance for solution 2
        if (tempboard[x] != 0 and tempboard.index(tempboard[x]) != solution2.index(tempboard[x])):
            hamming_distance2 += 1

    return min(hamming_distance1, hamming_distance2)


# Heuristic 2
# Sum of permutation inversions
def get_number_of_misplaced_tiles(tempboard):
    li = list(tempboard.split(" "))
    length = len(li)
    result1 = 0
    result2 = 0
    board = []

    for x in range(len(li)):
        t = int(li[x])
        board.append(t)

    # Calculates the sum of smaller elements to the right of each element in the board for solution 1
    for i in range(length):
        for j in range(i + 1, length):
            if (board[j] < board[i]):
                result1 += 1

    # Calculate the sum of misplaced tiles for solution 2
    for i in range(length):
        for j in range(i + 1, length):
            if (board[i] == 0 and board[j] > board[i]):
                result2 += 1
            elif (board[i] == 2 and (board[j] == 1 or board[j] == 3 or board[j] == 5 or board[j] == 7)):
                result2 += 1
            elif (board[i] == 3 and board[j] == 1):
                result2 += 1
            elif (board[i] == 4 and (board[j] == 1 or board[j] == 3 or board[j] == 5 or board[j] == 7 or board[j] == 2)):
                result2 += 1
            elif (board[i] == 5 and (board[j] == 1 or board[j] == 3)):
                result2 += 1
            elif (board[i] == 6 and (board[j] == 1 or board[j] == 3 or board[j] == 5 or board[j] == 7 or board[j] == 2 or board[j] == 4)):
                result2 += 1
            elif (board[i] == 7 and (board[j] == 1 or board[j] == 3 or board[j] == 5)):
                result2 += 1

    return min(result1, result2)


def get_h_score(option, state):
    if option == 0:
        return get_heuristic_zero(state)
    elif option == 1:
        return get_hamming_distance(state)
    elif option == 2:
        return get_number_of_misplaced_tiles(state)
    else:
        return "enter a valid heuristic option"


def filter_invalid_moves(explored_list, init, goalstate):
    """Filter invalid moves by reverse parsing the explored set and creating a final path list"""
    if (GoalPuzzle(goalstate[1]) == False):
        return "no solution"

    #print("\nExplored List", explored_list)
    final_path = []
    #print("Size of explored_list:", len(explored_list))
    i = 0
    currentn = explored_list[i]
    final_path.append(currentn)
    #print("Initial Node", currentn)

    while currentn != goalstate:
        if (i + 1 > (len(explored_list) - 1)):
            # do something
            string = "Dead end found at: (" + str(currentn[0]) + ", " + str(currentn[1]) + ")"
            #print(string)

            explored_list.remove(currentn)
            final_path.remove(currentn)

            lastfpn = final_path[len(final_path) - 1]
            i = explored_list.index(lastfpn)
            #print("Value of i:", i)

            currentn = explored_list[i]

            string = "\nCurrent Node: (" + str(currentn[0]) + ", " + str(currentn[1]) + ")"
            #print(string)

            nextn = explored_list[i + 1]
            string = "New Next Node: (" + str(nextn[0]) + ", " + str(nextn[1]) + ")"
            #print(string)
        else:
            nextn = explored_list[i + 1]
        possible_moves = get_possible_moves(currentn)

        if (isInQueue(nextn[1], possible_moves)):
            string = "Found Next Node: (" + str(nextn[0]) + ", " + str(nextn[1]) + ")"
            #print(string)
            final_path.append(nextn)
            currentn = nextn
        i += 1
    return final_path


def greedy_best_first_search(board, pmfilename, spfilename, i):
    print("\nThis is the Greedy Best-First Search Algorithm for Puzzle", i, "with Heuristic", heuristics_option)

    """Change the index in board[x] depending on puzzle number"""
    h_score = get_h_score(heuristics_option, board)
    initialState = (h_score, board, 0)

    priorityQueue = PriorityQueue()
    priorityQueue.put(initialState)
    explored = []

    tempPriorityQueue = []
    tempPriorityQueue.append(initialState)
    currentNode = (0, 0, 0)
    i = 0

    t_initial = time.time()
    t_end = time.time() + 60

    while priorityQueue.qsize() > 0 and time.time() < t_end:
        currentNode = priorityQueue.get()
        string = "\nCurrent Node: (" + str(currentNode[0]) + ", " + str(currentNode[1]) + ")"
        #print(string)
        tempPriorityQueue.remove(currentNode)

        if currentNode not in explored:
            explored.append(currentNode)

        # If the puzzle solution is found
        if (GoalPuzzle(currentNode[1])):
            print("Solution Found")
            break

        possible_actions = get_possible_moves(currentNode)
        for child_node in possible_actions:
            string = "\nCurrent Node: (" + str(child_node[0]) + ", " + str(child_node[1]) + ")"
            #print(string)

            #print("Is Current Child Node in Open List?")
            #print(isInQueue(child_node[1], tempPriorityQueue))

            #print("Is Current Child Node not in Closed List?")
            #print(isInQueue(child_node[1], explored))

            if (isInQueue(child_node[1], tempPriorityQueue) == False) and (isInQueue(child_node[1], explored) == False):
                priorityQueue.put(child_node)
                tempPriorityQueue.append(child_node)

                #print("Adding this child node to open list")
                priorityQueue.put(child_node)
                tempPriorityQueue.append(child_node)
                renewQueue(child_node, tempPriorityQueue)
        i += 1

    # stopping the timer if a solution is found in less than 60 seconds
    t_final = time.time() - t_initial
    print("Execution time:", t_final)

    final_path = filter_invalid_moves(explored, initialState, currentNode)
    print("Final Path:", final_path)

    t_string = ""

    if final_path != "no solution":
        cost_of_path = final_path[len(final_path)-1][2]
        t_string = str(cost_of_path) + " " + str(t_final)
    else:
        explored = "no solution"

    output_pathmoves_to_file(pmfilename, final_path, t_string)
    output_searchpath_to_file(spfilename, explored)


def gbfs(board, i):
    print("\nThis is the Greedy Best-First Search Algorithm for Puzzle", i, "with Heuristic", heuristics_option)

    """Change the index in board[x] depending on puzzle number"""
    g_score = 0
    h_score = get_h_score(heuristics_option, board)
    initialState = (h_score, board, g_score)

    priorityQueue = PriorityQueue()
    priorityQueue.put(initialState)
    explored = []

    tempPriorityQueue = []
    tempPriorityQueue.append(initialState)
    currentNode = (0, 0, 0)
    i = 0

    t_initial = time.time()
    t_end = time.time() + 60

    while priorityQueue.qsize() > 0: #and time.time() < t_end:
        currentNode = priorityQueue.get()
        string = "\nCurrent Node: (" + str(currentNode[0]) + ", " + str(currentNode[1]) + ")"
        #print(string)
        tempPriorityQueue.remove(currentNode)

        if currentNode not in explored:
            explored.append(currentNode)

        # If the puzzle solution is found
        if (GoalPuzzle(currentNode[1])):
            #print("Solution Found")
            break

        possible_actions = get_possible_moves(currentNode)
        for child_node in possible_actions:
            string = "\nCurrent Node: (" + str(child_node[0]) + ", " + str(child_node[1]) + ")"
            #print(string)

            #print("Is Current Child Node in Open List?")
            #print(isInQueue(child_node[1], tempPriorityQueue))

            #print("Is Current Child Node not in Closed List?")
            #print(isInQueue(child_node[1], explored))

            if (isInQueue(child_node[1], tempPriorityQueue) == False) and (isInQueue(child_node[1], explored) == False):
                priorityQueue.put(child_node)
                tempPriorityQueue.append(child_node)

                #print("Adding this child node to open list")
                priorityQueue.put(child_node)
                tempPriorityQueue.append(child_node)
                renewQueue(child_node, tempPriorityQueue)
        i += 1

    # stopping the timer if a solution is found in less than 60 seconds
    t_final = time.time() - t_initial
    print("Execution time:", t_final)

    final_path = filter_invalid_moves(explored, initialState, currentNode)
    print("Final Path:", final_path)

    t_string = ""

    if final_path != "no solution":
        cost_of_path = final_path[len(final_path)-1][2]
        t_string = str(cost_of_path) + " " + str(t_final)
    else:
        explored = "no solution"

    return final_path, t_string, explored


def main():
    board = getPuzzleFromCSV(filename)
    i = 0

    for brds in board:
        pathmovefilename = str(i) + "_gbfs-h" + str(heuristics_option) + "_solution.txt"
        searchpathfilename = str(i) + "_gbfs-h" + str(heuristics_option) + "_search.txt"
        greedy_best_first_search(brds, pathmovefilename, searchpathfilename, i)
        i += 1


if __name__ == "__main__":
    main()
