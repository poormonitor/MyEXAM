import os
import subprocess
import sys
from datetime import date
from typing import List, Tuple

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from misc.auth import get_current_user
from misc.s3 import get_presigned_post_url
from models import get_db
from models.assign import Assign
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
    md5: str
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


class NewAssign(BaseModel):
    ext: str
    md5: str


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

    file = db.query(File).filter_by(ext=ext).filter_by(md5=data.md5).first()

    new_file = File(**vars(data), ext=ext)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    if file:
        return {"result": "exists", "fid": new_file.fid}
    else:
        upload_url, key = get_presigned_post_url(ext, data.md5)
        return {"result": "success", "fid": new_file.fid, "url": upload_url, "key": key}


@router.post("/delete_file")
def delete_file(data: DeleteFile, db: Session = Depends(get_db)):
    file = db.query(File).filter_by(fid=data.fid).first()

    if not file:
        raise HTTPException(status_code=404, detail="项目未找到。")

    db.delete(file)
    db.commit()
    return {"result": "success"}


@router.post("/confirm")
def confirm_paper(
    data: NewConfirm,
    request: Request,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    paper = db.query(Paper).filter_by(pid=data.pid).first()

    if not paper:
        raise HTTPException(status_code=404, detail="项目未找到。")

    paper.comment = data.comment
    paper.created_at = func.now()
    paper.uploader_ip = request.client.host
    paper.user_token = user
    paper.eid = data.eid
    paper.status = 1

    files = db.query(File).filter_by(pid=data.pid).all()
    target = {i.fid: i.type for i in data.files}
    for i in files:
        if i.fid in target:
            i.type = target[i.fid]
            i.upload_time = func.now()

            same = (
                db.query(File)
                .filter(File.md5 == i.md5)
                .filter(File.ocr != None)
                .filter(File.fid != i.fid)
                .order_by(File.upload_time.desc())
                .first()
            )
            if same:
                i.ocr = same.ocr
            else:
                task = Task(type="ocr", data=i.fid)
                db.add(task)

        else:
            db.delete(i)
    
    db.commit()

    processing = db.query(Task).count()

    if not processing:
        current = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current, "..", "misc", "ocr.py")
        subprocess.Popen([sys.executable, path])

    db.commit()
    return {"result": "success"}


@router.post("/assign")
def add_assign(data: NewAssign, db: Session = Depends(get_db)):
    assign = db.query(Assign).filter_by(ext=data.ext).filter_by(md5=data.md5).first()

    new_assign = Assign(ext=data.ext, md5=data.md5)
    db.add(new_assign)
    db.commit()
    db.refresh(new_assign)

    if assign:
        return {"result": "exists", "aid": new_assign.aid}
    else:
        upload_url, key = get_presigned_post_url(data.ext, data.md5)
        return {
            "result": "success",
            "aid": new_assign.aid,
            "url": upload_url,
            "key": key,
        }
