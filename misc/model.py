from typing import List, Dict
from itertools import groupby

from models.exam import Exam


def get_courses(lst: List[Exam]) -> Dict[int, List[int]]:
    courses = {}
    for k, g in groupby(lst, lambda x: x.grade):
        courses[k] = list({c.course for c in g})
    return courses
