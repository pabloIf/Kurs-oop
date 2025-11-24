from models.flight import Flight
from exceptions.errors import NotFoundError, IncorrectDataError, NotEnouhtSeatsError

class FlightServices:
    def __init__(self, storage):
        self.storage = storage
    
    def create_flight(self, origin, destination, departure, arrival, seats: dict):
        flight = Flight(
            flight_id=self.storage.generate_id(Flight),
            origin=origin,
            destination=destination,
            departure=departure,
            arrival=arrival,
            seats=seats
        )
        self.storage.add_flight(flight)
        return flight

    def delete_flight(self, flight_id):
        flight = self.get_flight_by_id(flight_id)
        deleted = self.storage.del_flight(flight_id)
        if deleted:
            self.storage.del_tickets_for_flight(flight_id)
        return deleted

    def get_flight_by_id(self, flight_id):
        flight = self.storage.get_flight(flight_id)
        if not flight:
            raise NotFoundError("flight not found")
        return flight

    def get_all_flights(self):
        return self.storage.get_flights()
    
    def check_available_seats(self, flight, seat_class, quantity):
        if seat_class not in flight.seats:
            raise IncorrectDataError("incorrect seat class")
        if flight.seats[seat_class] < quantity:
            raise NotEnouhtSeatsError("not enouht seats available")
        return True

    def booking_seats(self, flight_id, seat_class, quantity):
        flight = self.get_flight_by_id(flight_id)
        self.check_available_seats(flight, seat_class, quantity)
        flight.seats[seat_class] -= quantity
        self.storage.update_flight(flight)
        return flight
    
    def returning_seats(self, flight_id, seat_class, quantity):
        flight = self.get_flight_by_id(flight_id)
        flight.seats[seat_class] += quantity
        self.storage.update_flight(flight)
        return flight
    
    def edit_flight(self, flight_id, origin, destination, departure, arrival, seats):
        flight = self.get_flight_by_id(flight_id)
        if origin is not None:
            flight.origin = origin
        if destination is not None:
            flight.destination = destination
        if departure is not None:
            flight.departure = departure
        if arrival is not None:
            flight.arrival = arrival

        for seat_class, value in seats.items():
            if value is not None:
                flight.seats[seat_class] = int(value)
        self.storage.update_flight(flight)
        return flight