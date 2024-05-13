import random
import math
from sympy import Rational
import numpy as np
from nums import nums_to_divide, signs, uneq_signs, forDivide, calc, check_sign


class Simple:
    def __init__(self) -> None:
        pass

    def simple_examples(self):
        sign = "+" if random.random() > 0.5 else "-"
        a = random.randint(1, 30)
        b = random.randint(1, a if sign == "-" else 30)
        answer = a + b if sign == "+" else a - b

        return [f"{a} {sign} {b}", answer]

    def branch_examples(self):
        branches_count = random.randint(2, 4)
        branches, sums = [], 0

        for i in range(branches_count):
            sign = signs[random.randint(0, 1)]
            sign_between_branches = "+" if random.random() > 0.5 else "-"
            a = random.randint(1, 30)
            b = random.randint(1, 30 if sign == "+" else a)

            ans = calc(a, b, sign)

            if i > 0:
                if sums - ans < 0:
                    sign_between_branches = "+"
                    sums += ans
                    branches.append(f" {sign_between_branches} ({a} {sign} {b})")
                else:
                    sums = sums + ans if sign_between_branches == "+" else sums - ans
                    branches.append(f" {sign_between_branches} ({a} {sign} {b})")
            else:
                sums = ans
                branches.append(f"({a} {sign} {b})")

        return ["".join([x for x in branches]), sums]

    def multNdivide(self):
        sign = signs[random.randint(2, 3)]

        if sign == ":":
            divisors = []
            a = nums_to_divide[random.randint(1, len(nums_to_divide) - 1)]
            b = forDivide(a)
            answer = int(a / b)

            return [f"{a} : {b}", answer]
        else:
            a = random.randint(1, 10)
            b = random.randint(2, 10)

            return [f"{a} {sign} {b}", int(a * b)]


class Normal:
    def __init__(self) -> None:
        pass

    def simple_equantion(self):
        nums_of_odds = random.randint(2, 3)

        if nums_of_odds == 2:
            sign = signs[random.randint(0, 3)]

            a, b = check_sign(sign)

            nums = [a, b]
            idx = random.randint(0, 1)
            solution, nums[idx] = nums[idx], "x"
            nums[idx] = "x"

            return [f"{nums[0]} {sign} {nums[1]} = {calc(a, b, sign)}", solution]

        elif nums_of_odds == 3:
            eq_signs = []
            while True:
                eq_signs = [signs[random.randint(0, 3)] for i in range(2)]
                if (eq_signs.count(":") == 1 or eq_signs.count("×") == 1) and (
                        eq_signs.count(":") + eq_signs.count("×") < 2):
                    break

            if eq_signs[1] in signs[2:5]:
                a, b = check_sign(eq_signs[1])
                result = calc(a, b, eq_signs[1])
                _, c = check_sign(eq_signs[0], result)
                result = calc(c, result, eq_signs[0])

                nums = [c, a, b]
                idx = random.randint(0, 2)
                solution, nums[idx] = nums[idx], "x"

            else:
                a, b = check_sign(eq_signs[0])
                result = calc(a, b, eq_signs[0])

                _, c = check_sign(eq_signs[1], result)
                result = calc(result, c, eq_signs[1])

                nums = [a, b, c]
                idx = random.randint(0, 2)
                solution, nums[idx] = nums[idx], "x"

            return [f"{nums[0]} {eq_signs[0]} {nums[1]} {eq_signs[1]} {nums[2]} = {result}", solution]


