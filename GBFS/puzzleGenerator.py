import random
import csv

def generate_puzzles():
    currentpuzzle = list(range(8))
    newpuzzle = random.sample(currentpuzzle, len(currentpuzzle))
    print(newpuzzle)
    currentpuzzle = newpuzzle

    with open("puzzles.txt", 'w', newline='') as file:
        writer = csv.writer(file)
        i = 0
        while i < 50:
            newpuzzle = random.sample(currentpuzzle,len(currentpuzzle))
            t_string = str(newpuzzle)
            print(t_string)
            t_string = t_string.replace(',','')
            t_string = t_string.replace('[','')
            t_string = t_string.replace(']','')
            print(t_string)
            writer.writerow([t_string])
            currentpuzzle = newpuzzle
            i += 1