import GBFS
import csv
import puzzleGenerator


def main():
    # puzzleGenerator.generate_puzzles()
    board = GBFS.getPuzzleFromCSV('puzzles.txt')
    nosol = "no solution"
    print(board)
    a = []
    i = 0

    for brds in board:
        temp = GBFS.gbfs(brds, i)
        a.append(temp)
        i += 1

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
            print(sl)
            sp = len(item[2])
            print(sp)
            ce = item[1].split()
            average_pm_length.append(sl)
            average_sp_length.append(sp)
            a_cost.append(int(ce[0]))
            a_time.append(float(ce[1]))
        else:
            sl = len(item[0])
            average_ns_length.append(sl)
        i += 1

    sum_of_path_lengths = 0
    for item in average_pm_length:
        sum_of_path_lengths+= item

    average_path_length = (sum_of_path_lengths/len(a))

    sum_of_searchpath_lengths = 0
    for item in average_sp_length:
        sum_of_searchpath_lengths+= item

    average_searchpath_length = (sum_of_searchpath_lengths/len(a))

    sum_of_nosolutions = 0
    i =0
    for item in average_ns_length:
        sum_of_nosolutions+= i
        i+=1

    average_nosol = (sum_of_nosolutions/len(a))

    sum_of_cost = 0
    for item in a_cost:
        sum_of_cost+= item

    average_cost = (sum_of_cost/len(a))

    sum_of_time = 0
    for item in a_time:
        sum_of_time += item

    average_time = (sum_of_time/len(a))

    print("---------------------------------------------\nAnalysis of GBFS Algorithm with 50 puzzles")
    print("1. Average & total length of the solution and search paths")
    print("Total length of solution paths:", sum_of_path_lengths)
    print("Average length of solution paths:", average_path_length)
    print("Total length of search paths:", sum_of_searchpath_lengths)
    print("Average length of search paths:", average_searchpath_length)

    print("\n2. Average and Total Number of no solution")
    print("Total number of no solution", sum_of_nosolutions)
    print("Average number of no solution", average_nosol)

    print("\n3. Average and total cost and execution time")
    print("Total execution time:", sum_of_time)
    print("Average execution time:", average_time)
    print("Total cost:", sum_of_cost)
    print("Average cost:", average_cost)

    #print("\n4. Optimality of the solution path")


if __name__ == "__main__":
    main()