"""
MongoDBManager Module

This module provides a MongoDBManager class for \
asynchronous MongoDB operations using motor.

Author: Your Name
Date: Your Date

Usage:
    from MongoDBManager import MongoDBManager

    # Create an instance of MongoDBManager
    manager = MongoDBManager(db_url, db_name, collection_name)

    # Perform MongoDB operations using manager methods
    result = await manager.insert_document(data)
    # ... (other operations)

    # Close the MongoDB connection when done
    await manager.close_connection()

Author: Arteii
Date: 20/11/2023
"""
from typing import Any, Tuple, List, Dict
import motor.motor_asyncio

from authly.core.config import application_config as config
from pymongo import errors as mongo_error


class MongoDBManager:
    def __init__(
        self,
        collection_name: str,
        db_url: str = config.MongodbSettings.MONGODB_URL,
        db_name: str = config.MongodbSettings.MONGODB_NAME,
    ) -> None:
        """
        Initialize MongoDBManager.

        Args:
            db_url (str): MongoDB connection URL.
            db_name (str): Database name.
            collection_name (str): Collection name.
        """
        self.client: motor.motor_asyncio.AsyncIOMotorClient = (
            motor.motor_asyncio.AsyncIOMotorClient(db_url)
        )
        self.db: motor.motor_asyncio.AsyncIOMotorDatabase = self.client[
            db_name
        ]
        self.collection: motor.motor_asyncio.AsyncIOMotorCollection = self.db[
            collection_name
        ]

    async def insert_document(
        self, data: Dict[str, Any]
    ) -> Tuple[bool, Any, str]:
        """
        Insert a document into the collection.

        Args:
            data (dict): Data to be inserted.

        Returns:
            Tuple[bool, Any, str]: Tuple indicating success, \
                inserted ID, and status message.
        """
        try:
            result = await self.collection.insert_one(data)

        except mongo_error.ServerSelectionTimeoutError:
            return (
                False,
                None,
                "ServerSelectionTimeoutError"
                "Issues with the connection to the MongoDB server. "
                "Make sure to configure it correctly.",
            )

        except mongo_error.DuplicateKeyError:
            return (
                False,
                None,
                "Duplicate key error: "
                "Document with the same key already exists",
            )
        except Exception as e:
            return False, None, f"Error inserting document: {e}"
        else:
            return True, result.inserted_id, "Document inserted successfully"

    async def find_one(
        self, query: Dict[str, Any]
    ) -> Tuple[bool, Dict[str, Any], str]:
        """
        Find a single document based on the query.

        Args:
            query (dict): Query to search for the document.

        Returns:
            Tuple[bool, dict, str]: Tuple indicating success, \
                result, and status message.
        """
        try:
            result = await self.collection.find_one(query)
        except Exception as e:
            return False, {}, f"Error finding document: {e}"
        else:
            return (
                True if result else False,
                result,  # type: ignore
                "Document found" if result else "Document not found",
            )

    async def find_many(
        self, query: Dict[str, Any]
    ) -> Tuple[bool, List[Dict[str, Any]], str]:
        """
        Find multiple documents based on the query.

        Args:
            query (dict): Query to search for documents.

        Returns:
            Tuple[bool, list, str]: Tuple indicating success, \
                result list, and status message.
        """
        try:
            result_list: List[Dict[str, Any]] = []
            async for doc in self.collection.find(query):
                result_list.append(doc)
        except Exception as e:
            return False, [], f"Error finding documents: {e}"
        else:
            return (
                True,
                result_list,
                "Documents found" if result_list else "No documents found",
            )

    async def get_all_documents(
        self,
    ) -> Tuple[bool, List[Dict[str, Any]], str]:
        """
        Get all documents from the collection.

        Returns:
            Tuple[bool, list, str]: Tuple indicating success, \
                result list, and status message.
        """
        try:
            result_list: List[Dict[str, Any]] = []
            async for doc in self.collection.find({}):
                result_list.append(doc)

        except Exception as e:
            return False, [], f"Error getting all documents: {e}"

        else:
            return (
                True,
                result_list,
                "Documents retrieved" if result_list else "No documents found",
            )

    async def update_one_document(
        self, query: Dict[str, Any], update_data: Dict[str, Any]
    ) -> Tuple[bool, Any, str]:
        """
        Update a single document based on the query.

        Args:
            query (dict): Query to identify the document.
            update_data (dict): Data to update.

        Returns:
            Tuple[bool, Any, str]: Tuple indicating success, \
                result, and status message.
        """
        try:
            result = await self.collection.update_one(
                query, {"$set": update_data}
            )

        except Exception as e:
            return False, None, f"Error updating document: {e}"

        else:
            return (
                True,
                result,
                "Document updated successfully"
                if result.modified_count > 0
                else "Document not updated",
            )

    async def replace_one_document(
        self, query: Dict[str, Any], replace_data: Dict[str, Any]
    ) -> Tuple[bool, Any, str]:
        """
        Replace a single document based on the query.

        Args:
            query (dict): Query to identify the document.
            replace_data (dict): Data to replace the existing document.

        Returns:
            Tuple[bool, Any, str]: Tuple indicating success, \
                result, and status message.
        """
        try:
            result = await self.collection.replace_one(query, replace_data)
        except Exception as e:
            return False, None, f"Error replacing document: {e}"
        else:
            return (
                True,
                result,
                "Document replaced successfully"
                if result.modified_count > 0
                else "Document not replaced",
            )

    async def delete_document(
        self, query: Dict[str, Any]
    ) -> Tuple[bool, Any, str]:
        """
        Delete a single document based on the query.

        Args:
            query (dict): Query to identify the document.

        Returns:
            Tuple[bool, Any, str]: Tuple indicating success, \
                result, and status message.
        """
        try:
            result = await self.collection.delete_one(query)
        except Exception as e:
            return False, None, f"Error deleting document: {e}"
        else:
            return (
                True,
                result,
                "Document deleted successfully"
                if result.deleted_count > 0
                else "Document not deleted",
            )

    async def delete_many_documents(
        self, query: Dict[str, Any]
    ) -> Tuple[bool, Any, str]:
        """
        Delete multiple documents based on the query.

        Args:
            query (dict): Query to identify the documents to be deleted.

        Returns:
            Tuple[bool, Any, str]: Tuple indicating success, \
                result, and status message.
        """
        try:
            result = await self.collection.delete_many(query)
        except Exception as e:
            return False, None, f"Error deleting documents: {e}"
        else:
            return (
                True,
                result,
                f"{result.deleted_count} documents deleted"
                if result.deleted_count > 0
                else "No documents deleted",
            )

    async def close_connection(self) -> Tuple[bool, str, str]:
        """
        Close the MongoDB connection.

        Returns:
            Tuple[bool, str, str]: Tuple indicating success, result message, \
                and status message.
        """
        try:
            self.client.close()
        except Exception as e:
            return False, "", f"Error closing connection: {e}"
        else:
            return True, "Connection closed", "Connection closed successfully"
