import csv
import numpy
import math
import decimal
import pandas as pd
from collections import deque
import heapq
from queue import PriorityQueue
import time


def output_pathmoves_to_file(filename,finalpath,finaltime):
    print(finalpath)
    print(finaltime)
    with open(filename, 'w',newline='') as file:
        writer = csv.writer(file)
        if(finalpath=="no solution"):
            writer.writerow([finalpath])
        else:
            i=0
            initialn=finalpath[i][1]
            initial_string= "0 0 "+str(initialn)
            writer.writerow([initial_string])
            while i+1 < len(finalpath):
                currentn=finalpath[i]
                currentnlist = list(currentn[1].split(" "))
                current_index_of_empty = currentnlist.index('0')
                nextn=finalpath[i+1]
                nextnlist = list(nextn[1].split(" "))
                next_index_of_empty = nextnlist.index('0')
                t_string =str(currentnlist[next_index_of_empty]) + " " + str(nextn[0]-currentn[0]) +" " + str(nextn[1])
                print(t_string)
                writer.writerow([t_string])
                    #do something
                i=i+1
            writer.writerow([finaltime])
        
def output_searchpath_to_file(filename,searchpath):
    with open(filename, 'w',newline='') as file:
        writer = csv.writer(file)
        if(searchpath=="no solution"):
            writer.writerow([searchpath])
        else:
            for node in searchpath:
                t_string = str(node[0]) + " " + str(node[0]) + " 0 " + str(node[1])
                writer.writerow([t_string])
    

def CheckIfStateExists(node,list):
    if node in list:
        return True
    else:
        return False


def RenewQueue(node,list1):
    queue1 = PriorityQueue()
    for item in list1:
        if(item[1]==node[1] and item[0]>node[0]):
            list1.remove(item)
            list1.append(node)
            for item in list1:
                queue1.put(item)
    return queue1,list1



def GoalTest(solution):
    sol1 = '1 2 3 4 5 6 7 0'
    sol2 = '1 3 5 7 2 4 6 0'
    #print("Solution: "+solution)
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

def is_in_queue(x, q):
    for element in q:
        if x in element:
            return True
    return False


def move_left(node): 
    li = list(node[1].split(" ")) 
    index_of_empty = li.index('0')
    newboard = li
    newnode = (node[0],node[1])
    if (index_of_empty!=3 and index_of_empty!=7):
        possible=True
        newboard[index_of_empty],newboard[index_of_empty+1] = newboard[index_of_empty+1],newboard[index_of_empty]
        s = ' '
        newboard = s.join(newboard)
        newnode = (node[0]+1,newboard)
    else:
        possible=False

    return possible,newnode

def move_right(node): 
    li = list(node[1].split(" ")) 
    index_of_empty = li.index('0')
    newboard = li
    newnode = (node[0],node[1])
    if (index_of_empty!=0 and index_of_empty!=4):
        possible=True
        newboard[index_of_empty],newboard[index_of_empty-1] = newboard[index_of_empty-1],newboard[index_of_empty]
        s = ' '
        newboard = s.join(newboard)
        newnode = (node[0]+1,newboard)
    else:
        possible=False

    return possible,newnode

def move_up(node): 
    li = list(node[1].split(" ")) 
    index_of_empty = li.index('0')
    newboard = li
    newnode = (node[0],node[1])
    if (index_of_empty!=4 and index_of_empty!=5 and index_of_empty!=6 and index_of_empty!=7):
        possible=True
        newboard[index_of_empty],newboard[index_of_empty+4] = newboard[index_of_empty+4],newboard[index_of_empty]
        s = ' '
        newboard = s.join(newboard)
        newnode = (node[0]+1,newboard)
    else:
        possible=False

    return possible,newnode

def move_down(node): 
    li = list(node[1].split(" ")) 
    index_of_empty = li.index('0')
    newboard = li
    newnode = (node[0],node[1])
    if (index_of_empty!=0 and index_of_empty!=1 and index_of_empty!=2 and index_of_empty!=3):
        possible=True
        newboard[index_of_empty],newboard[index_of_empty-4] = newboard[index_of_empty-4],newboard[index_of_empty]
        s = ' '
        newboard = s.join(newboard)
        newnode = (node[0]+1,newboard)
    else:
        possible=False

    return possible,newnode

def move_wrap(node): 
    li = list(node[1].split(" ")) 
    index_of_empty = li.index('0')
    newboard = li
    newnode = (node[0],node[1])
    if (index_of_empty==0 or index_of_empty==4):
        possible=True
        newboard[index_of_empty],newboard[index_of_empty+3] = newboard[index_of_empty+3],newboard[index_of_empty]
        s = ' '
        newboard = s.join(newboard)
        newnode = (node[0]+2,newboard)
    elif(index_of_empty==3 or index_of_empty==7):
        possible=True
        newboard[index_of_empty],newboard[index_of_empty-3] = newboard[index_of_empty-3],newboard[index_of_empty]
        s = ' '
        newboard = s.join(newboard)
        newnode = (node[0]+2,newboard)
    else:
        possible=False

    return possible,newnode

def move_diagonal(node): 
    li = list(node[1].split(" ")) 
    li2 = list(li)
    index_of_empty = li.index('0')
    newboard1 = li
    newboard2 = li2
    newnode1 = (node[0],node[1])
    newnode2 = (node[0],node[1])
    if (index_of_empty==0):
        possible=True
        newboard1[index_of_empty],newboard1[index_of_empty+5] = newboard1[index_of_empty+5],newboard1[index_of_empty]
        s = ' '
        newboard1 = s.join(newboard1)
        newnode1 = (node[0]+3,newboard1)
        #-------------------------------
        newboard2[index_of_empty],newboard2[index_of_empty+7] = newboard2[index_of_empty+7],newboard2[index_of_empty]
        s = ' '
        newboard2 = s.join(newboard2)
        newnode2 = (node[0]+3,newboard2)
    elif(index_of_empty==3):
        possible=True
        newboard1[index_of_empty],newboard1[index_of_empty+3] = newboard1[index_of_empty+3],newboard1[index_of_empty]
        s = ' '
        newboard1 = s.join(newboard1)
        newnode1 = (node[0]+3,newboard1)
        #-------------------------------
        newboard2[index_of_empty],newboard2[index_of_empty+1] = newboard2[index_of_empty+1],newboard2[index_of_empty]
        s = ' '
        newboard2 = s.join(newboard2)
        newnode2 = (node[0]+3,newboard2)
    elif(index_of_empty==4):
        possible=True
        newboard1[index_of_empty],newboard1[index_of_empty-3] = newboard1[index_of_empty-3],newboard1[index_of_empty]
        s = ' '
        newboard1 = s.join(newboard1)
        newnode1 = (node[0]+3,newboard1)
        #-------------------------------
        newboard2[index_of_empty],newboard2[index_of_empty-1] = newboard2[index_of_empty-1],newboard2[index_of_empty]
        s = ' '
        newboard2 = s.join(newboard2)
        newnode2 = (node[0]+3,newboard2)
    elif(index_of_empty==7):
        possible=True
        newboard1[index_of_empty],newboard1[index_of_empty-5] = newboard1[index_of_empty-5],newboard1[index_of_empty]
        s = ' '
        newboard1 = s.join(newboard1)
        newnode1 = (node[0]+3,newboard1)
        #-------------------------------
        newboard2[index_of_empty],newboard2[index_of_empty-7] = newboard2[index_of_empty-7],newboard2[index_of_empty]
        s = ' '
        newboard2 = s.join(newboard2)
        newnode2 = (node[0]+3,newboard2)   
    else:
        possible=False

    return possible,newnode1,newnode2

def get_possible_moves(node):
    possible_moves = []

    ret_tuple_left = move_left(node)
    ret_tuple_right = move_right(node)
    ret_tuple_up = move_up(node)
    ret_tuple_down = move_down(node)
    ret_tuple_wrap = move_wrap(node)
    ret_tuple_diagonal = move_diagonal(node)


    if ret_tuple_left[0]:
        possible_moves.append(ret_tuple_left[1])
    if ret_tuple_right[0]:
        possible_moves.append(ret_tuple_right[1])
    if ret_tuple_up[0]:
        possible_moves.append(ret_tuple_up[1])
    if ret_tuple_down[0]:
        possible_moves.append(ret_tuple_down[1])
    if ret_tuple_wrap[0]:
        possible_moves.append(ret_tuple_wrap[1])
    if ret_tuple_diagonal[0]:
        possible_moves.append(ret_tuple_diagonal[1])
        possible_moves.append(ret_tuple_diagonal[2])
    
    return possible_moves

def filter_unvalid_moves(explored_list,init,goalstate):
    if(GoalTest(goalstate[1])==False):
        return "no solution"
    #print(explored_list)
    final_path = []
    #print("Size of explored_list")
    #print(len(explored_list) - 1)
    i=0
    currentn = explored_list[i]
    final_path.append(currentn)
    #print("initial node")
    #print(currentn)
    while currentn != goalstate:
        if(i+1>(len(explored_list)-1)):
            #do something
            #print("Dead end Found at: ")
            #print(currentn)
            explored_list.remove(currentn)
            final_path.remove(currentn)
            lastfpn = final_path[len(final_path)-1]
            #print("Value of i")
            i = explored_list.index(lastfpn)
            #print(i)
            #print("New Current Node: ")
            currentn = explored_list[i]
            #print(currentn)
            nextn= explored_list[i+1]
            #print("New Next Node: ")
            #print(nextn)
            #print(explored_list)
            #break
        else:
            nextn = explored_list[i+1]
        possible_moves = get_possible_moves(currentn)
        if(is_in_queue(nextn[1],possible_moves) and nextn[0]>currentn[0]):
            #print("found next node")
            #print(nextn)
            final_path.append(nextn)
            currentn = nextn
        i=i+1
    #final_path.reverse()
    return final_path

def uniform_cost_search(brd,pmfilename,spfilename):
    initialState = (0,brd)

    frontier = PriorityQueue()
    explored = []

    frontier.put(initialState)
    tempfrontier = []

    tempfrontier.append(initialState)
    currentNode = (0,0)
    i=0
    t_initial = time.time()
    t_end = time.time() + 60
    while(frontier.qsize()>0 and time.time()< t_end):
        currentNode = frontier.get()
        #print("Current Node: ")
        #print(currentNode)
        tempfrontier.remove(currentNode)
        explored.append(currentNode)
        if(GoalTest(currentNode[1])):
            print("Solution Found")
            print(currentNode)
            break
        possible_actions = get_possible_moves(currentNode)
        for child_node in possible_actions:
            #print("Current Child Node: ")
            #print(child_node)
            #print("Is Current Child Node in Open List?")
            #print(is_in_queue(child_node[1],tempfrontier))
            #print("Is Current Child Node not in Closed List?")
            #print(is_in_queue(child_node[1],explored))
            if (is_in_queue(child_node[1],tempfrontier)==False) and (is_in_queue(child_node[1],explored)==False):
                    #print("Adding this child node to open list")
                    #print(child_node)
                    frontier.put(child_node)
                    tempfrontier.append(child_node)
            elif(is_in_queue(child_node[1],tempfrontier)):
                temp = RenewQueue(child_node,tempfrontier)
                tempq = temp[0]
                temptq = temp[1]
                if (tempq.empty()==False):
                    #print("FOUND SAME STATE WITH LESS PATH-COST")
                    frontier = tempq
                    tempfrontier = temptq
        i=i+1
    t_final = time.time() - t_initial
    final_path = filter_unvalid_moves(explored,initialState,currentNode)
    cost_of_path = ""
    t_string=""
    if final_path!="no solution":
            cost_of_path = final_path[len(final_path)-1][0]
            t_string = str(cost_of_path)+ " "+str(t_final)
    else:
        explored="no solution"
    output_pathmoves_to_file(pmfilename,final_path,t_string)
    output_searchpath_to_file(spfilename,explored)


def main():
    board = RetrievePuzzleFromCSV('test1.txt')
    i=0
    for brds in board:
        pathmovefilename = str(i)+"_ucs_solution.txt"
        searchpathfilename = str(i)+"_ucs_search.txt"
        uniform_cost_search(brds,pathmovefilename,searchpathfilename)
        i=i+1


if __name__ == "__main__":
    main()