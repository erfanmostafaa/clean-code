from utils.pagination import PaginationUtils
from pymongo.cursor import Cursor
from utils.pagination import PaginationUtils

class TestPaginationUtils:


    def test_is_valid_object_id_invalid_id(self):
        id = "invalid_id"
        try:
            PaginationUtils.is_valid_object_id(id)
        except Exception as e:
            assert str(e) == "Invalid object ID"

