import os
import subprocess
import sys
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import get_version, get_dependencies
from misc.s3 import delete_objects_from_s3, list_object_hash
from models import get_db
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
    delete_objects_from_s3([(i.md5, i.ext) for i in files.all()])
    files.delete(synchronize_session="fetch")
    db.commit()

    return {"result": "success"}


@router.post("/isolate")
def clean_isolate(db: Session = Depends(get_db)):
    db.query(ExamGroup).filter(~ExamGroup.nid.in_(db.query(Union.nid))).delete()
    db.query(Exam).filter(~Exam.egid.in_(db.query(ExamGroup.egid))).delete()
    db.query(Paper).filter(~Paper.eid.in_(db.query(Exam.eid))).delete()
    db.commit()

    files = db.query(File).filter(~File.pid.in_(db.query(Paper.pid)))
    delete_objects_from_s3([(i.md5, i.ext) for i in files.all()])
    files.delete(synchronize_session="fetch")
    db.commit()

    return {"result": "success"}


@router.post("/miss")
def clean_miss(db: Session = Depends(get_db)):
    hash = list_object_hash()

    db.query(File).filter(~File.md5.in_(hash)).delete()
    db.commit()

    return {"result": "success"}


@router.get("/statistic")
def clean_miss(db: Session = Depends(get_db)):
    union = db.query(Union).count()
    examgroup = db.query(ExamGroup).count()
    exam = db.query(Exam).count()
    paper = db.query(Paper).count()
    file = db.query(File).count()
    user = db.query(User).count()
    task = db.query(Task).count()

    latest_task = db.query(Task).order_by(Task.created.asc()).first()

    return {
        "cnt": {
            "union": union,
            "examgroup": examgroup,
            "exam": exam,
            "paper": paper,
            "file": file,
            "user": user,
            "task": task,
        },
        "version": get_version(),
        "deps": get_dependencies(),
        "task": latest_task,
    }


@router.post("/upgrade")
def upgrade_server():
    path = os.path.join(os.path.dirname(__file__), "..")

    cmd = ["git", "pull"]
    subprocess.run(cmd, cwd=path, shell=True)

    cmd = [sys.executable, "-m", "alembic", "upgrade", "head"]
    subprocess.Popen(cmd, cwd=path, shell=True)
    cmd = ["yarn", "build"]
    subprocess.Popen(cmd, cwd=os.path.join(path, "views"), shell=True)

    if sys.platform == "linux":
        cmd = ["systemctl", "restart", "myexam"]
        subprocess.Popen(cmd, cwd=path, shell=True)

    return {"result": "success"}
