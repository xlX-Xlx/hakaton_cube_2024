import math
import random

nums_to_divide = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 
                    26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50, 
                    51, 52, 54, 55, 56, 57, 58, 60, 62, 63, 64, 65, 66, 68, 69, 70, 72, 74, 75, 
                    76, 77, 78, 80, 81, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100]

signs = ["+", "-", ":", "×"]
uneq_signs = [">", "<", ">=", "<="]

def forDivide(a):
    divisors = []
    for i in range(1, int(math.sqrt(a) + 1)):
        if a % i == 0:
            divisors.append(i)
            if i != a // i:
                divisors.append(a // i)

    return sorted(divisors)[1:-1][random.randint(0, len(divisors) - 3)]

def calc(a, b, sign):
    if sign == "+":
        return a + b
    elif sign == "-":
        return a - b
    elif sign == ":":
        return a // b
    elif sign == "×":
        return a * b
    
def check_sign(sign, a=None):
    if sign == ":":
        a = nums_to_divide[random.randint(0, len(nums_to_divide) - 1)]
        b = forDivide(a)
    elif sign == "×":
        a = random.randint(1, 10) if not a else a
        b = random.randint(1, 10)
    else:
        a = random.randint(1, 50) if not a else a
        b = random.randint(1, 50 if not a else a)

    return a, b