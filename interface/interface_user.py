from exceptions.errors import NotFoundError, IncorrectDataError, NotEnouhtSeatsError

class UserInterface:
    def __init__(self, flight_service, ticket_service):
        self.flight_service = flight_service
        self.ticket_service = ticket_service
    
    def menu(self, user):
        self.user = user
        while True:
            print(f"\nUSER PANEL — {self.user.username}")
            print("1. View all flights")
            print("2. Search flight by ID")
            print("3. Book ticket")
            print("4. My tickets")
            print("5. Cancel ticket")
            print("6. Profile info")
            print("0. Exit")

            choice = input("Select: ")
            if choice == "1":
                self.view_all_flights()
            elif choice == "2":
                self.search_flight()
            elif choice == "3":
                self.book_ticket()
            elif choice == "4":
                self.view_my_tickets()
            elif choice == "5":
                self.cancel_ticket()
            elif choice == "6":
                self.show_profile()
            elif choice == "0":
                break
            else:
                print("Invalid choice")



    def view_all_flights(self):
        flights = self.flight_service.get_all_flights()
        if not flights:
            print("No flights found")
        for f in flights:
            print(f)

    def search_flight(self):
        try:
            flight_id = int(input("Enter flight ID: "))
            flight = self.flight_service.get_flight_by_id(flight_id)
            print(flight)
        except NotFoundError as e:
            print(e)
        except ValueError:
            print("Error invalid input")

    def book_ticket(self):
        while True:
            try:
                flight_id = int(input("Enter flight ID to book: "))
                flight = self.flight_service.get_flight_by_id(flight_id)

                print(f"Available seats: \n1. First class: {flight.seats['first_class']}\n2. Business class: {flight.seats['business_class']}\n3. Econom class: {flight.seats['econom_class']}")
                seat_choice = input("Choice: ")
                if seat_choice == "1":
                    seat_class = "first_class"
                elif seat_choice == "2":
                    seat_class = "business_class"
                elif seat_choice == "3":
                    seat_class = "econom_class"
                else:
                    print("Invalid seat class")
                    continue

                quantity = int(input("Quantity: "))
                ticket = self.ticket_service.book_ticket(flight_id, self.user.user_id, seat_class, quantity)
                print("Ticket booked:", ticket)
                break
            except (ValueError, NotFoundError, IncorrectDataError, NotEnouhtSeatsError) as e:
                print(e)

    def view_my_tickets(self):
        tickets = self.ticket_service.get_tickets_by_user(self.user.user_id)
        if not tickets:
            print("No tickets found")
        for t in tickets:
            print(t)

    def cancel_ticket(self):
        try:
            ticket_id = int(input("Enter ticket ID to cancel: "))
            self.ticket_service.cancel_ticket(ticket_id)
            print("Ticket canceled")
        except NotFoundError as e:
            print(e)
        except ValueError:
            print("Error invalid input")

    def show_profile(self):
        print(f"\nUsername: {self.user.username}\nRole: {self.user.role}")
        self.view_my_tickets()