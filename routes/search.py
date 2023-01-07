from datetime import date, datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from models import get_db
from models.union import Union
from models.examgroup import ExamGroup
from models.exam import Exam
from models.paper import Paper


router = APIRouter()


class searchInfo(BaseModel):
    name: Optional[str] = ""
    start: Optional[date] = datetime.now() - timedelta(days=30)
    end: Optional[date] = datetime.now()
    courses: Optional[List[int]] = []
    grade: Optional[int] = None
    page: Optional[int] = 0


class Unions(BaseModel):
    nid: str
    name: str
    views: int


class ExamGroups(BaseModel):
    egid: str
    name: str
    date: date
    views: int


class Papers(BaseModel):
    pid: str
    comment: str
    views: int
    created_at: datetime


class Exams(BaseModel):
    union: Unions
    examgroup: ExamGroups
    eid: str
    course: int
    grade: int
    views: int
    date: date
    papers: List[Papers]


@router.post("/query")
def search(info: searchInfo, db: Session = Depends(get_db)):
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
        Exams(
            **vars(item[0]),
            union=Unions(**vars(item[1])),
            examgroup=ExamGroups(**vars(item[2])),
            papers=[Papers(**vars(i)) for i in item[0].papers]
        )
        for item in result
    ]

    return {"list": lst, "count": cnt}
