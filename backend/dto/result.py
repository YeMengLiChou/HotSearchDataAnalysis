import dataclasses

from typing_extensions import Union


@dataclasses.dataclass
class ApiResult:
    data: Union[dict, str, None]
    code: int
    msg: str
