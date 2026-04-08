from pydantic import BaseModel
from typing import Union, Dict, Any, Optional

class GenerateUIRequest(BaseModel):
    query: Union[str, Dict[str, Any]]