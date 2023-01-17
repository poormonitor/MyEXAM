from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models import get_db
from models.exam import Exam
from models.examgroup import ExamGroup
from models.paper import Paper
from models.union import Union

router = APIRouter()


class SearchInfo(BaseModel):
    course: Optional[int] = None
    grade: Optional[int] = None


class Unions(BaseModel):
    nid: str
    name: str
    views: int


class ExamGroups(BaseModel):
    egid: str
    name: str
    date: date
    views: int


class Exams(BaseModel):
    union: Unions
    examgroup: ExamGroups
    eid: str
    course: int
    grade: int
    views: int
    date: date


@router.post("/exams")
def search(data: Optional[SearchInfo] = None, db: Session = Depends(get_db)):
    query = (
        db.query(Exam, Union, ExamGroup, Paper)
        .outerjoin(ExamGroup, ExamGroup.egid == Exam.egid)
        .outerjoin(Union, Union.nid == ExamGroup.nid)
        .outerjoin(Paper, Paper.eid == Exam.eid)
        .group_by(Exam.eid)
        .order_by(Exam.views.desc())
        .filter(Paper.receipt == True)
    )

    if data.course is not None:
        query = query.filter(Exam.course == data.course)
    if data.grade is not None:
        query = query.filter(Exam.grade == data.grade)

    result = query.limit(20).all()

    lst = [
        Exams(
            **vars(item[0]),
            union=Unions(**vars(item[1])),
            examgroup=ExamGroups(**vars(item[2])),
        )
        for item in result
    ]

    return {"list": lst}
