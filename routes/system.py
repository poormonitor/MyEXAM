import os
import subprocess
import sys
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import get_version
from misc.s3 import delete_objects_from_s3, list_object_names
from models import get_db
from models.assign import Assign
from models.exam import Exam
from models.examgroup import ExamGroup
from models.file import File
from models.paper import Paper
from models.task import Task
from models.union import Union
from models.user import User

router = APIRouter()


@router.post("/clean")
def clean_paper(db: Session = Depends(get_db)):
    (
        db.query(Paper)
        .filter(Paper.status == 0)
        .filter(Paper.created_at <= datetime.now() - timedelta(hours=1))
        .delete()
    )

    files = db.query(File).filter(~File.pid.in_(db.query(Paper.pid)))
    files.delete(synchronize_session="fetch")

    assigns = db.query(Assign).filter(~Assign.egid.in_(db.query(ExamGroup.egid)))
    assigns.delete(synchronize_session="fetch")

    db.commit()

    return {"result": "success"}


@router.post("/isolate")
def clean_isolate(db: Session = Depends(get_db)):
    db.query(ExamGroup).filter(~ExamGroup.nid.in_(db.query(Union.nid))).delete(
        synchronize_session="fetch"
    )

    db.query(Exam).filter(~Exam.egid.in_(db.query(ExamGroup.egid))).delete(
        synchronize_session="fetch"
    )

    db.query(Paper).filter(~Paper.eid.in_(db.query(Exam.eid))).delete(
        synchronize_session="fetch"
    )

    files = db.query(File).filter(~File.pid.in_(db.query(Paper.pid)))
    files.delete(synchronize_session="fetch")

    assigns = db.query(Assign).filter(~Assign.egid.in_(db.query(ExamGroup.egid)))
    assigns.delete(synchronize_session="fetch")

    db.commit()

    return {"result": "success"}


@router.post("/miss")
def clean_miss(db: Session = Depends(get_db)):
    names = list_object_names()

    hashes = list(map(lambda x: x[0], names))
    db.query(File).filter(~File.md5.in_(hashes)).delete(synchronize_session="fetch")
    db.query(Assign).filter(~Assign.md5.in_(hashes)).delete(synchronize_session="fetch")

    files = db.query(File.md5).all()
    assigns = db.query(Assign.md5).all()

    hashes = [i[0] for i in files + assigns]
    delete_list = []

    for i in names:
        if i[0] not in hashes:
            delete_list.append(i)

    delete_objects_from_s3(delete_list)

    db.commit()

    return {"result": "success"}


@router.get("/statistic")
def get_statistic(db: Session = Depends(get_db)):
    union = db.query(Union).count()
    examgroup = db.query(ExamGroup).count()
    exam = db.query(Exam).count()
    paper = db.query(Paper).count()
    file = db.query(File).count()
    user = db.query(User).count()
    task = db.query(Task).count()
    assign = db.query(Assign).count()

    latest_task = db.query(Task).order_by(Task.created.asc()).first()

    return {
        "cnt": {
            "union": union,
            "examgroup": examgroup,
            "exam": exam,
            "paper": paper,
            "file": file + assign,
            "user": user,
            "task": task,
        },
        "version": get_version(),
        "task": latest_task,
    }
