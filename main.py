import json
import typing

import uvicorn
import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL


@strawberry.type
class Action:
    id: int
    name: str
    time_to_complete: int


@strawberry.type
class Worker:
    id: int
    name: str
    last_name: str
    age: int
    salary: int
    working_hours: int
    experience: int
    work_place: str
    action: Action


@strawberry.type
class Query:
    @strawberry.field
    def workers(self) -> typing.List[Worker]:
        with open("./db.json", encoding="UTF-8") as workers_from_db:
            all_workers = json.load(workers_from_db)
            result = []
            for worker in all_workers:
                result.append(Worker(**worker))
                result[-1].action = Action(**worker.get("action"))
        return result


schema = strawberry.Schema(query=Query)


graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/", graphql_app)
app.add_websocket_route("/", graphql_app)

uvicorn.run(app)
