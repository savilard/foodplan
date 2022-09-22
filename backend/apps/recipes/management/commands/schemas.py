from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    measurement_unit: str

    class Conf:
        anystr_strip_whitespace = True
        anystr_lower = True
