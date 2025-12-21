#Given a list let's see how to double each element of the given list. Using map()
a = [1, 2, 3, 4]
print(list(map(lambda x: x*2,a)))
#Expected Output: [2, 4, 6, 8]

#Use filter() and lambda to extract all even numbers from a list of integers.
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(list(filter(lambda x: x%2==0,numbers)))
#Expected Output: [2, 4, 6, 8, 10]

#Use reduce() and lambda to find the longest word in a list of strings.
from functools import reduce
words = ["apple", "banana", "cherry", "date"]
print(reduce(lambda x,y: x if len(x)>=len(y) else y,words))
#Expected Output: 'banana'

#Use map() to square each number in the list and round the result to one decimal place.
my_floats = [4.35, 6.09, 3.25, 9.77, 2.16, 8.88, 4.59]
print(list(map(lambda x: round(x,1),my_floats)))
#Expected Output: [18.9, 37.1, 10.6, 95.5, 4.7, 78.9, 21.1]

#Use filter() to select names with 7 or fewer characters from the list.
my_names = ["olumide", "akinremi", "josiah", "temidayo", "omoseun"]
print(list(filter(lambda x: len(x)<=7,my_names)))
#Expected Output: ['olumide', 'josiah', 'omoseun']

#Use reduce() to calculate the sum of all numbers in a list.
sumOfNumbers = [1, 2, 3, 4, 5]
print(reduce(lambda x,y: x+y,sumOfNumbers))
