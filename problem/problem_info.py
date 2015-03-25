import os.path
from utils import config_info
from problem.models import Problem, Testcase

SPECIAL_PATH = config_info.get_config('path', 'special_judge_path')
PARTIAL_PATH = config_info.get_config('path', 'partial_judge_path')

def get_problem(problem):
    problem.testcase = Testcase.objects.filter(problem=problem)
    return problem

def has_special_judge_code(problem):
    return os.path.isfile("%s%d.c" % (SPECIAL_PATH, problem.pk))

def has_partial_judge_code(problem):
    return os.path.isfile("%s%d.c" % (PARTIAL_PATH, problem.pk))

