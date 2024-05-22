
from fastapi import HTTPException, Header
import jwt, os
import services

class AuthService:
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", 0))

    @staticmethod
    async def check_user_is_admin(authorization: str = Header(...)):
        email = await AuthService.get_email_from_token(authorization)
        user = services.DatabaseService.user_collection.find_one({'email': email})
        if user is None:
            raise HTTPException(detail='User not found', status_code=404)
        if user['user_type'] != 'admin':
            raise HTTPException(detail='User is not Admin', status_code=400)
        return user

    @staticmethod
    async def get_email_from_token(authorization: str = Header(...)):
        try:
            decode_token = AuthService.decode_jwt_token(authorization)
            email = decode_token["sub"]
            print(email)
        except Exception as e:
            print(f"Error: {str(e)}")
            raise HTTPException(detail="Invalid token", status_code=400)
        return email

    @staticmethod
    def decode_jwt_token(token: str):
        try:
            payload = jwt.decode(token, AuthService.JWT_SECRET, algorithms=[AuthService.JWT_ALGORITHM])
            return payload
        except jwt.PyJWTError:
            return {}

    @staticmethod
    async def parse_statuses(statuses):
        return [status.strip() for status in statuses.split(",")]
