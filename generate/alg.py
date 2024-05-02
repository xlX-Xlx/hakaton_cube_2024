import random
import math

class Generate():
    def __init__(self) -> None:
        self.nums_to_divide = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 
                               26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50, 
                               51, 52, 54, 55, 56, 57, 58, 60, 62, 63, 64, 65, 66, 68, 69, 70, 72, 74, 75, 
                               76, 77, 78, 80, 81, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100]


    def simple_examples(self, sign):
        a = random.randint(1, 30)
        b = random.randint(1, a if sign == "-" else 30)
        answer = a + b if sign == "+" else a - b

        return [f"{a} {sign} {b}", answer]

    def normal_examples(self):
        signs = ["+", "-", ":", "×"]

        if random.random() > 0.5:
            branches_count = random.randint(2, 4)

            branches, sums = [], 0

            for i in range(branches_count):
                sign = signs[random.randint(0, 1)]
                sign_between_branches = signs[random.randint(0, 1)]
                a = random.randint(1, 30)
                b = random.randint(1, 30 if sign == "+" else a)

                # branches.append(f"({a} {sign} {b})")
                ans = a + b if sign == "+" else a - b

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
        else:
            sign = signs[random.randint(2, 3)]
            
            if sign == ":":
                divisors = []
                a = self.nums_to_divide[random.randint(1, len(self.nums_to_divide) - 1)]

                for i in range(1, int(math.sqrt(a) + 1)):
                    if a % i == 0:
                        divisors.append(i)
                        if i != a // i:
                            divisors.append(a // i)

                b = sorted(divisors)[1:-1][random.randint(0, len(divisors) - 3)]
                answer = a / b

                return [f"{a} : {b}", answer]
            else:
                a = random.randint(1, 10)
                b = random.randint(2, 10)

                return [f"{a} {sign} {b}", a * b]
            
if __name__ == "__main__":
    print("function to generate various mathematical examples")
else:
    Generate()