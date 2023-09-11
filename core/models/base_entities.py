from typing import List
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, Field


class BaseUnit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description='Identifier created by the system', default_factory=lambda: uuid4().hex)
    name: str = Field(description='Name of the unit', min_length=3, max_length=50)
    concept: str = Field(description='Concept of the unit', default='')
    power: int = Field(description='Power', default=None, alias='power')
    hability: int = Field(description='Hability', default=None, alias='hability')
    resistance: int = Field(description='Resistance', default=None, alias='resistance')
    action_points: int = Field(description='Action Points', default=0, alias='actionPoints')
    mana_points: int = Field(description='Mana Points', default=0, alias='manaPoints')
    health_points: int = Field(description='Health Points', default=0, alias='healthPoints')
    total_points: int = Field(description='Total Points', default=0, alias='totalPoints')
    expertises: List[str] = Field(description='List of expertises the unit has', default=[])
    advantages: List[str] = Field(description='List of advantages the unit has', default=[])
    disadvantages: List[str] = Field(description='List of disadvantages the unit has', default=[])
    image_url: str = Field(description='URL address of the image of the unit', alias='imageURL')

    def calculate_additional_points(self):
        self.action_points = self.power
        self.mana_points = self.hability*5
        self.health_points = self.resistance*5
        self.total_points = self.power + self.hability + self.resistance + len(self.expertises) + len(self.advantages) - len(self.disadvantages)
    
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


class Character(BaseUnit):
    exp: int = Field(description='Experience points earned by the character', default=0, alias='experiencePoints')
    money_amount: int = Field(description='Amount of money the character has', default=0, alias='moneyAmount')
    bag: List[str] = Field(description='List of items the character has', default=[], alias='bag')


class NPC(BaseUnit):
    money_to_drop: int = Field(description='Amount of money the NPC will drop', default=0, alias='moneyToDrop')
    items_to_drop: List[str] = Field(description='List of items the NPC will drop', default=[], alias='itemsToDrop')
    notes_for_the_master: List[str] = Field(description='List of notes related to the NPC for supporting the master', default=[], alias='notesForTheMaster')