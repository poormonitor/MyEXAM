from datetime import date, datetime
from typing import Dict, List, Optional, Tuple

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from misc.auth import is_admin
from misc.model import get_courses
from misc.s3 import get_presigned_get_url
from models import get_db
from models.assign import Assign
from models.exam import Exam
from models.examgroup import ExamGroup
from models.file import File
from models.paper import Paper
from models.union import Union

router = APIRouter()


class OneUnion(BaseModel):
    nid: str
    name: str
    views: int
    member: str


class OneExamGroup(BaseModel):
    egid: str
    name: str
    date: date
    views: int
    courses: Dict[int, List[Tuple[int, str]]]


class Unions(BaseModel):
    nid: str
    name: str
    views: int
    member: str
    examgroups: List[OneExamGroup]


class OneExam(BaseModel):
    eid: str
    grade: int
    course: int
    date: date
    views: int


class OneAssign(BaseModel):
    aid: str
    comment: str
    views: int
    upload_time: datetime


class ExamGroups(BaseModel):
    egid: str
    name: str
    date: date
    views: int
    union: OneUnion
    exams: List[OneExam]
    assigns: List[OneAssign]


class OnePaper(BaseModel):
    pid: str
    comment: str
    views: int
    fcnt: int
    created_at: datetime


class OneFile(BaseModel):
    fid: str
    name: str
    ext: str
    type: int
    views: int
    upload_time: datetime


class QueryPapers(BaseModel):
    pids: List[str]


class Papers(BaseModel):
    union: OneUnion
    examgroup: OneExamGroup
    exam: OneExam
    pid: str
    comment: str
    views: int
    files: List[OneFile]
    created_at: datetime


class Exams(BaseModel):
    grade: int
    course: int
    date: date
    views: int
    examgroup: OneExamGroup
    union: OneUnion
    papers: List[OnePaper]


@router.get("/unions")
def get_unions(db: Session = Depends(get_db)):
    unions = db.query(Union).all()
    return {"list": [OneUnion(**vars(i)) for i in unions]}


@router.get("/union")
def get_union(nid: str, db: Session = Depends(get_db)):
    union = db.query(Union).filter_by(nid=nid).first()

    if not union:
        raise HTTPException(status_code=404, detail="项目未找到。")

    examgroups = [
        OneExamGroup(
            **vars(i),
            courses=get_courses(i.exams),
        )
        for i in union.examgroups
    ]

    result = vars(union)
    del result["examgroups"]

    result = Unions(**result, examgroups=examgroups)

    union.views += 1
    db.commit()

    return {"union": result}


@router.get("/examgroup")
def get_union(egid: str, db: Session = Depends(get_db)):
    eg = db.query(ExamGroup).filter_by(egid=egid).first()

    if not eg:
        raise HTTPException(status_code=404, detail="项目未找到。")

    un = db.query(Union).filter_by(nid=eg.nid).first()
    union = OneUnion(**vars(un))
    exams = [OneExam(**vars(i)) for i in eg.exams]
    assigns = [OneAssign(**vars(i)) for i in eg.assigns]
    

    result = vars(eg)
    del result["exams"]
    del result["assigns"]

    result = ExamGroups(
        **result,
        union=union,
        exams=exams,
        assigns=assigns
    )

    eg.views += 1
    db.commit()

    return {"examgroup": result}


@router.get("/exam")
def get_exam(eid: str, admin: bool = Depends(is_admin), db: Session = Depends(get_db)):
    query = (
        db.query(Exam, Union, ExamGroup)
        .outerjoin(Paper, Exam.eid == Paper.eid)
        .outerjoin(ExamGroup, ExamGroup.egid == Exam.egid)
        .outerjoin(Union, Union.nid == ExamGroup.nid)
        .filter(Exam.eid == eid)
        .filter(Paper.status >= (1 if admin else 2))
        .group_by(Exam.eid)
    )
    result = query.first()

    if not result:
        raise HTTPException(status_code=404, detail="项目未找到。")

    exam = result[0]
    union = OneUnion(**vars(result[1]))
    examgroup = OneExamGroup(**vars(result[2]), courses=get_courses(result[2].exams))
    papers = [OnePaper(**vars(i), fcnt=len(i.files)) for i in exam.papers]

    data = vars(exam)
    del data["papers"]

    examdata = Exams(**data, union=union, examgroup=examgroup, papers=papers)

    exam.views += 1
    db.commit()

    return {"exam": examdata}


@router.post("/papers")
def get_file_list(data: QueryPapers, db: Session = Depends(get_db)):
    query = (
        db.query(Paper, Union, ExamGroup, Exam)
        .outerjoin(Exam, Exam.eid == Paper.eid)
        .outerjoin(ExamGroup, ExamGroup.egid == Exam.egid)
        .outerjoin(Union, Union.nid == ExamGroup.nid)
        .filter(Paper.pid.in_(data.pids))
        .group_by(Exam.eid)
    )
    result = query.limit(5).all()

    if not result:
        raise HTTPException(status_code=404, detail="项目未找到。")

    papers = [
        Papers(
            **vars(i[0]),
            union=OneUnion(**vars(i[1])),
            examgroup=OneExamGroup(**vars(i[2]), courses=get_courses(i[2].exams)),
            exam=OneExam(**vars(i[3])),
            files=[OneFile(**vars(j)) for j in i[0].files],
        )
        for i in result
    ]

    return {"list": papers}


@router.get("/paper")
def get_paper(pid: str, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.pid == pid).first()

    if not paper:
        raise HTTPException(status_code=404, detail="项目未找到。")

    data = OnePaper(**vars(paper), fcnt=len(paper.files))

    paper.views += 1
    db.commit()

    return {"paper": data}


@router.get("/files")
def get_files(pid: str, db: Session = Depends(get_db)):
    files = db.query(File).filter_by(pid=pid).all()
    lst = [OneFile(**vars(i)) for i in files]

    return {"list": lst}


@router.get("/file")
def get_url(fid: str, db: Session = Depends(get_db)):
    file = db.query(File).filter(File.fid == fid).first()

    if not file:
        raise HTTPException(status_code=404, detail="项目未找到。")

    data = OneFile(**vars(file))

    file.views += 1
    db.commit()

    return {"file": data}


@router.get("/url")
def get_url(fid: str, download: Optional[bool] = True, db: Session = Depends(get_db)):
    file = db.query(File).filter(File.fid == fid).first()

    if not file:
        raise HTTPException(status_code=404, detail="项目未找到。")

    url = get_presigned_get_url(file.ext, file.md5, file.name, download)

    file.views += 1
    db.commit()

    return {"url": url}


@router.get("/assigns")
def get_assign_url(egid: str, db: Session = Depends(get_db)):
    assigns = db.query(Assign).filter_by(egid=egid).all()

    return {"list": [OneAssign(**vars(i)) for i in assigns]}


@router.get("/assign")
def get_assign_url(aid: str, db: Session = Depends(get_db)):
    assign = db.query(Assign).filter_by(aid=aid).first()

    if not assign:
        raise HTTPException(status_code=404, detail="项目未找到。")

    return {"assign": OneAssign(**vars(assign))}


@router.get("/assign_url")
def get_assign_url(aid: str, db: Session = Depends(get_db)):
    assign = db.query(Assign).filter_by(aid=aid).first()
    if not assign:
        raise HTTPException(status_code=404, detail="项目未找到。")

    url = get_presigned_get_url(assign.ext, assign.md5)

    return {"url": url}
