from typing import List, Dict
from itertools import groupby

from models.exam import Exam
from models.examgroup import ExamGroup
from models.file import File
from models.paper import Paper
from models.union import Union
from models.user import User
from models.task import Task
from models.jump import Jump


def get_courses(lst: List[Exam]) -> Dict[int, List[int]]:
    courses = {}
    for k, g in groupby(lst, lambda x: x.grade):
        courses[k] = list({(c.course, c.eid) for c in g})
    return courses


model_map = {
    "exam": [Exam, "eid"],
    "examgroup": [ExamGroup, "egid"],
    "file": [File, "fid"],
    "paper": [Paper, "pid"],
    "union": [Union, "nid"],
    "user": [User, "uid"],
    "task": [Task, "tid"],
    "jump": [Jump, "jid"],
}
