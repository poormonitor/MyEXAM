import os
import subprocess
import sys
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models import get_db
from models.assign import Assign
from models.exam import Exam
from models.examgroup import ExamGroup
from models.file import File
from models.paper import Paper
from models.task import Task
from models.union import Union

router = APIRouter()


class ReOCRFile(BaseModel):
    fid: str


@router.post("/ocr/file")
def perform_ocr_file(data: ReOCRFile, db: Session = Depends(get_db)):
    file = db.query(File).filter_by(fid=data.fid).first()

    if not file:
        raise HTTPException(status_code=404, detail="项目未找到。")

    processing = db.query(Task).count()

    task = Task(type="ocr", data=file.fid)
    db.add(task)

    db.commit()

    if not processing:
        current = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current, "..", "misc", "ocr.py")
        subprocess.Popen([sys.executable, path])

    return {"result": "success"}


class ReOCRPaper(BaseModel):
    pid: str


@router.post("/ocr/paper")
def perform_ocr_paper(data: ReOCRPaper, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter_by(pid=data.pid).first()

    if not paper:
        raise HTTPException(status_code=404, detail="项目未找到。")

    processing = db.query(Task).count()

    for i in paper.files:
        task = Task(type="ocr", data=i.fid)
        db.add(task)

    db.commit()

    if not processing:
        current = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current, "..", "misc", "ocr.py")
        subprocess.Popen([sys.executable, path])

    return {"result": "success"}


class EditUnion(BaseModel):
    nid: str
    name: str
    member: str


@router.post("/edit/union")
def edit_union(data: EditUnion, db: Session = Depends(get_db)):
    union = db.query(Union).filter_by(nid=data.nid).first()

    if not union:
        raise HTTPException(status_code=404, detail="项目未找到。")

    union.name = data.name
    union.member = data.member

    db.commit()
    return {"result": "success"}


class EditExamGroup(BaseModel):
    egid: str
    date: datetime
    name: str


@router.post("/edit/examgroup")
def edit_examgroup(data: EditExamGroup, db: Session = Depends(get_db)):
    examgroup = db.query(ExamGroup).filter_by(egid=data.egid).first()

    if not examgroup:
        raise HTTPException(status_code=404, detail="项目未找到。")

    examgroup.date = data.date
    examgroup.name = data.name

    db.commit()
    return {"result": "success"}


class EditExam(BaseModel):
    eid: str
    date: datetime
    course: int
    grade: int


@router.post("/edit/exam")
def edit_exam(data: EditExam, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter_by(eid=data.eid).first()

    if not exam:
        raise HTTPException(status_code=404, detail="项目未找到。")

    exam.date = data.date
    exam.course = data.course
    exam.grade = data.grade

    db.commit()
    return {"result": "success"}


class EditPaper(BaseModel):
    pid: str
    comment: str


@router.post("/edit/paper")
def edit_paper(data: EditPaper, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter_by(pid=data.pid).first()

    if not paper:
        raise HTTPException(status_code=404, detail="项目未找到。")

    paper.comment = data.comment

    db.commit()
    return {"result": "success"}


class EditFile(BaseModel):
    fid: str
    name: str
    type: str


@router.post("/edit/file")
def edit_file(data: EditFile, db: Session = Depends(get_db)):
    file = db.query(File).filter_by(fid=data.fid).first()

    if not file:
        raise HTTPException(status_code=404, detail="项目未找到。")

    file.name = data.name
    file.type = data.type

    db.commit()
    return {"result": "success"}


class EditAssign(BaseModel):
    aid: str
    egid: str
    comment: str


@router.post("/edit/assign")
def edit_file(data: EditAssign, db: Session = Depends(get_db)):
    assign = db.query(Assign).filter_by(aid=data.aid).first()

    if not assign:
        raise HTTPException(status_code=404, detail="项目未找到。")

    assign.comment = data.comment
    assign.egid = data.egid

    db.commit()
    return {"result": "success"}


class DeleteUnion(BaseModel):
    nid: str


@router.post("/delete/union")
def delete_union(data: DeleteUnion, db: Session = Depends(get_db)):
    union = db.query(Union).filter_by(nid=data.nid).first()

    if not union:
        raise HTTPException(status_code=404, detail="项目未找到。")

    if len(union.examgroups):
        raise HTTPException(status_code=400, detail="联盟非空。")

    db.delete(union)
    db.commit()
    return {"result": "success"}


class DeleteExamGroup(BaseModel):
    egid: str


@router.post("/delete/examgroup")
def delete_examgroup(data: DeleteExamGroup, db: Session = Depends(get_db)):
    examgroup = db.query(ExamGroup).filter_by(egid=data.egid).first()

    if not examgroup:
        raise HTTPException(status_code=404, detail="项目未找到。")

    if len(examgroup.exams):
        raise HTTPException(status_code=400, detail="考试非空。")

    db.delete(examgroup)
    db.commit()
    return {"result": "success"}


class DeleteExam(BaseModel):
    eid: str


@router.post("/delete/exam")
def delete_exam(data: DeleteExam, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter_by(eid=data.eid).first()

    if not exam:
        raise HTTPException(status_code=404, detail="项目未找到。")

    if len(exam.papers):
        raise HTTPException(status_code=400, detail="考试非空。")

    db.delete(exam)
    db.commit()
    return {"result": "success"}


class DeletePaper(BaseModel):
    pid: str


@router.post("/delete/paper")
def delete_paper(data: DeletePaper, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter_by(pid=data.pid).first()

    if not paper:
        raise HTTPException(status_code=404, detail="项目未找到。")

    db.query(File).filter_by(pid=paper.pid).delete()
    db.delete(paper)
    db.commit()
    return {"result": "success"}


class DeleteFile(BaseModel):
    fid: str


@router.post("/delete/file")
def delete_file(data: DeleteFile, db: Session = Depends(get_db)):
    file = db.query(File).filter_by(fid=data.fid).first()

    if not file:
        raise HTTPException(status_code=404, detail="项目未找到。")

    db.delete(file)
    db.commit()

    return {"result": "success"}


class DeleteAssign(BaseModel):
    aid: str


@router.post("/delete/assign")
def delete_assign(data: DeleteAssign, db: Session = Depends(get_db)):
    assign = db.query(Assign).filter_by(aid=data.aid).first()

    if not assign:
        raise HTTPException(status_code=404, detail="项目未找到。")

    db.delete(assign)
    db.commit()

    return {"result": "success"}
