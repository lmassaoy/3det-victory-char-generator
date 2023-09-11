from typing import Annotated, List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Header
from pydantic import ValidationError
from ..models.base_entities import NPC
from ..db import get_collection


npcs_collection = get_collection('npcs')
router = APIRouter()


@router.post("/v1/npcs",
            tags=["NPCs"],
            response_model=NPC,
            status_code=201,
            summary="Create a NPC")
def create_npc(character_body: NPC) -> NPC:
    character_body.calculate_additional_points()
    insert_result = npcs_collection.insert_one(character_body.to_bson())
    npcs_collection.update_one({'_id': insert_result.inserted_id},  {'$set': {"id": str(insert_result.inserted_id)}})
    character_body.id = str(insert_result.inserted_id)
    return character_body


@router.get("/v1/npcs", tags=["NPCs"], response_model=List[NPC], summary="List all NPCs")
def list_npcs(skip: int = 0, limit: int = 10) -> list:
    cursor = npcs_collection.find().sort("id").skip(skip).limit(limit)
    return [NPC(**doc) for doc in cursor]


# @router.get("/v1/characters/{character_id}", tags=["Characters"], response_model=Character, summary="Find a Charater")
# def find_character(character_id: str) -> Character:
#     character_body = npcs_collection.find_one({'_id': ObjectId(character_id)})
#     if character_body is None:
#         raise HTTPException(status_code=404, detail="Character not found.")
#     else:
#         return character_body


# @router.put("/v1/characters/{character_id}", tags=["Characters"], response_model=Character, summary="Update a Character")
# def update_character(character_id: str, character_body: Character) -> Character:
#     character_body.calculate_additional_points()
#     character_body.id = character_id
#     if npcs_collection.find_one_and_update({'_id': ObjectId(character_id)}, {'$set': character_body.to_bson()}) is None:
#         raise HTTPException(status_code=404, detail="Character not found.")
#     else:
#         return character_body


# @router.delete("/v1/characters/{character_id}", tags=["Characters"], status_code=204, summary="Delete a Character")
# def delete_character(character_id: str):  
#     if npcs_collection.find_one_and_delete({'_id': ObjectId(character_id)}) is None:
#         raise HTTPException(status_code=404, detail="Character not found.")
#     else:
#         return None

# @router.patch("/v1/characters/{character_id}", tags=["Characters"], response_model=Character, summary="Partial Update a Character")
# def partial_update_character(character_id: str, character_body: Character) -> Character:
#     character_body.id = character_id
    
#     stored_character_body = npcs_collection.find_one({'_id': ObjectId(character_id)})
#     if stored_character_body is None:
#         raise HTTPException(status_code=404, detail="Character not found.")
#     else:
#         stored_character_model = Character(**stored_character_body)
#         updated_character = stored_character_model.model_copy(update=character_body.model_dump(exclude_unset=True))
#         updated_character.calculate_additional_points()
#         npcs_collection.find_one_and_update({'_id': ObjectId(character_id)}, {'$set': updated_character.to_bson()})
#         return updated_character