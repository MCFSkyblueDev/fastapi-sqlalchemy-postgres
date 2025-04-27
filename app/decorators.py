
from ast import List
from functools import wraps

from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_user
from app.enums.roles import Role
from app.models.user import UserModel


def check_role(allowed_roles : List[Role]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user : UserModel = Depends(get_current_user), ** kwargs):
            if len(allowed_roles) > 0 and allowed_roles. current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to access this resource",
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# def role_required(required_role: List[Role]):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             current_user: UserModel = kwargs.get("current_user")
#             if not current_user or current_user.role != required_role:
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail="You do not have permission to access this resource",
#                 )
#             return await func(*args, **kwargs)
#         return wrapper
#     return decorator