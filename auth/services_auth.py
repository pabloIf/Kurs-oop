from services.services_user import UserServices
from exceptions.errors import NotFoundError, IncorrectPasswordError

class AuthServices:
    def __init__(self, user_services: UserServices):
        self.user_services = user_services

    def login(self, username, password):
        user = self.user_services.get_user_by_name(username)
        if not user:
            raise NotFoundError("user not found")
        if user.password != password:
            raise IncorrectPasswordError("wrong password")
        return user
    
    def register(self, username, password, role="user"):
        return self.user_services.create_user(username, password, role)