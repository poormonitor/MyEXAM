import os
import subprocess
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from misc.s3 import delete_objects_from_s3
from models import get_db
from models.exam import Exam
from models.examgroup import ExamGroup
from models.file import File
from models.paper import Paper
from models.union import Union

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
    delete_objects_from_s3([(i.fid, i.ext) for i in files.all()])
    files.delete(synchronize_session="fetch")

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
    delete_objects_from_s3([(i.fid, i.ext) for i in files.all()])
    files.delete(synchronize_session="fetch")

    db.commit()

    return {"result": "success"}


@router.post("/upgrade")
def upgrade_server():
    current = os.path.dirname(__file__)
    print(os.path.join(current, ".."))
    subprocess.Popen(["git", "pull"], cwd=os.path.join(current, ".."))
    subprocess.Popen(["yarn", "build"], cwd=os.path.join(current, "..", "views"))

    return {"result": "success"}
