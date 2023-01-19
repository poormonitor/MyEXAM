import re
from datetime import date, datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from misc.auth import is_admin
from models import get_db
from models.exam import Exam
from models.examgroup import ExamGroup
from models.file import File
from models.paper import Paper
from models.union import Union

router = APIRouter()


class SearchFile(BaseModel):
    s: Optional[str] = ""
    start: Optional[date] = datetime.now() - timedelta(days=30)
    end: Optional[date] = datetime.now()
    courses: Optional[List[int]] = []
    grade: Optional[int] = None
    page: Optional[int] = 0


class SearchExam(BaseModel):
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
    status: int


class OneExam(BaseModel):
    eid: str
    course: int
    grade: int
    views: int
    date: date


class Exams(BaseModel):
    union: OneUnion
    examgroup: OneExamGroup
    eid: str
    course: int
    grade: int
    views: int
    date: date
    papers: List[OnePaper]


class Files(BaseModel):
    fid: str
    name: str
    ext: str
    type: int
    views: int
    upload_time: datetime
    text: str
    union: OneUnion
    examgroup: OneExamGroup
    exam: OneExam
    paper: OnePaper


def GetHighlight(text: str, keyword: str):
    f = []

    target = "|".join(keyword.split(" "))
    rs = re.findall(r"(.{0,8})(%s)(.{0,8})" % target, text)

    if not rs:
        return None

    for i in rs:
        f.append(i[0] + "*s*" + i[1] + "*e*" + i[2])

    return "\n".join(f[:5])


@router.post("/exam")
def search_exam(
    info: SearchExam, admin: bool = Depends(is_admin), db: Session = Depends(get_db)
):
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
        .filter(Paper.status >= (1 if admin else 2))
    )

    if info.courses:
        query = query.filter(Exam.course.in_(info.courses))
    if info.grade is not None:
        query = query.filter(Exam.grade == info.grade)

    cnt = query.count()
    result = query.limit(10).offset(info.page * 10).all()

    lst = [
        Exams(
            **vars(item[0]),
            union=OneUnion(**vars(item[1])),
            examgroup=OneExamGroup(**vars(item[2])),
            papers=[OnePaper(**vars(i)) for i in item[0].papers],
        )
        for item in result
    ]

    return {"list": lst, "count": cnt}


@router.post("/file")
def search_file(
    info: SearchFile, admin: bool = Depends(is_admin), db: Session = Depends(get_db)
):
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
        .filter(Paper.status >= (1 if admin else 2))
    )

    if info.courses:
        query = query.filter(Exam.course.in_(info.courses))
    if info.grade:
        query = query.filter(Exam.grade == info.grade)

    cnt = query.count()
    result = query.limit(10).offset(info.page * 10).all()

    lst = [
        Files(
            **vars(item[0]),
            union=OneUnion(**vars(item[1])),
            examgroup=OneExamGroup(**vars(item[2])),
            exam=OneExam(**vars(item[3])),
            paper=OnePaper(**vars(item[4])),
            text=GetHighlight(item[0].ocr, info.s),
        )
        for item in result
    ]

    return {"list": lst, "count": cnt}
