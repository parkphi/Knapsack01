'''/
CS 445 Algorithms
Dynamic Programming 1: Brute Force Approach to 0-1 Knapsack Problem
Philip Park
March 26, 2019
/'''

import random
import itertools
import time

class Item:
  def __init__(self, id, weight, value):
    self.id     = id
    self.weight = weight
    self.value  = value
    
#Defining variables
    
class container:
  def __init__(self, items):
    self.items = items

  def weight(self):
    return sum([x.weight for x in self.items])

  def value(self):
    return sum([x.value for x in self.items])

  def ids(self):
    return ', '.join([str(x.id) for x in self.items])

# https://docs.python.org/3/library/functions.html
  def __repr__(self):
    return "{0:10} {1:10}   {2}".format(self.weight(), self.value(), self.ids())

"""
# https://docs.python.org/3/library/itertools.html#itertools.chain
# https://docs.python.org/2/library/itertools.html
# https://stackoverflow.com/questions/33595575/using-python-itertools-to-generate-custom-iteration
"""

def powerset(iterable):

  s = list(iterable)
  return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

def item_list(n,weightmax,valuemax):
  """
    Randomly Generates a List of Items, then returns a list of a number(ID), weight, value.
    #For each one# - simply said a random generator

    n         = number of items
    weightmax = range of weights (1, value)
    valuemax  = range of values (1, value)

"""
  items = []
  for i in range(1,n+1):
    items.append(Item(id=i, weight=random.randint(1,weightmax), value=random.randint(1,valuemax)))
  return items


def knapsack(items,capacity):
  """Lists all the possible combinations, then prints the best option."""

  time.sleep(0.5)
  FitSubSets = []
  for packitems in powerset(items):
    packing = container(packitems)
    if packing.weight()>capacity:
      continue
    #print(packing) # uncomment to see all the values of list print, it can get VERY LONG
    FitSubSets.append(packing)
  best_option = max(FitSubSets, key=lambda x: x.value())
  print("Best Option: ")
  print("{0:>10} {1:>10}   {2}".format("Weight","Value","Subset"))#Printing the Sub-titles when list is finished (especially in long lists)
  print(best_option)

# Running the code

def main():
  time.sleep(1)
print("0-1 Knapsack Problem - Brute Force Style")
time.sleep(0.5)
print("Enter the Max Capacity Weight, Item Weight Range, and Value Range to get the best option.")
time.sleep(1)
maxcapacity   = int(input("Enter Max Capacity: "))
maxweight = int(input("Enter Max Weight Range (Between 1-N): "))
maxvalue    = int(input("Enter Max Value Range (Between 1-N): "))
numitems  = int(input("Number of Items to Generate: "))

print("------------------------------")
print("Printing...\n")

start = time.time() #Variable for timing the function -using import time
knapsack(item_list(numitems,maxweight,maxvalue),maxcapacity)
print("\n")
end = time.time()

print("Time to run: ",end - start, "seconds") #prints the time calculated during process
print('------------------------------\n')
#Import Time module does not calculate out the cpu/ram processes. 



main()
