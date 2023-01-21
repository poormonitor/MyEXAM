import os
import subprocess
import sys
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from misc.auth import get_user_token
from misc.s3 import delete_object_from_s3, get_presigned_put_url
from models import get_db
from models.exam import Exam
from models.examgroup import ExamGroup
from models.file import File
from models.paper import Paper
from models.task import Task
from models.union import Union

router = APIRouter()


class NewUnion(BaseModel):
    name: str
    member: str


class NewExamGroup(BaseModel):
    name: str
    date: date
    nid: str


class NewExam(BaseModel):
    egid: str
    course: int
    grade: int
    date: date


class NewFile(BaseModel):
    name: str
    pid: str


class DeleteFile(BaseModel):
    fid: str


class ConfirmFile(BaseModel):
    fid: str
    type: int


class NewConfirm(BaseModel):
    pid: str
    eid: str
    comment: str

    files: List[ConfirmFile]


@router.post("/union")
def new_union(data: NewUnion, db: Session = Depends(get_db)):
    union = db.query(Union).filter_by(name=data.name).first()
    if union:
        return {"result": "success", "nid": union.nid}

    new_union = Union(**vars(data))
    db.add(new_union)
    db.commit()
    db.refresh(new_union)
    return {"result": "success", "nid": new_union.nid}


@router.post("/examgroup")
def new_examgroup(data: NewExamGroup, db: Session = Depends(get_db)):
    new_examgroup = ExamGroup(**vars(data))
    db.add(new_examgroup)
    db.commit()
    db.refresh(new_examgroup)
    return {"result": "success", "egid": new_examgroup.egid}


@router.post("/exam")
def new_exam(data: NewExam, db: Session = Depends(get_db)):
    exam_ext = db.query(Exam).filter_by(egid=data.egid, course=data.course).first()
    if exam_ext:
        return {"result": "success", "eid": exam_ext.eid}

    new_exam = Exam(**vars(data))
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    return {"result": "success", "eid": new_exam.eid}


@router.post("/paper")
def new_paper(db: Session = Depends(get_db)):
    new_paper = Paper()
    db.add(new_paper)
    db.commit()
    db.refresh(new_paper)
    return {"result": "success", "pid": new_paper.pid}


@router.post("/file")
def new_file(data: NewFile, db: Session = Depends(get_db)):
    ext = os.path.splitext(data.name)[1].replace(".", "")
    new_file = File(**vars(data), ext=ext)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    upload_url, key = get_presigned_put_url(ext, new_file.fid)
    return {"result": "success", "fid": new_file.fid, "url": upload_url, "key": key}


@router.post("/delete_file")
def delete_file(data: DeleteFile, db: Session = Depends(get_db)):
    file = db.query(File).filter_by(fid=data.fid).first()

    if not file:
        raise HTTPException(status_code=404, detail="项目未找到。")

    delete_object_from_s3(file.ext, file.fid)
    db.delete(file)
    db.commit()
    return {"result": "success"}


@router.post("/confirm")
def confirm_paper(
    data: NewConfirm,
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(get_user_token),
):
    paper = db.query(Paper).filter_by(pid=data.pid).first()

    if not paper:
        raise HTTPException(status_code=404, detail="项目未找到。")

    paper.comment = data.comment
    paper.created_at = func.now()
    paper.uploader_ip = request.client.host
    paper.user_token = token
    paper.eid = data.eid
    paper.status = 1

    files = db.query(File).filter_by(pid=data.pid).all()
    target = {i.fid: i.type for i in data.files}
    for i in files:
        if i.fid in target:
            i.type = target[i.fid]
            i.upload_time = func.now()
        else:
            delete_object_from_s3(i.ext, i.fid)
            db.delete(i)

    processing = db.query(Task).count()

    for fid in target.keys():
        task = Task(type="ocr", data=fid)
        db.add(task)

    db.commit()

    if not processing:
        current = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current, "..", "misc", "ocr.py")
        subprocess.Popen([sys.executable, path])

    db.commit()
    return {"result": "success"}
