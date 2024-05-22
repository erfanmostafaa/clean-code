import datetime
from typing import List
from fastapi import HTTPException
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from services.db_service import DatabaseService

DEFAULT_PAGE_SIZE = 3

class PaginationUtils:
    
    @staticmethod
    async def is_valid_object_id(id):
        try:
            return ObjectId(id)
        except:
            raise HTTPException(detail="Invalid object ID", status_code=400)

    @staticmethod
    async def create_paginate_response(page, collection, match, add_wallet=False):
        page, total_docs, result = await PaginationUtils.paginate_results(page, collection, match, add_wallet)
        return {
            "page": page,
            "pageSize": DEFAULT_PAGE_SIZE,
            "totalPages": -(-total_docs // DEFAULT_PAGE_SIZE) if page else 1,
            "totalDocs": total_docs if page else len(result),
            "results": result,
        }

    @staticmethod
    async def paginate_results(page, collection, match, add_wallet=False):
        total_docs = 0
        if page is None:
            cursor = collection.find(match)
            result = list(cursor)
            for index, doc in enumerate(result):
                doc["_id"] = str(doc["_id"])
                if "affiliate_tracking_id" in doc:
                    doc["affiliate_tracking_id"] = str(doc["affiliate_tracking_id"])
                if "user_id" in doc:
                    doc["user_id"] = str(doc["user_id"])

                if add_wallet:
                    available_balance, pending_balance = await PaginationUtils.check_available_balance(doc["_id"])
                    doc["available_balance"] = available_balance
                    doc["pending_balance"] = pending_balance

                result[index] = await PaginationUtils.convert_dict_to_camel_case(doc)
        else:
            total_docs = collection.count_documents(match)
            if page < 1:
                page = 1

            skip = (page - 1) * DEFAULT_PAGE_SIZE
            limit = DEFAULT_PAGE_SIZE

            cursor = collection.find(match)
            result = await PaginationUtils.paginate_documents(cursor, skip, limit, add_wallet)
        return page, total_docs, result

    @staticmethod
    async def check_available_balance(user_id):
        user_id = await PaginationUtils.is_valid_object_id(user_id)
        wallet = DatabaseService.wallet_collection.find_one({"user_id": user_id})

        available_balance = wallet['available_balance']
        pending_balance = 0
        transactions_to_delete = []
        for transaction in wallet["transactions"]:
            if transaction["date_available"] <= datetime.datetime.now():
                available_balance += transaction["amount"]
                transactions_to_delete.append(transaction["id"])
            else:
                pending_balance += transaction["amount"]

        DatabaseService.wallet_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "available_balance": available_balance,
                    "pending_balance": pending_balance,
                },
                "$pull": {
                    "transactions": {"id": {"$in": transactions_to_delete}}
                },
            },
        )
        return available_balance, pending_balance

    @staticmethod
    async def snake_to_camel(snake_str):
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    @staticmethod
    async def convert_dict_to_camel_case(data):
        camel_dict = {}
        for key, value in data.items():
            camel_key = await PaginationUtils.snake_to_camel(key)
            camel_dict[camel_key] = value
        return camel_dict

    @staticmethod
    async def paginate_documents(cursor: Cursor, skip: int = 0, limit: int = 10, add_wallet=False) -> List[dict]:
        cursor.skip(skip).limit(limit)
        result = [doc for doc in cursor]
        for index, doc in enumerate(result):
            _id = doc["_id"]
            doc["_id"] = str(doc["_id"])
            if "affiliate_tracking_id" in doc:
                doc["affiliate_tracking_id"] = str(doc["affiliate_tracking_id"])
            if "user_id" in doc:
                doc["user_id"] = str(doc["user_id"])

            doc = await PaginationUtils.convert_dict_to_camel_case(doc)
            if add_wallet:
                available_balance, pending_balance = await PaginationUtils.check_available_balance(_id)
                doc["availableBalance"] = available_balance
                doc["pendingBalance"] = pending_balance
            result[index] = doc
        return result
