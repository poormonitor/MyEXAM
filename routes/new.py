import os
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from models import get_db
from models.exam import Exam
from models.examgroup import ExamGroup
from models.file import File
from models.paper import Paper
from models.union import Union
from misc.s3 import delete_from_s3, get_presigned_post_url, get_file_local
from misc.ocr import WriteOCR

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
    upload_url, key = get_presigned_post_url(ext, new_file.fid)
    return {"result": "success", "fid": new_file.fid, "url": upload_url, "key": key}


@router.post("/delete_file")
def delete_file(data: DeleteFile, db: Session = Depends(get_db)):
    file = db.query(File).filter_by(fid=data.fid).first()
    if file:
        delete_from_s3(file.ext, file.fid)
        db.delete(file)
        db.commit()
        return {"result": "success"}
    raise HTTPException(status_code=404, detail="The file you request does not exist.")


@router.post("/confirm")
def delete_file(
    data: NewConfirm,
    background: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    paper = db.query(Paper).filter_by(pid=data.pid).first()
    paper.comment = data.comment
    paper.created_at = func.now()
    paper.uploader_ip = request.client.host
    paper.user_token = request.headers.get("X-MyExam-Token", "")
    paper.eid = data.eid
    paper.receipt = True

    files = db.query(File).filter_by(pid=data.pid).all()
    target = {i.fid: i.type for i in data.files}
    for i in files:
        if i.fid in target:
            i.type = target[i.fid]
            i.upload_time = func.now()
            tempfile = get_file_local(i.ext, i.fid)
            background.add_task(WriteOCR, tempfile, i.ext, i.fid, db)
        else:
            db.delete(i)

    db.commit()
    return {"result": "success"}
