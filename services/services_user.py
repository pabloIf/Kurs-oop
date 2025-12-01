from models.user import User
from services.services_ticket import TicketServices
from exceptions.errors import AlreadyExistsError, NotFoundError

class UserServices:
    def __init__(self, storage, ticket_service: TicketServices):
        self.storage = storage
        self.ticket_service = ticket_service

    def create_user(self, username, password, role="user"):
        if self.get_user_by_name(username):
            raise AlreadyExistsError("username already exist")
        user = User(
            user_id=self.storage.generate_id(User),
            username=username,
            password=password,
            role=role
        )
        self.storage.add_user(user)
        return user

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        
        tickets = self.ticket_service.get_tickets_by_user(user_id)
        for ticket in tickets:
            self.ticket_service.cancel_ticket(ticket.ticket_id)
        return self.storage.del_user(user_id)

    def get_user_by_id(self, user_id):
        user = self.storage.get_user(user_id)
        if not user:
            raise NotFoundError("user not found")
        return user
    
    def get_user_by_name(self, username):
        for user in self.storage.get_users():
            if user.username == username:
                return user
        return None
    
    def get_all_users(self):
        return self.storage.get_users()
    