from pydantic import BaseModel, ConfigDict


class BaseInput(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BaseOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

