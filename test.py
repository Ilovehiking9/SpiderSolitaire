import copy

numbers = [0, 1, 2, 3]

numbersCopy = numbers.copy()
numbersDeepCopy = copy.deepcopy(numbers)

numbersCopy[0] = 17
numbersDeepCopy[0] = 17

print(numbers)
print(numbersCopy)
print(numbersDeepCopy)