import requests
import json
import math

from config import url, header, data, nums
from promts import prompts

def generate(eqution_type, complexity):
    data["query"] = prompts[f"{eqution_type}{complexity}"] + prompts["solvability"] + prompts["const"]

    request = requests.post(url, headers=header, data=json.dumps(data))
    answer = request.json()["messages"][0]["content"]

    # return request.json()

    try:
        a, b, c = map(float, answer.split("$"))
        print(a, b, c)
    except:
        print("another try", answer)
        generate(eqution_type, complexity)

    D = b ** 2 - (4 * a * c)

    if D < 0:
        print("another try", answer, D)
        generate(eqution_type, complexity)

    return a, b, c, D

print(generate("quadratic_equations", 1))