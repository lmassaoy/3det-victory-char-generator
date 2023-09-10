from typing import List
from pydantic.dataclasses import dataclass
from uuid import uuid4
from pydantic import AliasPath, BaseModel, ConfigDict, Field


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

    def alter_xp(self, op=str, qty=int):
        if self.exp is None: self.exp = 0

        if op == '+':
            self.exp = self.exp + qty
        elif op == '-':
            self.exp = self.exp - qty
        else:
            print('operator should be `+` or `-`.')
        

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


# char1 = Character(name='Roger', attributes=[3,4,3])
# char1.calculate_additional_points()
# char1.include_expertise('fight')
# char1.include_expertise('sports')
# char1.include_advantage('special attack')
# char1.include_advantage('genius')
# char1.include_disadvantage('fragile')
# char1.include_disadvantage('code of honor: combat')
# char1.remove_advantage('genius')
# char1.remove_disadvantage('fragile')
# char1.alter_xp('+',10)

# print(char1)
# print(char1.model_dump(by_alias=True))
# print(char1.model_json_schema())