import json
from typing import Annotated, List

# from fastapi.encoders import jsonable_encoder
from ..models.base_entities import Character
from fastapi import APIRouter, HTTPException, Header


router = APIRouter()


char1 = Character(name='Roger', power=3, hability=3, resistance=2)
char1.calculate_additional_points()
char1.include_expertise('fight')
char1.include_expertise('sports')
char1.include_advantage('special attack')
char1.include_advantage('genius')
char1.include_disadvantage('fragile')
char1.include_disadvantage('code of honor: combat')
char1.remove_advantage('genius')
char1.remove_disadvantage('fragile')
char1.alter_xp('+',10)


characters_list = []
characters_list.append(char1)


@router.put("/characters/{character_id}:increaseEXP",
            tags=["characters (custom ops)"],
            status_code=200,
            summary="Custom Op: Increase Character Experience")
def increase_character_exp(character_id: str, experience_points: Annotated[int | None, Header(convert_underscores=False)] = None):
    if experience_points is None:
        raise HTTPException(status_code=400, detail="Missing experience_points header.")
    
    for i in range(len(characters_list)):
        if characters_list[i].id == character_id:
            previous_exp = characters_list[i].exp
            characters_list[i].alter_xp('+', experience_points)
            return {'previousExperience': previous_exp, 'currentExperience': characters_list[i].exp}
    raise HTTPException(status_code=404)


@router.put("/characters/{character_id}:decreaseEXP",
            tags=["characters (custom ops)"],
            status_code=200,
            summary="Custom Op: Decrease Character Experience")
def decrease_character_exp(character_id: str, experience_points: Annotated[int | None, Header(convert_underscores=False)] = None):
    if experience_points is None:
        raise HTTPException(status_code=400, detail="Missing experience_points header.")
    
    for i in range(len(characters_list)):
        if characters_list[i].id == character_id:
            previous_exp = characters_list[i].exp

            if previous_exp - experience_points < 0:
                raise HTTPException(
                    status_code=400,
                    detail=f'cannot decrease experience lower than 0. Current experience: {previous_exp}'
                ) 

            characters_list[i].alter_xp('-', experience_points)
            return {'previousExperience': previous_exp, 'currentExperience': characters_list[i].exp}
    raise HTTPException(status_code=404)


@router.get("/characters", tags=["characters"], response_model=List[Character])
def list_characters() -> list:
    return characters_list


@router.get("/characters/{character_id}", tags=["characters"], response_model=Character)
def find_character(character_id: str) -> Character:
    for i in range(len(characters_list)):
        if characters_list[i].id == character_id:
            return characters_list[i]
    raise HTTPException(status_code=404)


@router.post("/characters", tags=["characters"], response_model=Character, status_code=201)
def create_character(character_body: Character) -> Character:
    character_body.calculate_additional_points()
    characters_list.append(character_body)
    return character_body


@router.put("/characters/{character_id}", tags=["characters"], response_model=Character, status_code=200)
def update_character(character_id: str, character_body: Character) -> Character:
    for i in range(len(characters_list)):
        if characters_list[i].id == character_id:
            character_body.calculate_additional_points()
            character_body.id = character_id
            characters_list[i] = character_body
            return character_body
    raise HTTPException(status_code=404) 


@router.patch("/characters/{character_id}", tags=["characters"], response_model=Character, status_code=200)
def partial_update_character(character_id: str, character_body: Character) -> Character:
    for i in range(len(characters_list)):
        if characters_list[i].id == character_id:
            stored_character_data = characters_list[i].model_dump(by_alias=True)
            stored_character_model = Character(**stored_character_data)
            updated_character = stored_character_model.model_copy(update=character_body.model_dump(exclude_unset=True))
            updated_character.calculate_additional_points()
            characters_list[i] = updated_character
            # characters_list[i] = jsonable_encoder(updated_character) # implements w/ a proper database
            return updated_character
    raise HTTPException(status_code=404) 
    

@router.delete("/characters/{character_id}", tags=["characters"], status_code=204)
def delete_character(character_id: str):
    for i in range(len(characters_list)):
        if characters_list[i].id == character_id:
            characters_list.pop(i)
            return None
    raise HTTPException(status_code=404)


# @router.get("/characters:dumpToStorage", tags=["characters"])
# def save_characters_into_storage(status_code=200):
#     with open(characters_in_storage, 'w') as outfile:
#         json.dump(characters_list, outfile)