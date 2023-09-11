from typing import Annotated, List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Header
from pydantic import ValidationError
from ..models.base_entities import Character
from ..db import get_collection


characters_collection = get_collection('characters')
router = APIRouter()


@router.patch("/v1/characters/{character_id}:increaseExp",
            tags=["Characters (custom ops)"],
            summary="Custom Op: Increase a Character's Experience")
def increase_character_exp(character_id: str, experience_points: Annotated[int | None, Header(convert_underscores=False)] = None):
    if experience_points is None:
        raise HTTPException(status_code=400, detail="Missing experience_points header.")
    
    character_body = characters_collection.find_one({'_id': ObjectId(character_id)})
    if character_body is None:
        raise HTTPException(status_code=404, detail="Character not found.")
    else:
        previous_exp = character_body['experiencePoints']
        characters_collection.update_one({'_id': ObjectId(character_id)},  {'$set': {'experiencePoints': previous_exp+experience_points}})
        return {'previousExperience': previous_exp, 'currentExperience': previous_exp+experience_points}


@router.patch("/v1/characters/{character_id}:decreaseExp",
            tags=["Characters (custom ops)"],
            summary="Custom Op: Decrease a Character's Experience")
def decrease_character_exp(character_id: str, experience_points: Annotated[int | None, Header(convert_underscores=False)] = None):
    if experience_points is None:
        raise HTTPException(status_code=400, detail="Missing experience_points header.")
    
    character_body = characters_collection.find_one({'_id': ObjectId(character_id)})
    if character_body is None:
        raise HTTPException(status_code=404, detail="Character not found.")
    else:
        previous_exp = character_body['experiencePoints']
        current_exp = 0 if previous_exp-experience_points < 0 else previous_exp-experience_points
        characters_collection.update_one({'_id': ObjectId(character_id)},  {'$set': {'experiencePoints': current_exp}})
        return {'previousExperience': previous_exp, 'currentExperience': current_exp}


@router.post("/v1/characters",
            tags=["Characters"],
            response_model=Character,
            status_code=201,
            summary="Create a Character")
def create_character(character_body: Character) -> Character:
    character_body.calculate_additional_points()
    insert_result = characters_collection.insert_one(character_body.to_bson())
    characters_collection.update_one({'_id': insert_result.inserted_id},  {'$set': {"id": str(insert_result.inserted_id)}})
    character_body.id = str(insert_result.inserted_id)
    return character_body


@router.get("/v1/characters", tags=["Characters"], response_model=List[Character], summary="List all Charaters")
def list_characters(skip: int = 0, limit: int = 10) -> list:
    cursor = characters_collection.find().sort("id").skip(skip).limit(limit)
    return [Character(**doc) for doc in cursor]


@router.get("/v1/characters/{character_id}", tags=["Characters"], response_model=Character, summary="Find a Charater")
def find_character(character_id: str) -> Character:
    character_body = characters_collection.find_one({'_id': ObjectId(character_id)})
    if character_body is None:
        raise HTTPException(status_code=404, detail="Character not found.")
    else:
        return character_body


@router.put("/v1/characters/{character_id}", tags=["Characters"], response_model=Character, summary="Update a Character")
def update_character(character_id: str, character_body: Character) -> Character:
    character_body.calculate_additional_points()
    character_body.id = character_id
    if characters_collection.find_one_and_update({'_id': ObjectId(character_id)}, {'$set': character_body.to_bson()}) is None:
        raise HTTPException(status_code=404, detail="Character not found.")
    else:
        return character_body


@router.delete("/v1/characters/{character_id}", tags=["Characters"], status_code=204, summary="Delete a Character")
def delete_character(character_id: str):  
    if characters_collection.find_one_and_delete({'_id': ObjectId(character_id)}) is None:
        raise HTTPException(status_code=404, detail="Character not found.")
    else:
        return None

@router.patch("/v1/characters/{character_id}", tags=["Characters"], response_model=Character, summary="Partial Update a Character")
def partial_update_character(character_id: str, character_body: Character) -> Character:
    character_body.id = character_id
    
    stored_character_body = characters_collection.find_one({'_id': ObjectId(character_id)})
    if stored_character_body is None:
        raise HTTPException(status_code=404, detail="Character not found.")
    else:
        stored_character_model = Character(**stored_character_body)
        updated_character = stored_character_model.model_copy(update=character_body.model_dump(exclude_unset=True))
        updated_character.calculate_additional_points()
        characters_collection.find_one_and_update({'_id': ObjectId(character_id)}, {'$set': updated_character.to_bson()})
        return updated_character