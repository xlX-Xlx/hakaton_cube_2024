import random

from sdamgia import SdamGIA
import json

OGE_NUMS = ['6', '7', '8', '9', '10', '12', '14', '19']
EGE_NUMS = ['4', '5', '6', '7', '10', '16', '19', '8']


class GIATasks:
    def __init__(self):
        # Install modified sdamgia from git: pip install git+https://github.com/CanisLupus25/sdamgia-api-extended@usable
        self.__OGE = SdamGIA(exam='oge')
        self.__EGE = SdamGIA()

    def __get_tasks(self, exam, task_numbers):
        if exam == 'oge':
            sdam_gia = self.__OGE
            exam_name = 'oge'
        else:
            sdam_gia = self.__EGE
            exam_name = 'ege'
        catalogue = sdam_gia.get_catalog('math')
        categories = []
        for topic in catalogue:
            if task_numbers is None or topic['topic_id'] in task_numbers:
                for category in topic['categories']:
                    categories.append(category['category_id'])
        main_ids = set(sdam_gia.get_category_by_id('math', categories))
        temp_problems = list(filter(lambda s: s['only_text'], sdam_gia.get_problem_by_id('math', main_ids)))
        tp_dict = {}
        for prob in temp_problems:
            tp_dict[prob['id']] = prob['condition']['text']
        tp_file = open(f"temp_{exam_name}_probs.json", mode='w', encoding='UTF-8')
        json.dump(tp_dict, tp_file, ensure_ascii=False, indent=4)
        tp_file.close()
        all_problems = set()
        for prob in temp_problems:
            for analog in prob['analogs']:
                if analog.isdigit():
                    all_problems.add(analog)
        ap_file = open(f"all_{exam_name}_problems.txt", mode='w', encoding='UTF-8')
        ap_file.write('\n'.join(all_problems))
        ap_file.close()

    def write_oge_task_base(self):
        self.__get_tasks('oge', OGE_NUMS)

    def write_ege_task_base(self):
        self.__get_tasks('ege', EGE_NUMS)

    def __get_task(self, exam, task_number):
        if task_number is None:
            if exam == 'oge':
                sdam_gia = self.__OGE
                try:
                    file = open('all_oge_problems.txt', encoding='UTF-8')
                except FileNotFoundError:
                    self.write_oge_task_base()
                    file = open('all_oge_problems.txt', encoding='UTF-8')
            else:
                sdam_gia = self.__EGE
                try:
                    file = open('all_ege_problems.txt', encoding='UTF-8')
                except FileNotFoundError:
                    self.write_ege_task_base()
                    file = open('all_ege_problems.txt', encoding='UTF-8')
            tasks = file.readlines()
            problem = sdam_gia.get_problem_by_id('math', [str(tasks[random.randrange(0, len(tasks))])])
        else:
            if exam == 'oge':
                sdam_gia = self.__OGE
            else:
                sdam_gia = self.__EGE
            problem = sdam_gia.get_problem_by_id('math', task_number)[0]
        return problem

    def validate(self, problem):
        try:
            floated = float(problem[0]['answer'].replace(',', '.'))
        except Exception:
            return False
        return problem and problem[0]['only_text'] and floated == float(int(floated))

    def get_randowm_oge_task(self):
        for _ in range(20):
            result = self.__get_task('oge', None)
            if self.validate(result):
                break
        if result:
            result = result[0]
            return {
                'ok': True,
                'id': result['id'],
                'condition': result['condition']['text'],
                'answer': result['answer']
            }
        else:
            return {
                'ok': False,
                'id': '0',
                'condition': 'Не удалось получить задачу',
                'answer': '0'
            }

    def get_randowm_ege_task(self):
        for _ in range(20):
            result = self.__get_task('ege', None)
            if self.validate(result):
                break
        if result:
            result = result[0]
            return {
                'ok': True,
                'id': result['id'],
                'condition': result['condition']['text'],
                'answer': result['answer']
            }
        else:
            return {
                'ok': False,
                'id': '0',
                'condition': 'Не удалось получить задачу',
                'answer': '0'
            }


if __name__ == '__main__':
    tasks = GIATasks()
    print('Wait...')
    for _ in range(10):
        print(tasks.get_randowm_oge_task())
    print('Wait...')
    for _ in range(10):
        print(tasks.get_randowm_ege_task())
