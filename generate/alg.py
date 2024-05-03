import random
import math
from sympy import Rational

class Generate():
    def __init__(self) -> None:
        self.nums_to_divide = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 
                               26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50, 
                               51, 52, 54, 55, 56, 57, 58, 60, 62, 63, 64, 65, 66, 68, 69, 70, 72, 74, 75, 
                               76, 77, 78, 80, 81, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100]


    def simple_examples(self):
        sign = "+" if random.random() > 0.5 else "-"
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
            
    def generate_prime(self):
        while True:
            num = random.randint(1, 20)
            if num > 1:
                for i in range(2, num):
                    if (num % i) == 0:
                        break
                else:
                    return num

    def generate_quadratic_equation(self):
    # Генерация рациональных коэффициентов для квадратного уравнения
        a = Rational(random.randint(-10, 10), random.randint(1, 10))
        b = Rational(random.randint(-10, 10), random.randint(1, 10))
    
    # Генерация простых корней
        root1 = Rational(self.generate_prime())
        root2 = Rational(self.generate_prime())
    
    # Построение квадратного уравнения
        c = a * root1 * root2 + b * (root1 + root2)
    
        return a, b, c, root1, root2
            
if __name__ == "__main__":
    print("function to generate various mathematical examples")
else:
    Generate()