from exceptions.errors import NotFoundError, AlreadyExistsError

class AdminInterface:
    def __init__(self, flight_service, user_service, ticket_service):
        self.flight_service = flight_service
        self.user_service = user_service
        self.ticket_service = ticket_service

    def menu(self):
        while True:
            print("\nADMIN PANEL")
            print("1. Manage flights")
            print("2. Manage users")
            print("3. Manage tickets")
            print("0. Exit")
            choice = input("Select: ")
            
            if choice == "1":
                self.flight_menu()
            elif choice == "2":
                self.user_menu()
            elif choice == "3":
                self.ticket_menu()
            elif choice == "0":
                break
            else:
                print("Invalid choice")

    def flight_menu(self):
        while True:
            print("\nFLIGHT MANAGEMENT")
            print("1. Create flight")
            print("2. Review all flights")
            print("3. Search flight by ID")
            print("4. Delete flight")
            print("5. Edit flight")
            print("0. Back")
            choice = input("Choice: ")

            if choice == "1":
                self.create_flight()
            elif choice == "2":
                self.review_flights()
            elif choice == "3":
                self.search_flight()
            elif choice == "4":
                self.delete_flight()
            elif choice == "5":
                self.edit_flight()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def user_menu(self):
        while True:
            print("\nUSER MANAGEMENT")
            print("1. Review all users")
            print("2. Search user by ID")
            print("3. Search user by username")
            print("4. Create ADMIN")
            print("5. Delete user")
            print("0. Back")
            choice = input("Choice: ")

            if choice == "1":
                self.review_users()
            elif choice == "2":
                self.search_user_by_id()
            elif choice == "3":
                self.search_user_by_username()
            elif choice == "4":
                self.create_admin()
            elif choice == "5":
                self.delete_user()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def ticket_menu(self):
        while True:
            print("\nTICKET MANAGEMENT")
            print("1. Review all tickets")
            print("2. Search ticket by ID")
            print("3. Delete ticket")
            print("0. Back")
            choice = input("Choice: ")

            if choice == "1":
                self.review_tickets()
            elif choice == "2":
                self.search_ticket()
            elif choice == "3":
                self.delete_ticket()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")



    def create_flight(self):
        print("Fill in all fields:\n")
        origin = input("Origin: ")
        destination = input("Destination: ")
        departure = input("Departure: ")
        arrival = input("Arrival: ")
        seats = {}
        seats["first_class"] = int(input("First class seats: "))
        seats["business_class"] = int(input("Business seats: "))
        seats["econom_class"] = int(input("Economy seats: "))
        new_flight = self.flight_service.create_flight(origin, destination, departure, arrival, seats)

    def review_flights(self):
        flights = self.flight_service.get_all_flights()
        if not flights:
            print("No flights found")
        for f in flights:
            print(f.to_json())

    def search_flight(self):
        try:
            flight_id = int(input("Enter flight ID: "))
            flight = self.flight_service.get_flight_by_id(flight_id)
            print(flight.to_json())
        except NotFoundError as e:
            print(e)
        except ValueError:
            print("Error invalid input")

    def delete_flight(self):
        try:
            flight_id = input("Enter flight ID to delete: ")
            flight = self.flight_service.delete_flight(int(flight_id))
            print("Flight deleted")
        except NotFoundError as e:
            print(e)
        except ValueError:
            print("Error invalid input")

    def edit_flight(self):
        try:
            flight_id = int(input("Enter flight ID: "))
            print("\nLeave empty to keep old value")
            new_origin = input("Origin: ")
            new_destination = input("Destination: ")
            new_departure = input("Departure: ")
            new_arrival = input("Arrival: ")

            seats = {}
            print("\nUpdate seats:")
            for seat_class in ["first_class", "business_class", "econom_class"]:
                value = input(f"{seat_class}: ")
                seats[seat_class] = value if value else None

            self.flight_service.edit_flight(
                flight_id,
                new_origin or None,
                new_destination or None,
                new_departure or None,
                new_arrival or None,
                seats
            )
            print("Flight updated successfully.")
        except Exception as e:
            print("Error:", e)



    def review_users(self):
        users = self.user_service.get_all_users()
        for u in users:
            print(u.to_json())
    
    def search_user_by_id(self):
        try:
            user_id = int(input("User ID: "))
            user = self.user_service.get_user_by_id(user_id)
            user_tickets = self.ticket_service.get_tickets_by_user(user_id)
            print(user.to_json())
            print([user_ticket.to_json() for user_ticket in user_tickets])
        except NotFoundError as e:
            print(e)
        except ValueError:
            print("Error invalid input")
    
    def search_user_by_username(self):
        username = input("Username: ")
        user = self.user_service.get_user_by_name(username)
        user_tickets = self.ticket_service.get_tickets_by_user(user.user_id)
        if not user:
            print(f"User '{username}' not found")
            return
        else:
            print(user.to_json())
            print([user_ticket.to_json() for user_ticket in user_tickets])
    
    def create_admin(self):
        username = input("Admin username: ")
        password = input("Admin password: ")
        try:
            admin = self.user_service.create_user(username, password, role="admin")
            print(f"Admin '{username}' created successfully.")
        except AlreadyExistsError as e:
            print("Error:", e)
    
    def delete_user(self):
        try:
            user_id = int(input("User ID: "))
            user = self.user_service.delete_user(user_id)
        except NotFoundError as e:
            print(e)
            


    def review_tickets(self):
        tickets = self.ticket_service.get_tickets_by_user()
        if not tickets:
            print("No tickets found")
        for t in tickets:
            print(t)
    
    def search_ticket(self):
        try:
            ticket_id = int(input("Enter ticket ID: "))
            ticket = self.ticket_service.get_ticket_by_id(ticket_id)
            print(ticket.to_json())
        except NotFoundError as e:
            print(e)
        except ValueError:
            print("Error invalid input")
    
    def delete_ticket(self):
        try:
            ticket_id = int(input("Enter ticket ID to delete: "))
            self.ticket_service.cancel_ticket(ticket_id)
            print("Ticket deleted")
        except ValueError:
            print("Error invalid input")
