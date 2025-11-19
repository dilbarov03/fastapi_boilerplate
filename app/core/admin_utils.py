from enum import Enum
from typing import Any, Callable, List, Optional, Tuple

from sqladmin._types import MODEL_ATTR
from sqladmin.filters import get_column_obj, get_parameter_name, get_title
from sqlalchemy.sql.expression import Select
from starlette.requests import Request


class EnumFilter:
    def __init__(
            self,
            column: MODEL_ATTR,
            enum_class: type[Enum],
            title: Optional[str] = None,
            parameter_name: Optional[str] = None,
    ):
        self.column = column
        self.enum_class = enum_class
        self.title = title or get_title(column)
        self.parameter_name = parameter_name or get_parameter_name(column)

    async def lookups(
            self,
            request: Request,
            model: Any,
            run_query: Callable[[Select], Any],
    ) -> List[Tuple[str, str]]:
        return [("", "All")] + [
            (e.value, e.name.replace("_", " ").title()) for e in self.enum_class
        ]

    async def get_filtered_query(
            self,
            query: Select,
            value: Any,
            model: Any,
    ) -> Select:
        if value == "":
            return query

        column_obj = get_column_obj(self.column, model)
        return query.filter(column_obj == value)
