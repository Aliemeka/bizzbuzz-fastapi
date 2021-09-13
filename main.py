from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List


class Status(str, Enum):
    active = "Active"
    inactive = "Inactive"
    suspended = "Suspended"
    deleted = "Deleted"


class BaseItem(BaseModel):
    name: str
    description: str
    status: Optional[Status] = Status.active


class Item(BaseItem):
    id: int


app = FastAPI(title="Bizzbuzz API")

items: List[Item] = []


@app.get("/")
def hello():
    return {"message": "Hello!, Welcome to Bizzbuzz on fastAPI"}


@app.get("/items")
def get_items():
    return items


def createItem(item: BaseItem):
    someItem = dict(item)
    someItem["id"] = len(items) + 1
    newItem = Item(**someItem)
    items.append(newItem)
    return newItem


@app.post("/items")
def add_item(item: BaseItem):
    return createItem(item)


def add_items(items: List[BaseItem]):
    for item in items:
        yield createItem(item)


@app.post("/items/add_multiple")
def add_mulitple(itemList: List[BaseItem]):
    items = [item for item in add_items(itemList)]
    return items
