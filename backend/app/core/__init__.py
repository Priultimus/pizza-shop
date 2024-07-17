from .creator import Create
from .deletor import Delete
from .finder import Find
from .updater import Update

create = Create()
delete = Delete()
find = Find()
update = Update()

__all__ = (
    "create",
    "delete",
    "find",
    "update",
)
