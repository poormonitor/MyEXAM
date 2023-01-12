from datetime import date, datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from models import get_db
from models.exam import Exam
from models.examgroup import ExamGroup
from models.file import File
from models.paper import Paper
from models.union import Union

router = APIRouter()


class searchFile(BaseModel):
    s: Optional[str] = ""
    start: Optional[date] = datetime.now() - timedelta(days=30)
    end: Optional[date] = datetime.now()
    courses: Optional[List[int]] = []
    grade: Optional[int] = None
    page: Optional[int] = 0


class searchExam(BaseModel):
    name: Optional[str] = ""
    start: Optional[date] = datetime.now() - timedelta(days=30)
    end: Optional[date] = datetime.now()
    courses: Optional[List[int]] = []
    grade: Optional[int] = None
    page: Optional[int] = 0


class OneUnion(BaseModel):
    nid: str
    name: str
    views: int


class OneExamGroup(BaseModel):
    egid: str
    name: str
    date: date
    views: int


class OnePaper(BaseModel):
    pid: str
    comment: str
    views: int
    created_at: datetime


class OneExam(BaseModel):
    union: OneUnion
    examgroup: OneExamGroup
    eid: str
    course: int
    grade: int
    views: int
    date: date
    papers: List[OnePaper]


class OneFile(BaseModel):
    fid: str
    name: str
    ext: str
    type: int
    views: int
    upload_time: datetime
    union: OneUnion
    examgroup: OneExamGroup
    exam: OneExam
    paper: OnePaper


@router.post("/exam")
def search(info: searchExam, db: Session = Depends(get_db)):
    k = info.name.split(" ")
    query = (
        db.query(Exam, Union, ExamGroup, Paper)
        .outerjoin(ExamGroup, ExamGroup.egid == Exam.egid)
        .outerjoin(Union, Union.nid == ExamGroup.nid)
        .outerjoin(Paper, Paper.eid == Exam.eid)
        .group_by(Exam.eid)
        .filter(
            and_(
                or_(
                    Union.name.contains(i),
                    ExamGroup.name.contains(i),
                    Paper.comment.contains(i),
                )
                for i in k
            )
        )
        .filter(Exam.date >= info.start)
        .filter(Exam.date <= info.end)
        .filter(Paper.receipt == True)
    )

    if info.courses:
        query = query.filter(Exam.course.in_(info.courses))
    if info.grade:
        query = query.filter(Exam.grade == info.grade)

    cnt = query.count()
    result = query.limit(50).offset(info.page * 50).all()

    lst = [
        OneExam(
            **vars(item[0]),
            union=OneUnion(**vars(item[1])),
            examgroup=OneExamGroup(**vars(item[2])),
            papers=[OnePaper(**vars(i)) for i in item[0].papers],
        )
        for item in result
    ]

    return {"list": lst, "count": cnt}


@router.post("/file")
def search(info: searchFile, db: Session = Depends(get_db)):
    k = info.s.split(" ")
    query = (
        db.query(File, Union, ExamGroup, Exam, Paper)
        .outerjoin(Paper, Paper.pid == File.pid)
        .outerjoin(Exam, Paper.eid == Exam.eid)
        .outerjoin(ExamGroup, ExamGroup.egid == Exam.egid)
        .outerjoin(Union, Union.nid == ExamGroup.nid)
        .filter(and_(File.ocr.contains(i) for i in k))
        .filter(Exam.date >= info.start)
        .filter(Exam.date <= info.end)
        .filter(Paper.receipt == True)
    )

    if info.courses:
        query = query.filter(Exam.course.in_(info.courses))
    if info.grade:
        query = query.filter(Exam.grade == info.grade)

    cnt = query.count()
    result = query.limit(50).offset(info.page * 50).all()

    lst = [
        OneFile(
            **vars(item[0]),
            union=OneUnion(**vars(item[4])),
            examgroup=OneExamGroup(**vars(item[3])),
            exam=OneExam(**vars(item[2])),
            paper=OnePaper(**vars(item[1])),
        )
        for item in result
    ]

    return {"list": lst, "count": cnt}
