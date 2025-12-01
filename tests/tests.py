from storage.json_storage import JsonStorage
from services.services_flight import FlightServices
from services.services_ticket import TicketServices

def test_book_ticket():
    storage = JsonStorage("test.json")
    flight_service = FlightServices(storage)
    ticket_service = TicketServices(storage, flight_service)

    flight = flight_service.create_flight("Kyiv", "Paris", "2025-01-01", "2025-01-01", {"economy": 50})

    ticket = ticket_service.book_ticket(flight.flight_id, 1, "economy", 2)

    updated = storage.get_flight(flight.flight_id)

    assert updated.seats["economy"] == 48


def test_cancel_ticket():
    storage = JsonStorage("test.json")
    flight_service = FlightServices(storage)
    ticket_service = TicketServices(storage, flight_service)

    flight = flight_service.create_flight("Kyiv", "Rome", "2025-01-01", "2025-01-01", {"business": 10})

    ticket = ticket_service.book_ticket(flight.flight_id, 1, "business", 2)
    ticket_service.cancel_ticket(ticket.ticket_id)

    updated_flight = storage.get_flight(flight.flight_id)

    assert updated_flight.seats["business"] == 10

open("test.json", "w").write("")
test_book_ticket()
print("1")

open("test.json", "w").write("")
test_cancel_ticket()
print("2")
