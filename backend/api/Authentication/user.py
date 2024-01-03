from fastapi import (Depends,
                     HTTPException,
                     APIRouter
                    )


api = APIRouter(prefix="/auth")
openapi_tags = {
    "name":"Auth",
    "description":"Routes to interact with auth API functionality."   
}


