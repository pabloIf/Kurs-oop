from models.ticket import Ticket
from services.services_flight import FlightServices
from exceptions.errors import NotFoundError

class TicketServices:
    def __init__(self, storage, flight_service: FlightServices):
        self.storage = storage
        self.flight_service = flight_service

    def book_ticket(self, flight_id, user_id, seat_class, quantity):
        if quantity <= 0:
            raise ValueError("quantity seats cant be < 0")
        self.flight_service.booking_seats(flight_id, seat_class, quantity)

        tiket = Ticket(
            ticket_id=self.storage.generate_id(Ticket),
            flight_id=flight_id,
            user_id=user_id,
            seat_class=seat_class,
            quantity=quantity
        )
        self.storage.add_ticket(tiket)
        return tiket

    def cancel_ticket(self, ticket_id):
        ticket = self.get_ticket_by_id(ticket_id)
        
        self.flight_service.returning_seats(ticket.flight_id, ticket.seat_class, ticket.quantity)
        return self.storage.del_ticket(ticket_id)

    def get_tickets_by_user(self, user_id=None):
        tickets = self.storage.get_tickets()
        if user_id is None:
            return tickets
        user_tickets = [ticket for ticket in tickets if ticket.user_id == user_id]
        return user_tickets

    def get_ticket_by_id(self, ticket_id):
        ticket = self.storage.get_ticket(ticket_id)
        if not ticket:
            raise NotFoundError("ticket not found")
        return ticket
    