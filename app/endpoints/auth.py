from fastapi import APIRouter
from Filteration.auth import LoginRequest, SignupRequest
from repositary.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", description="Register a new user with email and password")
async def signup(payload: SignupRequest):
    return await UserRepository().signup_user(payload)


@router.post("/login", description="Authenticate user with email and password")
async def login(payload: LoginRequest):
    return await UserRepository().login_user(payload)


@router.get("/profile", description="Get user profile by email")
async def get_profile(email: str):
    return await UserRepository().get_user_profile(email)

