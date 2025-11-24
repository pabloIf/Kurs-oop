import json
import os
from models.flight import Flight
from models.ticket import Ticket
from models.user import User


class JsonStorage:
    def __init__(self, filename="storage.json"):

        storage_dirname = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(storage_dirname, filename)

        self.data = {"flights": [], "tickets": [], "users": []}
        self._load()

    def _load(self):
        try:
            with open(self.path, "r") as file:
                data = file.read().strip()
                if not data:
                    self._save()
                    return
                self.data = json.loads(data)
        except FileNotFoundError:
            self._save()

    def _save(self):
        with open(self.path, "w") as file:
            json.dump(self.data, file, indent=4)

    def generate_id(self, model):
        items = self.data[model.collection]
        if not items:
            return 1
        return max(item[model.id_field] for item in items) + 1
    

    
    def add_flight(self, flight: Flight):
        self.data["flights"].append(flight.to_json())
        self._save()

    def get_flight(self, flight_id):
        for flight in self.data["flights"]:
            if flight["flight_id"] == flight_id:
                return Flight(**flight)

    def get_flights(self):
        flights = []
        for flight in self.data["flights"]:
            flights.append(Flight(**flight))
        return flights
    
    def del_flight(self, flight_id):
        before = len(self.data["flights"])
        new_flights = []

        for flight in self.data["flights"]:
            if flight["flight_id"] != flight_id:
                new_flights.append(flight)
        after = len(new_flights)

        if before != after:
            self.data["flights"] = new_flights
            self._save()
            return True
        return False
    
    def update_flight(self, flight: Flight):
        for i, f in enumerate(self.data["flights"]):
            if f["flight_id"] == flight.flight_id:
                self.data["flights"][i] = flight.to_json()
                self._save()
                return True
        return False



    def add_ticket(self, ticket: Ticket):
        self.data["tickets"].append(ticket.to_json())
        self._save()

    def get_ticket(self, ticket_id):
        for ticket in self.data["tickets"]:
            if ticket["ticket_id"] == ticket_id:
                return Ticket(**ticket)

    def get_tickets(self):
        tickets = []
        for ticket in self.data["tickets"]:
            tickets.append(Ticket(**ticket))
        return tickets
    
    def del_ticket(self, ticket_id):
        before = len(self.data["tickets"])
        new_tickets = []

        for ticket in self.data["tickets"]:
            if ticket["ticket_id"] != ticket_id:
                new_tickets.append(ticket)
        after = len(new_tickets)

        if before != after:
            self.data["tickets"] = new_tickets
            self._save()
            return True
        return False
    
    def del_tickets_for_flight(self, flight_id):
        before = len(self.data["tickets"])
        new_tickets = []

        for ticket in self.data["tickets"]:
            if ticket["flight_id"] != flight_id:
                new_tickets.append(ticket)
        after = len(new_tickets)

        if before != after:
            self.data["tickets"] = new_tickets
            self._save()
            return True
        return False



    def add_user(self, user: User):
        self.data["users"].append(user.to_json())
        self._save()

    def del_user(self, user_id):
        before = len(self.data["users"])
        new_users = []

        for user in self.data["users"]:
            if user["user_id"] != user_id:
                new_users.append(user)
        after = len(new_users)

        if before != after:
            self.data["users"] = new_users
            self._save()
            return True
        return False

    def get_user(self, user_id):
        for user in self.data["users"]:
            if user["user_id"] == user_id:
                return User(**user)

    def get_users(self):
        users = []
        for user in self.data["users"]:
            users.append(User(**user))
        return users
