import os
import sys
import numpy as np


num_seeds = int(sys.argv[1])
num_levels = 10
# randomly generate seed values
seeds = np.random.randint(1, 100, num_seeds)
marks = np.zeros(num_seeds)
levels = np.zeros((num_seeds, num_levels))

for i in range(num_seeds):
    os.system(f"python3 main.py --level-all --no-render --seed {seeds[i]} > test.txt")
    with open('test.txt') as f:
        lines = f.readlines()
        for line in lines:
            if "#### Marks" in line:
                marks[i] = float(line.split()[3])
            if "Level " in line:
                parts = line.split()
                if parts[2] == "passed":
                    levels[i][int(parts[1])] = 1
                else:
                    levels[i][int(parts[1])] = 0
    os.system("rm test.txt")

# Print a tabular form with Seed, Levels with Tick and Cross, Final Marks
print("Seed\t", end="")
for i in range(num_levels):
    print(f"{i}\t", end="")
print("Marks")
for i in range(num_seeds):
    print(f"{seeds[i]}\t", end="")
    for j in range(num_levels):
        if levels[i][j] == 1:
            print("✔\t", end="")
        else:
            print("✘\t", end="")
    print(f"{marks[i]}")

# Print the average marks
print(f"Average Marks : {np.mean(marks)}")

# Print the average number of levels passed
print(f"Average Levels Passed : {np.mean(np.sum(levels, axis=1))}")
