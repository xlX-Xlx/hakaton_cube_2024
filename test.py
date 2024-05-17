from oge_ege_tasks.ege_oge_tasks import GIATasks

tasks = GIATasks()

oge_task = tasks.get_random_oge_task()
print(oge_task)

ege_task = tasks.get_random_oge_task()
print(ege_task)

example = [oge_task['condition'], oge_task['answer']]  
print(example)
