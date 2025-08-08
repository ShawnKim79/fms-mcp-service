from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from passlib.hash import pbkdf2_sha256

from domains.passenger import Passenger, ResponsePassenger
from domains.route import Route
from domains.trip import Trip
from controllers.dto.request_dto import RequestCreatePassenger
from models.model import PassengerDB, RouteDB, TripDB

class FmsService:
    def __init__(self, session: Session):
        self.session: Session = session

    def create_passenger(self, passenger: Passenger) -> Passenger:
        try:
            hashed_password = pbkdf2_sha256.hash(passenger.password)
            passenger_db = PassengerDB(
                id = uuid4(),
                password = hashed_password,
                name = passenger.name,
                nickname = passenger.nickname,
                contact_info = passenger.contact_info
            )
            
            self.session.add(passenger_db)
            self.session.commit()
            self.session.refresh(passenger_db)
            return Passenger.model_validate(passenger_db)
        except Exception as e:
            print(f"Error creating passenger: {e}")
            self.session.rollback()
            return None

    def create_route(self, route: Route) -> Route:
        try:
            route_db = RouteDB(
                id=uuid4(),
                departure_location_name=route.departure_location_name,
                departure_time=route.departure_time,
                destination_location_name=route.destination_location_name
            )
            self.session.add(route_db)
            self.session.commit()
            self.session.refresh(route_db)
            
            return Route.model_validate(route_db)
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
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        departure_location_name: Optional[str] = None,
        destination_location_name: Optional[str] = None,
    ) -> List[Route]:
        try:
            query = self.session.query(RouteDB)
            
            if start_time is not None:
                query = query.filter(RouteDB.departure_time >= start_time)
            if end_time is not None:
                query = query.filter(RouteDB.departure_time <= end_time)
            if departure_location_name is not None:
                query = query.filter(RouteDB.departure_location_name == departure_location_name)
            if destination_location_name is not None:
                query = query.filter(RouteDB.destination_location_name == destination_location_name)

            routes_db = query.all()
            return [Route.model_validate(route) for route in routes_db]
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

    def create_trip(self, trip: Trip) -> Trip:
        try:
            trip_db = TripDB(
                id=trip.id,
                ride_route_id=trip.ride_route_id,
                passenger_id=trip.passenger_id,
                pickup_request_location_name=trip.pickup_request_location_name,
                pickup_time=trip.pickup_time,
                is_approved=trip.is_approved
            )
            self.session.add(trip_db)
            self.session.commit()
            self.session.refresh(trip_db)
            return trip
        except Exception as e:
            print(f"Error creating trip: {e}")
            self.session.rollback()
            return None

    def get_trip(self, request_id: UUID) -> Optional[Trip]:
        try:
            trip_db = self.session.query(TripDB).filter(TripDB.id == request_id).first()
            if trip_db:
                return Trip(
                    id=trip_db.id,
                    ride_route_id=trip_db.ride_route_id,
                    passenger_id=trip_db.passenger_id,
                    pickup_request_location_name=trip_db.pickup_request_location_name,
                    pickup_time=trip_db.pickup_time,
                    is_approved=trip_db.is_approved
                )
            return None
        except Exception as e:
            print(f"Error getting trip: {e}")
            return None

    def find_trips(
        self,
        ride_route_id: Optional[UUID] = None,
        passenger_id: Optional[UUID] = None,
        is_approved: Optional[bool] = None,
    ) -> List[Trip]:
        try:
            query = self.session.query(TripDB)
            
            if ride_route_id:
                query = query.filter(TripDB.ride_route_id == ride_route_id)
            if passenger_id:
                query = query.filter(TripDB.passenger_id == passenger_id)
            if is_approved is not None:
                query = query.filter(TripDB.is_approved == is_approved)

            trips_db = query.all()
            return [Trip(
                id=trip.id,
                ride_route_id=trip.ride_route_id,
                passenger_id=trip.passenger_id,
                pickup_request_location_name=trip.pickup_request_location_name,
                pickup_time=trip.pickup_time,
                is_approved=trip.is_approved
            ) for trip in trips_db]
        except Exception as e:
            print(f"Error finding trips: {e}")
            return []

    def approve_trip(self, request_id: UUID) -> Optional[Trip]:
        try:
            trip_db = self.session.query(TripDB).filter(TripDB.id == request_id).first()
            if trip_db:
                trip_db.is_approved = True
                self.session.commit()
                self.session.refresh(trip_db)
                
                return Trip(
                    id=trip_db.id,
                    ride_route_id=trip_db.ride_route_id,
                    passenger_id=trip_db.passenger_id,
                    pickup_request_location_name=trip_db.pickup_request_location_name,
                    pickup_time=trip_db.pickup_time,
                    is_approved=trip_db.is_approved
                )
            return None
        except Exception as e:
            print(f"Error approving trip: {e}")
            self.session.rollback()
            return None

    # def create_passenger_route(self, route: PassengerRoute) -> Route:
    #     try:
    #         route_db = RouteDB(
    #             id=route.id,
    #             departure_location_name=route.departure_location_name,
    #             departure_time=route.departure_time,
    #             destination_location_name=route.destination_location_name,
    #             passenger_name=route.passenger_name,
    #             passenger_contact_info=route.passenger_contact_info
    #         )
    #         self.session.add(route_db)
    #         self.session.commit()
    #         self.session.refresh(route_db)

    #         passenger_route : Route = Route(
    #             id=route_db.id,
    #             departure_location_name=route_db.departure_location_name,
    #             departure_time=route_db.departure_time,
    #             destination_location_name=route_db.destination_location_name,
    #             passenger_name=route_db.passenger_name,
    #             passenger_contact_info=route_db.passenger_contact_info,
    #             created_at=route_db.created_at,
    #             updated_at=route_db.updated_at
    #         )
    #         return passenger_route
    #     except Exception as e:
    #         print(f"Error creating passenger route: {e}")
    #         self.session.rollback()
    #         return None
        
    # def involve_driver_to_route(self, route_id: UUID, route: RequestInvolveDriverToRoute) -> Optional[Route]:
    #     try:
    #         route_db = self.session.query(RouteDB).filter(RouteDB.id == route_id).first()
    #         if route_db is not None:
    #             route_db.driver_id = route.driver_id
    #             route_db.car_plate_number = route.car_plate_number
    #             route_db.driver_name = route.driver_name
    #             route_db.driver_contact_info = route.driver_contact_info
    #             route_db.confirm_onboard = True

    #             self.session.commit()
    #             self.session.refresh(route_db)
                
    #             return Route.model_validate(route_db)
    #         return None
    #     except Exception as e:
    #         print(f"Error involving driver to route: {e}")
    #         self.session.rollback()
    #         return None
    
    def find_passenger(self, passenger_id: str):

        try:
            passenger_db:PassengerDB = self.session.query(PassengerDB).filter(PassengerDB.id == passenger_id).first()
            return Passenger.model_validate(passenger_db)
        except Exception as e:
            print(f"Error create passenger:{e}")
            self.session.rollback()
            return None