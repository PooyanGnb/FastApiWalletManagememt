from fastapi import FastAPI

# Import routers from different modules
from routers.users import router as user_router
from routers.receipt import router as receipt_router


app = FastAPI()

# Include routers in the application
app.include_router(user_router)
app.include_router(receipt_router)