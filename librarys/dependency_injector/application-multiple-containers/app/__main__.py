import sys

from dependency_injector import Provide, inject

from .services import AuthService, PhotoService, UserService
from .containers import Application


@inject
def main(
    email: str,
    password: str,
    photo: str,
    user_service: UserService = Provide[Application.services.user],
    auth_service: AuthService = Provide[Application.services.auth],
    photo_service: PhotoService = Provide[Application.services.photo],
) -> None:
    user = user_service.get_user(email=email)
    auth_service.authenticate(user=user, password=password)
    photo_service.upload_photo(user=user, photo=photo)


if __name__ == "__main__":
    application = Application()
    application.core.init_resources()
    application.wire(modules=[__name__])

    main(*sys.argv[1:])
