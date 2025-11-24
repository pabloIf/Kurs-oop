from storage.json_storage import JsonStorage
from services.services_flight import FlightServices
from services.services_ticket import TicketServices
from services.services_user import UserServices
from auth.services_auth import AuthServices
from interface.interface_main import MainInterface
from interface.interface_admin import AdminInterface
from interface.interface_user import UserInterface


def main():
    db = JsonStorage()

    flight_service = FlightServices(db)
    ticket_service = TicketServices(db, flight_service)
    user_service = UserServices(db, ticket_service)
    auth_services = AuthServices(user_service)

    admin_ui = AdminInterface(flight_service, user_service, ticket_service)
    user_ui = UserInterface(flight_service, ticket_service)
    main_ui = MainInterface(auth_services, admin_ui, user_ui)
    main_ui.menu()

if __name__ == "__main__":
    main()
