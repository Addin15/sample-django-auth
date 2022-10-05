import dataclasses
import datetime
import jwt
from typing import TYPE_CHECKING, List
from django.conf import settings
from . import models
from .models import User

if TYPE_CHECKING:
    from .models import User


@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    password: str = None
    id: int = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            id=user.id,
        )


def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    instance = models.User(
        first_name=user_dc.first_name,
        last_name=user_dc.last_name,
        email=user_dc.email,
    )

    if user_dc.password is not None:
        instance.set_password(user_dc.password)

    instance.save()

    return UserDataClass.from_instance(instance)


def update_user(user: "User", data: dict) -> "UserDataClass":
    user = User.objects.filter(id=user.id).first()

    user.first_name = data['first_name']
    user.last_name = data['last_name']

    user.save()

    return UserDataClass.from_instance(user)


def get_all_users() -> List["UserDataClass"]:

    users_object = User.objects.all()
    users = []

    for user in users_object:
        users.append(UserDataClass.from_instance(user=user))

    return users


def user_email_selector(email: str) -> "User":
    user = models.User.objects.filter(email=email).first()

    return user


def create_token(user_id: int) -> str:
    payload = dict(
        id=user_id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=48),
        iat=datetime.datetime.utcnow(),
    )

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token
