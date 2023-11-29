from typing import Any
from authly.db.mongo import MongoDBManager
from authly.models import admin_model
from authly.core.utils.log import Logger, LogLevel
from authly.core.utils import object_id
from pymongo.errors import PyMongoError

ADMIN_COLLECTION = "Admins"


async def insert_admin_user(
    data: admin_model.AdminAccount,
) -> tuple[bool, admin_model.AdminAccount, str]:
    mongo_manager = MongoDBManager(ADMIN_COLLECTION)
    try:
        status, id, details = await mongo_manager.insert_document(
            {
                "username": data.username,
                "password": data.password,
                "email": data.email,
                "role": data.role,
                "geo_location": data.geo_location,
                "bubble": data.bubble,
                "settings": data.settings,
            }
        )
        data.id = str(id)
        Logger.log(
            LogLevel.DEBUG, f"{id} -> {data.id} ({type(data.id)})", details
        )

    except PyMongoError as e:
        Logger.log(LogLevel.ERROR, "MongoDB error in insert_admin_user:", e)
        raise

    except Exception as e:
        Logger.log(LogLevel.ERROR, "Error occured in interface/admin:", e)
        raise Exception(e)

    finally:
        try:
            await mongo_manager.close_connection()

        except Exception:
            raise

    return status, data, details


async def get_all_admin_user() -> tuple[
    bool, admin_model.AllAdminAccounts, str
]:
    mongo_manager = MongoDBManager(ADMIN_COLLECTION)
    try:
        success, documents, message = await mongo_manager.get_all_documents()

        if not success:
            return False, admin_model.AllAdminAccounts(data=[]), "Failed"

        admin_accounts = [
            admin_model.AdminAccount(**object_id.convert_object_id_to_str(doc))
            for doc in documents
        ]
        all_admin_accounts = admin_model.AllAdminAccounts(data=admin_accounts)

    except Exception:
        raise

    else:
        return True, all_admin_accounts, ""

    finally:
        try:
            _, _, _ = await mongo_manager.close_connection()

        except Exception:
            raise


async def get_admin_user(
    key: str, value: str | Any
) -> admin_model.AdminAccount:
    mongo_manager = MongoDBManager(ADMIN_COLLECTION)
    try:
        (status, data, details) = await mongo_manager.find_one({key: value})

        Logger.log(LogLevel.DEBUG, status, data, details)
        if not status:
            raise ValueError("invalid email/username")

        result = admin_model.AdminAccount(
            **object_id.convert_object_id_to_str(data)
        )

    except Exception:
        raise

    else:
        return result

    finally:
        await mongo_manager.close_connection()
