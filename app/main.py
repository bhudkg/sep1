from pydantic import BaseModel
from typing import Annotated
from pydantic import Field
from datetime import datetime
from typing import Dict

from fastapi import FastAPI, HTTPException
import uuid




#app

app = FastAPI(
    title="Simple Poll/Voting API",
    description="An API for creating polls and voting on different options",
    version="1.0.0"
)


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
    total_votes: int
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
async def create_poll(poll_data: CreatePoll):
    if len(poll_data.options) < 2:
        raise HTTPException(
            status_code=400,
            detail="Options length should be grater than 2"
        )
    
    poll_id =  generate_id()
    options = []

    for option in poll_data.options:
        option = Option(
            id = generate_id(),
            option= option.text,
            vote_count=0
        )
        options.append(option)

    poll = Poll(
        id = poll_id,
        title=poll_data.title,
        description=poll_data.description,
        option=options,
        total_votes=0,
        created_at=datetime.now()
    )

    db_dependencies[poll_id] = poll

    return poll



#to get the list of all the items in the db
@app.get('/polls', response_model=PollSummary, tags=['Polls'])
async def get_all_polls():

    summary = []
    if len(db_dependencies) < 1:
        return {"msg": "Objects are not in db"}

    for poll_data in db_dependencies.values():
        poll_summary = PollSummary(
            id = poll_data.id,
            title=poll_data.title,
            description=poll_data.description,
            total_votes=poll_data.total_votes,
            created_at=poll_data.created_at
        )
        summary.append(poll_summary)

    return sorted(summary, key=lambda x: x.created_at, reverse=True)

@app.get('/polls/{poll_id}', response_model=Poll, tags=['Polls']) 
async def get_one_poll(poll_id: str):
    if poll_id not in db_dependencies:
        raise HTTPException(status_code=404, detail="Object not found in the db.")
    return db_dependencies[poll_id]



def find_option(poll: Poll, option_id: str):
    for option in poll.option:
        if option.id == option_id:
            return option
        
    raise HTTPException(status_code=404, detail="Option not found.")


@app.post('/polls/{poll_id}/vote', tags=['Voting'])
async def caste_vote(poll_id: str, vote: VoteRequest):
    if poll_id not in db_dependencies:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    poll = db_dependencies[poll_id]

    option = find_option(poll, vote.option_id)
    option.vote_count += 1
    poll.total_votes += 1


    return {
        "message": f"Vote cast successfully for '{option.option}'",
        "poll_id": poll_id,
        "option_id": vote.option_id,
        "option_text": option.option,
        "new_vote_count": option.vote_count,
        "total_poll_votes": poll.total_votes
    }


@app.get('/polls/{poll_id}/results', tags=['Results'])
async def poll_results(poll_id: str):
    if poll_id not in db_dependencies:
        raise HTTPException(status_code=404, detail="Poll couldn't found in the DB."
        )
    poll = db_dependencies[poll_id]

    results = []
    for option in poll.option:
        option_percentage = (option.vote_count / poll.total_votes)*100 if poll.total_votes > 0 else 0
        results.append({
            "id": option.id,
            "text": option.option,
            "votes": option.vote_count,
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



    








