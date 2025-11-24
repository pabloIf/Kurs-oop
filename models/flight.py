
class Flight:
    def __init__(self, flight_id, origin, destination, departure, arrival, seats):
        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
        self.seats = seats

    collection = "flights"
    id_field = "flight_id"

    def to_json(self):
        return {
            "flight_id": self.flight_id,
            "origin": self.origin,
            "destination": self.destination,
            "departure": self.departure,
            "arrival": self.arrival,
            "seats": self.seats
        }
