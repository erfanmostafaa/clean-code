from services.auth_service import AuthService
from fastapi import HTTPException
import jwt
from services.db_service import DatabaseService



class TestAuthService:
    async def test_check_user_is_admin_valid_admin(self, mocker):
        authorization_header = "Bearer token"
        mocked_user_collection = mocker.patch.object(DatabaseService, 'user_collection')
        mocked_user_collection.find_one.return_value = {'email': 'admin@example.com', 'user_type': 'admin'}
        assert AuthService.check_user_is_admin(authorization_header) == {'email': 'admin@example.com', 'user_type': 'admin'}

    def test_check_user_is_admin_invalid_user(self, mocker):
        authorization_header = "Bearer token"
        mocked_user_collection = mocker.patch.object(DatabaseService, 'user_collection')
        mocked_user_collection.find_one.return_value = None

        try:
            AuthService.check_user_is_admin(authorization_header)
        except HTTPException as e:
            assert e.status_code == 404

    