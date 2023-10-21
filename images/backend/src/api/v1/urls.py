from fastapi import APIRouter

from api.v1.handlers import pastes

api_v1_router = APIRouter(prefix='/v1')

# Pastes
api_v1_router.include_router(router=pastes.router)
