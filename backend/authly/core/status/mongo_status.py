import asyncio
from datetime import datetime
from authly.core.db.mongo_crud import MongoDBManager
from authly.core.config import application_config
from authly.core.log import Logger
from authly.core.log import LogLevel

MONGODB_URL = application_config.MongodbSettings.MONGODB_URL
DB_NAME = f"{application_config.MongodbSettings.MONGODB_NAME}TESTER"
COLLECTION_NAME = "Test"


# Create an instance of the MongoDBManager
mongo = MongoDBManager(
    db_url=MONGODB_URL, db_name=DB_NAME, collection_name=COLLECTION_NAME
)


# Test function to check the MongoDB operations
async def async_mongo_operations() -> dict:
    test_results = {}
    Logger.set_verbosity_level(level="DEVELOPMENT")

    # Connect to MongoDB
    connected = await mongo.client.server_info()
    if connected:
        test_results["connection"] = "Passed"
    if not connected:
        Logger.log(LogLevel.ERROR, "Failed to connect to MongoDB:", connected)
        test_results["connection"] = "Failed"

    # Perform a write operation
    data = {"example_key": "example_value", "timestamp": datetime.now()}
    _, inserted_id = await mongo.write_manager.insert_document(data)
    if _:
        test_results["write_operation"] = "Passed"
        Logger.log(LogLevel.DEBUG, f"Document inserted with ID: {inserted_id}")
    else:
        test_results["write_operation"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to insert document into MongoDB")

    # Perform a read operation
    query = {"example_key": "example_value"}
    _, result = await mongo.read_manager.find_one(query)
    if _:
        test_results["read_operation"] = "Passed"
        Logger.log(
            LogLevel.DEBUG, f"Document retrieved from MongoDB: {result}"
        )
    else:
        test_results["read_operation"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to retrieve document from MongoDB")

    # Perform an update operation
    update_data = {"set": {"example_key": "updated_value"}}
    _, update_result = await mongo.update_manager.update_one_document(
        query, update_data
    )
    if _:
        test_results["update_operation"] = "Passed"
        Logger.log(LogLevel.DEBUG, "Document updated successfully in MongoDB")
    else:
        test_results["update_operation"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to update document in MongoDB")

    # Perform a delete operation
    _, delete_result = await mongo.delete_manager.delete_document(query)
    if _:
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
    closed, _ = await mongo.close_connection()
    if closed:
        test_results["close_connection"] = "Passed"
        Logger.log(LogLevel.DEBUG, "MongoDB connection closed successfully")
    else:
        test_results["close_connection"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to close MongoDB connection")

    return {"MongoDB": [test_results]}


async def print_results():
    Logger.tests(await async_mongo_operations())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_results())
