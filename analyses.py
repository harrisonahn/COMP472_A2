import ucs
import csv
import puzzlegenerator



def main():
    #puzzlegenerator.generate_puzzles()
    board = ucs.RetrievePuzzleFromCSV('puzzles.txt')
    nosol = "no solution"
    print(board)
    a = []
    i=0
    for brds in board:
        temp = ucs.uniform_cs(brds)
        a.append(temp)
        i=i+1

    print(a[0])
    average_pm_length = []
    average_ns_length = []
    average_sp_length = []
    a_cost = []
    a_time = []
    i = 0
    for item in a:
        if item[0] != nosol:
            sl = len(item[0])
            #print(sl)
            sp = len(item[2])
            #print(sp)
            ce = item[1].split()
            average_pm_length.append(sl)
            average_sp_length.append(sp)
            a_cost.append(int(ce[0]))
            a_time.append(float(ce[1]))
        else:
            sl = ["no solution"]
            average_ns_length.append(sl)
        i = i+1
    
    sum_of_path_lengths = 0
    for item in average_pm_length:
        sum_of_path_lengths+= item

    average_path_length = (sum_of_path_lengths/len(average_pm_length))

    sum_of_searchpath_lengths = 0
    for item in average_sp_length:
        sum_of_searchpath_lengths+= item

    average_searchpath_length = (sum_of_searchpath_lengths/len(average_sp_length))

    sum_of_nosolutions = 0
    i = 1
    for item in average_ns_length:
        sum_of_nosolutions = i
        i=i+1

    average_nosol = (sum_of_nosolutions/len(a))

    sum_of_cost = 0
    for item in a_cost:
        sum_of_cost+= item

    average_cost = (sum_of_cost/len(average_pm_length))

    sum_of_time = 0
    for item in a_time:
        sum_of_time+= item

    average_time = (sum_of_time/len(average_pm_length))

    print("total length of solution paths = "+ str(sum_of_path_lengths))
    print("average length of solution paths = "+ str(average_path_length))
    print("total length of search paths = "+ str(sum_of_searchpath_lengths))
    print("average length of search paths = "+ str(average_searchpath_length))
    print("total number of no solutions = "+ str(sum_of_nosolutions))
    print("average of no solution found = "+ str(average_nosol))
    print("total cost of solutions = "+ str(sum_of_cost))
    print("average cost of solution paths = "+ str(average_cost))
    print("total time of solutions = "+ str(sum_of_time))
    print("average time of solution paths = "+ str(average_time))





if __name__ == "__main__":
    main()

