from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import Optional, List

from app.domains.passenger import Passenger
from app.domains.route import Route
from app.domains.trip import trip as RideRequest
from app.models.model import PassengerDB, RouteDB, TripDB
from database import get_db_session

class FmsService:
    def __init__(self, session: Session):
        self.session: Session = session

    def create_passenger(self, passenger: Passenger) -> Passenger:
        try:
            passenger_db = PassengerDB(
                id=passenger.id,
                name=passenger.name,
                contact_info=passenger.contact_info
            )
            self.session.add(passenger_db)
            self.session.commit()
            self.session.refresh(passenger_db)
            return passenger
        except Exception as e:
            print(f"Error creating passenger: {e}")
            self.session.rollback()
            return None

    def create_ride_route(self, route: Route) -> Route:
        try:
            route_db = RouteDB(
                id=route.id,
                driver_id=route.driver_id,
                car_plate_number=route.car_plate_number,
                departure_location_name=route.departure_location_name,
                departure_time=route.departure_time,
                destination_location_name=route.destination_location_name
            )
            self.session.add(route_db)
            self.session.commit()
            self.session.refresh(route_db)
            return route
        except Exception as e:
            print(f"Error creating ride route: {e}")
            self.session.rollback()
            return None

    def get_ride_route(self, route_id: UUID) -> Optional[Route]:
        try:
            route_db = self.session.query(RouteDB).filter(RouteDB.id == route_id).first()
            if route_db:
                return Route(
                    id=route_db.id,
                    driver_id=route_db.driver_id,
                    car_plate_number=route_db.car_plate_number,
                    departure_location_name=route_db.departure_location_name,
                    departure_time=route_db.departure_time,
                    destination_location_name=route_db.destination_location_name
                )
            return None
        except Exception as e:
            print(f"Error getting ride route: {e}")
            return None

    def find_ride_routes(
        self,
        driver_id: Optional[UUID] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        departure_location_name: Optional[str] = None,
        destination_location_name: Optional[str] = None,
    ) -> List[Route]:
        try:
            query = self.session.query(RouteDB)
            
            if driver_id:
                query = query.filter(RouteDB.driver_id == driver_id)
            if start_time:
                query = query.filter(RouteDB.departure_time >= start_time)
            if end_time:
                query = query.filter(RouteDB.departure_time <= end_time)
            if departure_location_name:
                query = query.filter(RouteDB.departure_location_name == departure_location_name)
            if destination_location_name:
                query = query.filter(RouteDB.destination_location_name == destination_location_name)

            routes_db = query.all()
            return [Route(
                id=route.id,
                driver_id=route.driver_id,
                car_plate_number=route.car_plate_number,
                departure_location_name=route.departure_location_name,
                departure_time=route.departure_time,
                destination_location_name=route.destination_location_name
            ) for route in routes_db]
        except Exception as e:
            print(f"Error finding ride routes: {e}")
            return []

    def update_ride_route(self, route_id: UUID, route: Route) -> Optional[Route]:
        try:
            route_db = self.session.query(RouteDB).filter(RouteDB.id == route_id).first()
            if route_db:
                route_db.car_plate_number = route.car_plate_number
                route_db.departure_location_name = route.departure_location_name
                route_db.departure_time = route.departure_time
                route_db.destination_location_name = route.destination_location_name
                
                self.session.commit()
                self.session.refresh(route_db)
                
                return Route(
                    id=route_db.id,
                    driver_id=route_db.driver_id,
                    car_plate_number=route_db.car_plate_number,
                    departure_location_name=route_db.departure_location_name,
                    departure_time=route_db.departure_time,
                    destination_location_name=route_db.destination_location_name
                )
            return None
        except Exception as e:
            print(f"Error updating ride route: {e}")
            self.session.rollback()
            return None

    def delete_ride_route(self, route_id: UUID):
        try:
            route_db = self.session.query(RouteDB).filter(RouteDB.id == route_id).first()
            if route_db:
                self.session.delete(route_db)
                self.session.commit()
        except Exception as e:
            print(f"Error deleting ride route: {e}")
            self.session.rollback()

    def create_ride_request(self, ride_request: RideRequest) -> RideRequest:
        try:
            trip_db = TripDB(
                id=ride_request.id,
                ride_route_id=ride_request.ride_route_id,
                passenger_id=ride_request.passenger_id,
                pickup_request_location_name=ride_request.pickup_request_location_name,
                pickup_time=ride_request.pickup_time,
                is_approved=ride_request.is_approved
            )
            self.session.add(trip_db)
            self.session.commit()
            self.session.refresh(trip_db)
            return ride_request
        except Exception as e:
            print(f"Error creating ride request: {e}")
            self.session.rollback()
            return None

    def get_ride_request(self, request_id: UUID) -> Optional[RideRequest]:
        try:
            trip_db = self.session.query(TripDB).filter(TripDB.id == request_id).first()
            if trip_db:
                return RideRequest(
                    id=trip_db.id,
                    ride_route_id=trip_db.ride_route_id,
                    passenger_id=trip_db.passenger_id,
                    pickup_request_location_name=trip_db.pickup_request_location_name,
                    pickup_time=trip_db.pickup_time,
                    is_approved=trip_db.is_approved
                )
            return None
        except Exception as e:
            print(f"Error getting ride request: {e}")
            return None

    def find_ride_requests(
        self,
        ride_route_id: Optional[UUID] = None,
        passenger_id: Optional[UUID] = None,
        is_approved: Optional[bool] = None,
    ) -> List[RideRequest]:
        try:
            query = self.session.query(TripDB)
            
            if ride_route_id:
                query = query.filter(TripDB.ride_route_id == ride_route_id)
            if passenger_id:
                query = query.filter(TripDB.passenger_id == passenger_id)
            if is_approved is not None:
                query = query.filter(TripDB.is_approved == is_approved)

            trips_db = query.all()
            return [RideRequest(
                id=trip.id,
                ride_route_id=trip.ride_route_id,
                passenger_id=trip.passenger_id,
                pickup_request_location_name=trip.pickup_request_location_name,
                pickup_time=trip.pickup_time,
                is_approved=trip.is_approved
            ) for trip in trips_db]
        except Exception as e:
            print(f"Error finding ride requests: {e}")
            return []

    def approve_ride_request(self, request_id: UUID) -> Optional[RideRequest]:
        try:
            trip_db = self.session.query(TripDB).filter(TripDB.id == request_id).first()
            if trip_db:
                trip_db.is_approved = True
                self.session.commit()
                self.session.refresh(trip_db)
                
                return RideRequest(
                    id=trip_db.id,
                    ride_route_id=trip_db.ride_route_id,
                    passenger_id=trip_db.passenger_id,
                    pickup_request_location_name=trip_db.pickup_request_location_name,
                    pickup_time=trip_db.pickup_time,
                    is_approved=trip_db.is_approved
                )
            return None
        except Exception as e:
            print(f"Error approving ride request: {e}")
            self.session.rollback()
            return None
