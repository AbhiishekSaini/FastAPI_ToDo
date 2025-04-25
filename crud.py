from turtle import title
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import ToDo
from typing import List, Optional

from fastapi import Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


router = APIRouter()
templates=Jinja2Templates(directory='templates')

class ToDoCreate(BaseModel):

    title: str
    description : Optional[str] = None
    done : bool

class ToDoResponse(ToDoCreate):    
     id : int

@router.get('/',response_model=List[ToDoResponse])
def show_Todos (request:Request,db: Session = Depends(get_db)):
    todos= db.query(ToDo).all()
    return templates.TemplateResponse('todo_list.html',{"request": request, "todos":todos})

@router.get('/create')
def create_todo(request:Request):
    return templates.TemplateResponse('create_todo.html',{'request':request})






@router.post('/create')
def create_todo(
    title : str = Form(...),
    description : str = Form(...),
    done : bool = Form(False),
    db: Session = Depends(get_db)):
    new_todo = ToDo(title=title,description =description,done=done)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return RedirectResponse(url='/todo/' , status_code=303)
    # todos.append(todo)
    # return { "message" : "TODO create Sucessfully"}

@router.get('/edit/{todo_id}')
def update_todo(todo_id:int, request: Request,  db: Session=Depends(get_db)):
    todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if not todo: 
        return HTTPException(status_code=404, detail="ToDo not found")
    return templates.TemplateResponse('todo_edit.html', {'request': request , 'todo': todo})
 
@router.post('/update/{todo_id}', response_model=ToDoResponse)
def update_todo(
    todo_id: int,
    title: str = Form(...),
    description: str = Form(...),
    done: bool = Form(False),
    db: Session = Depends(get_db)
):
    db_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    
    if not db_todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    
    db_todo.title = title
    db_todo.description = description
    db_todo.done = done

    db.commit()
    db.refresh(db_todo)

    return RedirectResponse(url='/todo/' , status_code=303)

@router.get('/delete/{todo_id}')
def delete_todo(todo_id:int ,db: Session = Depends(get_db)):
    db_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if not db_todo:
        return HTTPException(status_code=404,detail="ToDo not found")
    db.delete(db_todo)
    db.commit()
    return RedirectResponse(url='/todo/' , status_code=303)
     