from enum import Enum


class Status(str, Enum):
    published = "Published"
    draft = "Draft"
    archived = "Archived"
    deleted = "Deleted"
