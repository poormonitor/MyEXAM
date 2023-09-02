from itertools import groupby
from typing import Dict, List

from sqlalchemy.orm import Session

from models.exam import Exam
from models.examgroup import ExamGroup
from models.file import File
from models.jump import Jump
from models.paper import Paper
from models.task import Task
from models.union import Union
from models.user import User


def get_courses(lst: List[Exam]) -> Dict[int, List[int]]:
    courses = {}
    for k, g in groupby(lst, lambda x: x.grade):
        courses[k] = list({(c.course, c.eid) for c in g})
    return courses


def get_owner(uid: str, db: Session):
    owner = db.query(User).filter_by(uid=uid).filter_by(admin=True).first()
    return owner.nick if owner else None


def create_admin():
    from hashlib import sha256
    from misc.auth import hash_passwd
    from models.user import User
    from models import get_db

    db = list(get_db())[0]
    admin = db.query(User).filter_by(admin=True).count()
    if not admin:
        passwd = hash_passwd(sha256("admin".encode("utf-8")).hexdigest())
        admin = User(email="root@localhost", nick="管理员", passwd=passwd, admin=True)
        db.add(admin)
        db.commit()


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
