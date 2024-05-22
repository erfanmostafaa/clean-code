from services.db_service import DatabaseService
from pymongo.collection import Collection

class TestDatabaseService:
    def test_get_user_collection(self):
        assert isinstance(DatabaseService.user_collection, Collection)

    def test_get_wallet_collection(self):
        assert isinstance(DatabaseService.wallet_collection, Collection)

    def test_get_payout_collection(self):
        assert isinstance(DatabaseService.payout_collection, Collection)
