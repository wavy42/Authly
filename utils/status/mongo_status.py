import asyncio
from datetime import datetime
from authly.core.db.mongo_crud import MongoDBManager
from authly.config import application_config
from authly.core.log import Logger, LogLevel

mongo_config = application_config.MongodbSettings  # type: ignore


MONGODB_URL = mongo_config.MONGODB_URL
DB_NAME = f"{mongo_config.MONGODB_NAME}TESTER"
COLLECTION_NAME = "Test"


# Create an instance of the MongoDBManager
mongo = MongoDBManager(
    db_url=MONGODB_URL, db_name=DB_NAME, collection_name=COLLECTION_NAME
)


# Test function to check the MongoDB operations
async def async_mongo_operations() -> dict:
    test_results = {}
    Logger.debug_log(True)

    # Connect to MongoDB
    connected = await mongo.client.server_info()
    if connected:
        test_results["connection"] = "Passed"
    if not connected:
        Logger.log(LogLevel.ERROR, "Failed to connect to MongoDB:", connected)
        test_results["connection"] = "Failed"

    # Perform a write operation
    data = {"example_key": "example_value", "timestamp": datetime.now()}
    status, inserted_id = await mongo.write_manager.insert_document(data)
    if status:
        test_results["write_operation"] = "Passed"
        Logger.log(LogLevel.DEBUG, f"Document inserted with ID: {inserted_id}")
    else:
        test_results["write_operation"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to insert document into MongoDB")

    # Perform a read operation
    query = {"example_key": "example_value"}
    status, result = await mongo.read_manager.find_one(query)
    if status:
        test_results["read_operation"] = "Passed"
        Logger.log(
            LogLevel.DEBUG, f"Document retrieved from MongoDB: {result}"
        )
    else:
        test_results["read_operation"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to retrieve document from MongoDB")

    # Perform an update operation
    update_data = {"set": {"example_key": "updated_value"}}
    (
        status,
        _,
    ) = await mongo.update_manager.update_one_document(query, update_data)
    if status:
        test_results["update_operation"] = "Passed"
        Logger.log(LogLevel.DEBUG, "Document updated successfully in MongoDB")
    else:
        test_results["update_operation"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to update document in MongoDB")

    # Perform a delete operation
    (
        status,
        _,
    ) = await mongo.delete_manager.delete_document(query)
    if status:
        test_results["delete_operation"] = "Passed"
        Logger.log(
            LogLevel.DEBUG, "Document deleted successfully from MongoDB"
        )
    else:
        test_results["delete_operation"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to delete document from MongoDB")

    try:
        await mongo.client.drop_database(DB_NAME)
        Logger.log(
            LogLevel.DEBUG, f"The database '{DB_NAME}' has been deleted"
        )
    except Exception as e:
        Logger.log(
            LogLevel.ERROR, f"Failed to delete the database '{DB_NAME}': {e}"
        )

    # Close the MongoDB connection
    status, status = await mongo.close_connection()
    if status:
        test_results["close_connection"] = "Passed"
        Logger.log(LogLevel.DEBUG, "MongoDB connection closed successfully")
    else:
        test_results["close_connection"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to close MongoDB connection")

    return {"MongoDB": [test_results]}


async def print_results():
    Logger.tests(await async_mongo_operations())  # type: ignore


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_results())
