from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from misc.auth import admin_required
from models import get_db
from models.exam import Exam
from models.examgroup import ExamGroup
from models.file import File
from models.paper import Paper
from models.union import Union
from misc.s3 import delete_object_from_s3, delete_objects_from_s3

router = APIRouter()


@router.post("/ocr/file", dependencies=[Depends(admin_required)])
def perform_ocr(
    fid: str,
    background: BackgroundTasks,
    db: Session = Depends(get_db),
):
    from misc.ocr import WriteOCR

    file = db.query(File).filter_by(fid=fid).first()
    background.add_task(WriteOCR, file.ext, file.fid, db)

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


@router.post("/delete/union")
def delete_union(nid: str, db: Session = Depends(get_db)):
    union = db.query(Union).filter_by(nid=nid).first()

    if not union:
        raise HTTPException(status_code=404, detail="项目未找到。")

    if len(union.examgroups):
        raise HTTPException(status_code=400, detail="联盟非空。")

    db.delete(union)
    db.commit()
    return {"result": "success"}


@router.post("/delete/examgroup")
def delete_examgroup(egid: str, db: Session = Depends(get_db)):
    examgroup = db.query(ExamGroup).filter_by(egid=egid).first()

    if not examgroup:
        raise HTTPException(status_code=404, detail="项目未找到。")

    if len(examgroup.exams):
        raise HTTPException(status_code=400, detail="考试非空。")

    db.delete(examgroup)
    db.commit()
    return {"result": "success"}


@router.post("/delete/exam")
def delete_exam(eid: str, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter_by(eid=eid).first()

    if not exam:
        raise HTTPException(status_code=404, detail="项目未找到。")

    if len(exam.papers):
        raise HTTPException(status_code=400, detail="考试非空。")

    db.delete(exam)
    db.commit()
    return {"result": "success"}


@router.post("/delete/paper")
def delete_paper(pid: str, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter_by(pid=pid).first()

    if not paper:
        raise HTTPException(status_code=404, detail="项目未找到。")

    delete_objects_from_s3([(i.fid, i.ext) for i in paper.files])
    db.query(File).filter_by(pid=pid).delete()
    db.delete(paper)
    db.commit()
    return {"result": "success"}


@router.post("/delete/file")
def delete_file(fid: str, db: Session = Depends(get_db)):
    file = db.query(File).filter_by(fid=fid).first()

    if not file:
        raise HTTPException(status_code=404, detail="项目未找到。")

    delete_object_from_s3(file.ext, file.fid)
    db.delete(file)
    db.commit()
    return {"result": "success"}
