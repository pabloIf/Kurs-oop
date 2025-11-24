
class Ticket:
    def __init__(self, ticket_id, flight_id, user_id, seat_class, quantity):
        self.ticket_id = ticket_id
        self.flight_id = flight_id
        self.user_id = user_id
        self.seat_class = seat_class
        self.quantity = quantity

    collection = "tickets"
    id_field = "ticket_id"

    def to_json(self):
        return {
            "ticket_id": self.ticket_id,
            "flight_id": self.flight_id,
            "user_id": self.user_id,
            "seat_class": self.seat_class,
            "quantity": self.quantity
        }