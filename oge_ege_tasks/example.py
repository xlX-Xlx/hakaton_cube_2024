import pprint

from oge_ege_tasks.ege_oge_tasks import GIATasks

tasks = GIATasks()
pprint.pprint(tasks.get_randowm_oge_task())
pprint.pprint(tasks.get_randowm_ege_task())