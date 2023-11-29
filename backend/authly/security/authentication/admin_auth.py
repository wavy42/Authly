from typing import Annotated
from authly.crud import crud_admin
from authly.db.redis import RedisManager
from authly.models.admin_model import AdminAccount
from authly.security.authentication import token_module
from fastapi import Depends
from fastapi.exceptions import ValidationException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authly.core.utils import hashing


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/admin/token")


async def authenticate_admin_user(user_data: OAuth2PasswordRequestForm) -> str:
    try:
        user: AdminAccount = await crud_admin.get_admin_account_by_email(
            user_data.username
        )

        if not hashing.verify_password(user_data.password, user.password):
            raise ValidationException("invalid password")

        redis_manager = RedisManager(redis_db=1)
        redis_manager.connect()
        new_token: str = token_module.get_new_token(
            str(user.id), redis_manager
        )
        redis_manager.close()

    except ValueError:
        raise
    except ValidationException:
        raise
    except Exception:
        raise

    else:
        return new_token


async def get_current_admin_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> AdminAccount:
    redis_manager = RedisManager()
    try:
        redis_manager.connect()
        user_id = token_module.get_user_id(token, redis_manager)

    except Exception:
        raise ValidationException("invalid token")

    else:
        return await crud_admin.get_admin_account_by_id(user_id)

    finally:
        redis_manager.close()
