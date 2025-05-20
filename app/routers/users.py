from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.models.user import UserCreate, UserResponse
from app.database import users_collection

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate):
    user_dict = user.dict()
    result = await users_collection.insert_one(user_dict)
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    created_user["id"] = str(created_user["_id"])
    del created_user["_id"]
    return UserResponse(**created_user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    del user["_id"]
    return UserResponse(**user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserCreate):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    user_dict = user.dict()
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": user_dict}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    updated_user["id"] = str(updated_user["_id"])
    del updated_user["_id"]
    return UserResponse(**updated_user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return