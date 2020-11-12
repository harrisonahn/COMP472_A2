import csv
import numpy
import math
import decimal
import pandas as pd
from collections import deque
import heapq
from queue import PriorityQueue

def CheckIfStateExists(node,list):
    return

def RenewQueue(node,list,queue):
    return



def GoalTest(solution):
    sol1 = '1 2 3 4 5 6 7 0'
    sol2 = '1 3 5 7 2 4 6 0'
    print("Solution: "+solution)
    if solution == sol1 or solution == sol2:
        return True
    else:
        return False


def RetrievePuzzleFromCSV(filename):
    with open(filename, 'r') as file:
        content = file.read()
        data = content.splitlines()
        file.close()
    return data


def move_left(node): 
    li = list(node.split(" ")) 
    index_of_empty = li.index('0')
    newboard = li
    if (index_of_empty!=3 or index_of_empty!=0):
        possible=True
        newboard[index_of_empty],newboard[index_of_empty+1] = newboard[index_of_empty+1],newboard[index_of_empty]
        s = ' '
        newboard = s.join(newboard)
    else:
        possible=False

    return possible,newboard

def move_right(node): 
    li = list(node.split(" ")) 
    index_of_empty = li.index('0')
    newboard = li
    if (index_of_empty!=0 or index_of_empty!=4):
        possible=True
        newboard[index_of_empty],newboard[index_of_empty-1] = newboard[index_of_empty-1],newboard[index_of_empty]
        s = ' '
        newboard = s.join(newboard)
    else:
        possible=False

    return possible,newboard


openlist = []
closedlist = []
board = RetrievePuzzleFromCSV('test1.txt')
temp = board
#print(board[0])

initialState = (0,board[0])

print(initialState)

#print(move_left(initialState[1]))



frontier = PriorityQueue()
explored = []

frontier.put(initialState)
tempfrontier = []

#if(any(str(board[0])in item for item in frontier.queue)):
    #print("True")
tempfrontier.append(initialState)


while(frontier.qsize()>0):
    currentNode = frontier.get()
    tempfrontier.remove(currentNode)
    possiblemove = PriorityQueue()
    if(GoalTest(currentNode[1])):
        print("Solution Found")
        break
    explored.append(currentNode[1])
    if(move_left(currentNode[1])[0] and (move_left(currentNode[1])[1]) not in explored):
        currentNode = (currentNode[0]+2,move_left(currentNode[1])[1])
        possiblemove.put(currentNode)
    elif(CheckIfStateExists(move_left(currentNode[1])[1],tempfrontier)[0]):
        frontier = RenewQueue(currentNode,tempfrontier,frontier)

    frontier.put(possiblemove.get())

   
    
    
        
       
        