"""
CS 445 - Algorithms
Dynamic Programming 1 - Knapsack 0-1 Problem
April 8, 2018
Philip Park

References of code and other materials are commented below
"""
import random
import argparse
import time
import sys

def knapsackmain(n, log=False):
    """
    A instance of the Knapsack 0-1 Problem, with n items.

    To Run this Script, Open a command shell and enter arguments to get results
    When completed: look for runtime.txt for runtimes of each n item
                    look for output.txt for all output results
    """
    
    #Random Number Generator for n Items
    def random_items(): 
        to_return = []

        for x in range(n):
            random_weight = random.randint(1, n)
            random_value = random.randint(1, n)
            to_return.append(Item(random_weight, random_value))

        return to_return

    #Calculating the weight capacity of the knapsack
    def item_capacity(items):
        sum_weights = sum([item.weight for item in items])
        return int(sum_weights)

    new_items = random_items()
    input_capacity = item_capacity(new_items)

    return KnapsackVariables(n, new_items, input_capacity, log=log)


class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

    def __str__(self):
        return "{'weight': " + str(self.weight) + \
               ", 'value': " + str(self.value) + "}"


# Class containing the brute force, top-down, bottom-up variables.
"""
References:
For python classes:
https://codereview.stackexchange.com/questions/94478/python-knapsack-problem-greedy
https://docs.python.org/3/tutorial/classes.html

For import argparse uses:
https://stackoverflow.com/questions/48633847/python-argparse-errors-to-file?noredirect=1&lq=1
https://stackoverflow.com/questions/8259001/python-argparse-command-line-flags-without-arguments
"""
class KnapsackVariables:
    def __init__(self, n, items, weight_cap, log=False):    
        self.n = n
        self.items = items
        self.weight_cap = weight_cap
        self.log = log #Only Prints out each individual output line when --log is specified.
                       #A Method to hide and prevent extra time spent printing.

        if self.log:
            sys.stdout = open('output.txt', 'w') #Only prints values when --log is used. 
            print("Knapsack 0-1 Problem")
            print(" n: ", self.n)
            print(" Weight Capacity of Knapsack: ", self.weight_cap)
            print(" items:")
            for item in self.items:
                print(" \t", item)
            print("")

    sys.stdout = open('runtime.txt', 'w') # This will print a txt file when the task has been completed. Some of the time
                                          # values shows up as 0.0, because of the time module...
                                          # https://stackoverflow.com/questions/48196000/why-is-time-time-time-time-0-0?rq=1
                                          # Comment both runtime.txt and output.txt lines out, to see the output in command line
            
    def brute_force(self):
        
        def brute_force_function(cur_i, still_weight):
            """
            Recursive function that returns the total value of the items, to the maximum capacity of the knapsack
            after checking through all the elements in the range specified by the user.

            If the value of the item exceeds the maximum capacity, the system should ignore it, and the program
            will end. 
            """
            # base case: we have looked at every element or current weight is at capacity
            if cur_i == -1 or still_weight == 0:
                return 0

            if self.items[cur_i].weight > still_weight:
                return brute_force_function(cur_i - 1, still_weight)  # leave item

            # solve in both cases: take item and leave item
            take = self.items[cur_i].value + brute_force_function(cur_i - 1, still_weight - self.items[cur_i].weight)
            leave = brute_force_function(cur_i - 1, still_weight)
            
            return max(take, leave)

        Best_value = brute_force_function(self.n - 1, self.weight_cap)

        if self.log:
            print("Brute Force: \n", "Best Value: ", Best_value, "\n")

        return Best_value

    def greedy_solution(self): #Top-Down Approach
        """
        Greedy Algorithm for the top-down approach.
        Created a local class of the items to volume value, then sorted by high to low (by Volume)
        and calculates until the knapsack is full. 
        """
        class Items_Volume(Item):
            def __init__(self, weight, value):
                super().__init__(weight, value)
                self.volume = self.value/self.weight

            def __str__(self):
                return "{'weight': " + str(self.weight) + \
                       ", 'value': " + str(self.value) + \
                       ", 'volume': " + str(self.volume) + "}"

        # a new array and sorting for items with the volume of each value
        volume_of_items = [Items_Volume(item.weight, item.value) for item in self.items]
        volume_of_items.sort(key=lambda item: item.volume, reverse=True)

        if self.log:
            print("Top-Down Approach Solution\n", "Items sorted by volume: ")

        # add the values of the items from high to low (volume values)
        still_weight = self.weight_cap
        total_value = 0
        for item in volume_of_items:
            if item.weight <= still_weight:
                total_value += item.value
                still_weight -= item.weight

            if self.log:
                print("\t", item)

        if self.log:
            print(" Total value: ", total_value)
            print("")

        return total_value

    def dynamic_solution(self): #Bottom-Up Approach
        """
        A Bottom-Up Approach for the knapsack problem. (Dynamic Programming)

        The algorithm creates a two-dimensional array for each scenario of available weight, items taken,
        and fills in the array.

        Array Key:
        [row] Rows = Weights
        [col] Columns = Index Values
        """
        if self.log:
            print("Array of Values: ")

        # array for storing completed solutions
        computed_values = [[None] * (self.n + 1) for row in range(self.weight_cap + 1)]

        for row in range(self.weight_cap + 1):
            for col in range(self.n + 1):
                # return 0 if the weight_cap is reached. 
                if row == 0 or col == 0:
                    computed_values[row][col] = 0

                # if the weight of this item is less than or equal to the weight remaining,
                # get the values
                elif self.items[col-1].weight <= row:
                    my_weight = self.items[col-1].weight
                    my_value = self.items[col-1].value

                    # return the max value of the item if:
                        # calculated =  add the value and get the solution from the remaining weight value
                        # or no change. 
                    computed_values[row][col] = max(my_value + computed_values[row-my_weight][col-1],
                                                  computed_values[row][col-1])

                # if the weight is max, no change
                else:
                    computed_values[row][col] = computed_values[row][col-1]

        Best_value = computed_values[self.weight_cap][self.n]

        if self.log:
            for row in range(self.weight_cap + 1):
                for col in range(self.n + 1):
                    if col == 0:
                        print("\t[", computed_values[row][col], end=", ")
                    elif col != self.n:
                        print(computed_values[row][col], end=", ")
                    else:
                        print(computed_values[row][col], end="]\n")

            print("\nBest Value: ", Best_value, "\n")

        return Best_value

#########################################################################################################
# argument list for command-line input, found this a better strategy than manually entering the table
# especially for top-down and bottom-up approaches. 
"""
This part of the code is for running the algorithm with test cases. Use this in through shell execution.
*Define the file path first*
Example Input: python knapsack2.py --bruteforce --greedy --dynamic 100 50 75
This will then calculate per algorithm, then print the results after it has been completed.

Referenced Off:
https://www.programcreek.com/python/example/92651/argparse.parse_args
https://docs.python.org/3/library/argparse.html
https://stackoverflow.com/questions/20063/whats-the-best-way-to-parse-command-line-arguments
"""

# Does not work at the moment - because of the output to txt function, I have not found a way to generate this separate from
# the output file...the system will print the all outputs to the 'runtime.txt' file (when --log is not in use)
parser = argparse.ArgumentParser()
parser.add_argument("n_min", type=int, help="enter the minimum range value for the algorithm to generate")
parser.add_argument("n_max", type=int, help="enter the maximum range value for the algorithm to generate")
parser.add_argument("n_step", type=int, help="enter the step-wise value for the number of items (what number to jump by)")
parser.add_argument("--bruteforce", help="brute force algorithm for n = 1, 2, 3...", action="store_true")
parser.add_argument("--greedy", help="top-down algorithm for n (use values greater than 100,000, for better comparison data)", action="store_true")
parser.add_argument("--dynamic", help="bottom-up algorithm for n", action="store_true")

#Do not use --log when measuring for time, as import time module will not account for extra time taken.
#Use only for testing to make sure the code works properly. 
parser.add_argument("--log", help="use this to print out all the outputs in output.txt", action="store_true")
args = parser.parse_args()


# run algorithms as per arguments
if args.bruteforce:
    #sys.stdout = open('log.txt', 'w')
    print("Brute Force Algorithm Runtime:") #Brute Force Algorithm
    print("n\ttime (s)")
    for i in range(args.n_min, args.n_max + args.n_step, args.n_step):
        if args.log:
            my_problem = knapsackmain(i, log=True)
        else:
            my_problem = knapsackmain(i)

        # timing of algorithm, then prints
        start = time.time()
        brute_force_sln = my_problem.brute_force()
        end = time.time()

        #print("Time", "\t", (end-start)) - use this line for formatting, only in --log 
        print(i, "\t", (end-start))
        
if args.greedy:
    #sys.stdout = open('log.txt', 'w')
    print("Top-Down Approach Runtime:") #Greedy Algorithm
    print("n\ttime (s)")
    for i in range(args.n_min, args.n_max + args.n_step, args.n_step):
        if args.log:
            my_problem = knapsackmain(i, log=True)
        else:
            my_problem = knapsackmain(i)

        # timing of algorithm, then prints
        start = time.time()
        greedy_sln = my_problem.greedy_solution()
        end = time.time()

        #print("Time", "\t", (end-start)) - use this line for formatting, only in --log 
        print(i, "\t", (end-start))
        
if args.dynamic:
    #sys.stdout = open('log.txt', 'w')
    print("Bottom-Up Approach Runtime:") #Dynamic Programming Algorithm
    print("n\ttime (s)")
    for i in range(args.n_min, args.n_max + args.n_step, args.n_step):
        if args.log:
            my_problem = knapsackmain(i, log=True)
        else:
            my_problem = knapsackmain(i)

        # timing of algorithm, then prints
        start = time.time()
        dynamic_sln = my_problem.dynamic_solution()
        end = time.time()
        
        #print("Time", "\t", (end-start)) - use this line for formatting, only in --log 
        print(i, "\t", (end-start))
