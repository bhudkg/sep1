from pydantic import BaseModel
from typing import Annotated
from pydantic import Field
from datetime import datetime
from typing import Dict
from database import create_tables, SessionLocal
from sqlalchemy.orm import Session
from models import PollTable, OptionTable

from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
import uuid




#app

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(
    title="Simple Poll/Voting API",
    description="An API for creating polls and voting on different options",
    version="1.0.0",
    lifespan=lifespan
)

#sqlite database

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



# models 
class Option(BaseModel):
    id: str
    option: str
    vote_count: int = 0

class CreatePollOption(BaseModel):
    text: str

class Poll(BaseModel):
    id: str
    title: str
    description: str
    option: list[Option]
    created_at: datetime
    total_votes: int = 0

class CreatePoll(BaseModel):
    title: str
    description: str
    options: list[CreatePollOption]

class PollSummary(BaseModel):
    id: str
    title: str
    description: str 
    # total_votes: int
    created_at: datetime

class VoteRequest(BaseModel):
    option_id : str 


#database - using a dict for memory of database. It can be changed for production database.
db_dependencies : Dict[str, Poll] = {}


#utility funtions

def generate_id():
    return str(uuid.uuid4())

#endpoints for the app

@app.post('/polls', response_model=Poll, tags=['Polls'])
async def create_poll(poll_data: CreatePoll, db: db_dependency):
    if len(poll_data.options) < 2:
        raise HTTPException(
            status_code=400,
            detail="Options length should be greater than 2"
        )
    
    # Create the poll first
    poll = PollTable(
        id=generate_id(),
        title=poll_data.title,
        description=poll_data.description
    )
    db.add(poll)
    db.flush()  # Get the poll ID
    
    # Create options with the poll_id
    options = []
    for option_data in poll_data.options:
        option = OptionTable(
            id=generate_id(),
            option=option_data.text,
            vote_count=0,
            poll_id=poll.id  # Set the poll_id
        )
        options.append(option)
        db.add(option)
    
    db.commit()
    db.refresh(poll)
    
    # Convert to response model
    response_options = []
    for opt in options:
        response_options.append(Option(
            id=opt.id,
            option=opt.option,
            vote_count=opt.vote_count
        ))
    
    return Poll(
        id=poll.id,
        title=poll.title,
        description=poll.description,
        option=response_options,
        total_votes=0,
        created_at=poll.created_at
    )



#to get the list of all the items in the db
@app.get('/polls', response_model=list[PollSummary], tags=['Polls'])
async def get_all_polls(db: db_dependency):
    polls = db.query(PollTable).all()
    if not polls:
        raise HTTPException(status_code=404, detail="No polls are found in DB.")

    summary = []
    for poll in polls:
        poll_summary = PollSummary(
            id=poll.id,
            title=poll.title,
            description=poll.description,
            created_at=poll.created_at
        )
        summary.append(poll_summary)

    # Return sorted by created_at descending
    return sorted(summary, key=lambda x: x.created_at, reverse=True)
  

@app.get('/polls/{poll_id}', response_model=Poll, tags=['Polls']) 
async def get_one_poll(poll_id: str, db: db_dependency):
    poll = db.query(PollTable).filter(PollTable.id == poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail=f"Poll with id {poll_id} not found")
    
    # Convert poll options to response model
    response_options = []
    for opt in poll.options:
        response_options.append(Option(
            id=opt.id,
            option=opt.option,
            vote_count=opt.vote_count
        ))
    
    total_votes = sum(opt.vote_count for opt in poll.options)
    
    return Poll(
        id=poll.id,
        title=poll.title,
        description=poll.description,
        option=response_options,
        total_votes=total_votes,
        created_at=poll.created_at
    )
    
    



def find_option(poll:PollTable, option_id: str):
    for option in poll.options:
        print(option.id)
        if option.id == option_id:
            return option
        
    raise HTTPException(status_code=404, detail="Option not found.")


@app.post('/polls/{poll_id}/vote', tags=['Voting'])
async def caste_vote(poll_id: str, vote: VoteRequest, db: db_dependency):
    poll = db.query(PollTable).filter(PollTable.id == poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    

    option = find_option(poll, vote.option_id)
    option.vote_count += 1
    # poll.total_votes += 1
    db.add(option)
    db.commit()
    db.refresh(option)


    return {
        "message": f"Vote cast successfully for '{option.option}'",
        "poll_id": poll_id,
        "option_id": vote.option_id,
        "option_text": option.option,
        "new_vote_count": option.vote_count,
        # "total_poll_votes": poll.total_votes
    }


@app.get('/polls/{poll_id}/results', tags=['Results'])
async def poll_results(poll_id: str, db: db_dependency):
    poll = db.query(PollTable).filter(PollTable.id == poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found.")

    results = []
    for option in poll.option:
        option_percentage = (option.vote_count / poll.total_votes)*100 if poll.total_votes > 0 else 0
        results.append({
            "id": option.id,
            "text": option.option,
            "votes": option.vote_ccount,
            "% Votes": option_percentage
            

        })

    return {
        "id": poll_id,
        "title": poll.title,
        "description": poll.description,
        "results": results,
        "created_at": poll.created_at
    }

@app.get("/polls/{poll_id}/delete", tags=['Polls'])
async def delete_poll(poll_id: str):
    if poll_id not in db_dependencies:
        raise HTTPException(status_code=404, detail="Poll not found with this id.")
    
    poll = db_dependencies[poll_id]

    deleted_poll = db_dependencies.pop(poll)

    return {"message": f"Poll '{deleted_poll.title}' deleted successfully"}



    








