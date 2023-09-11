from typing import List, Optional
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, Field


class BaseUnit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(description='Name of the unit', min_length=3, max_length=50)
    concept: str = Field(description='Concept of the unit', default='')
    po: int = Field(description='Power', default=None, alias='power')
    ha: int = Field(description='Hability', default=None, alias='hability')
    res: int = Field(description='Resistance', default=None, alias='resistance')
    ap: int = Field(description='Action Points', default=0, alias='actionPoints')
    mp: int = Field(description='Mana Points', default=0, alias='manaPoints')
    hp: int = Field(description='Health Points', default=0, alias='healthPoints')

    def calculate_additional_points(self):
        self.ap = self.po
        self.mp = self.ha*5
        self.hp = self.res*5


class Character(BaseUnit):
    id: str = Field(description='Identifier created by the system', default_factory=lambda: uuid4().hex)
    exp: int = Field(description='Experience points earned by the character', default=0, alias='experiencePoints')
    expertises: List[str] = Field(description='List of expertises the character has', default=[])
    advantages: List[str] = Field(description='List of advantages the character has', default=[])
    disadvantages: List[str] = Field(description='List of disadvantages the character has', default=[])      

    def include_expertise(self, expertise=str):
        self.expertises.append(expertise)

    def include_advantage(self, advantage=str):
        self.advantages.append(advantage)
    
    def include_disadvantage(self, disadvantage=str):
        self.disadvantages.append(disadvantage)
    
    def remove_advantage(self, advantage=str):
        self.advantages.remove(advantage)

    def remove_disadvantage(self, disadvantage=str):
        self.disadvantages.remove(disadvantage)

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.model_dump(by_alias=True, exclude_none=True)
        try:
            if data["_id"] is None:
                data.pop("_id")
        except KeyError:
            return data
        return data