from typing import Literal

from pydantic import BaseModel


class Split(BaseModel):
    type: Literal["split"]
