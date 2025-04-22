from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Health"])
def read_root():
    return {"message": "Electrik Light Orchestrator API is live"}