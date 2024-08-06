from .finder import Find

find = Find()
from .creator import Create

create = Create()
from .deletor import Delete

delete = Delete()
from .updater import Update

update = Update()

__all__ = (
    "create",
    "delete",
    "find",
    "update",
)
