import os
import psycopg2
from uuid import UUID
from datetime import datetime
from typing import Optional, List

from app.domains.passenger import Passenger
from app.domains.route import Route
from app.domains.trip import trip as RideRequest

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_NAME = os.environ.get("DB_NAME", "fms")

class FmsService:
    def __init__(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                dbname=DB_NAME,
            )
            print("Connected to PostgreSQL")
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def __del__(self):
        if self.conn:
            self.conn.close()
            print("Disconnected from PostgreSQL")

    def create_passenger(self, passenger: Passenger) -> Passenger:
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO passengers (id, name, contact_info) VALUES (%s, %s, %s) RETURNING id"
            cursor.execute(query, (passenger.id, passenger.name, passenger.contact_info))
            passenger.id = cursor.fetchone()[0]
            self.conn.commit()
            cursor.close()
            return passenger
        except psycopg2.Error as e:
            print(f"Error creating passenger: {e}")
            return None

    def create_ride_route(self, route: Route) -> Route:
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO ride_routes (id, driver_id, car_plate_number, departure_location_name, departure_time, destination_location_name) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
            cursor.execute(query, (route.id, route.driver_id, route.car_plate_number, route.departure_location_name, route.departure_time, route.destination_location_name))
            route.id = cursor.fetchone()[0]
            self.conn.commit()
            cursor.close()
            return route
        except psycopg2.Error as e:
            print(f"Error creating ride route: {e}")
            return None

    def get_ride_route(self, route_id: UUID) -> Optional[Route]:
        try:
            cursor = self.conn.cursor()
            query = "SELECT id, driver_id, car_plate_number, departure_location_name, departure_time, destination_location_name FROM ride_routes WHERE id = %s"
            cursor.execute(query, (route_id,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return Route(**{
                    "id": row[0],
                    "driver_id": row[1],
                    "car_plate_number": row[2],
                    "departure_location_name": row[3],
                    "departure_time": row[4],
                    "destination_location_name": row[5]
                })
            return None
        except psycopg2.Error as e:
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
            cursor = self.conn.cursor()
            query = "SELECT id, driver_id, car_plate_number, departure_location_name, departure_time, destination_location_name FROM ride_routes WHERE TRUE"
            conditions = []
            if driver_id:
                conditions.append(f"driver_id = '{driver_id}'")
            if start_time:
                conditions.append(f"departure_time >= '{start_time}'")
            if end_time:
                conditions.append(f"departure_time <= '{end_time}'")
            if departure_location_name:
                conditions.append(f"departure_location_name = '{departure_location_name}'")
            if destination_location_name:
                conditions.append(f"destination_location_name = '{destination_location_name}'")

            if conditions:
                query += " AND " + " AND ".join(conditions)

            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [Route(**{
                    "id": row[0],
                    "driver_id": row[1],
                    "car_plate_number": row[2],
                    "departure_location_name": row[3],
                    "departure_time": row[4],
                    "destination_location_name": row[5]
                }) for row in rows]
        except psycopg2.Error as e:
            print(f"Error finding ride routes: {e}")
            return []

    def update_ride_route(self, route_id: UUID, route: Route) -> Optional[Route]:
        try:
            cursor = self.conn.cursor()
            query = "UPDATE ride_routes SET car_plate_number = %s, departure_location_name = %s, departure_time = %s, destination_location_name = %s WHERE id = %s RETURNING id, driver_id, car_plate_number, departure_location_name, departure_time, destination_location_name"
            cursor.execute(query, (route.car_plate_number, route.departure_location_name, route.departure_time, route.destination_location_name, route_id))
            row = cursor.fetchone()
            self.conn.commit()
            cursor.close()
            if row:
                return Route(**{
                    "id": row[0],
                    "driver_id": row[1],
                    "car_plate_number": row[2],
                    "departure_location_name": row[3],
                    "departure_time": row[4],
                    "destination_location_name": row[5]
                })
            return None
        except psycopg2.Error as e:
            print(f"Error updating ride route: {e}")
            return None

    def delete_ride_route(self, route_id: UUID):
        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM ride_routes WHERE id = %s"
            cursor.execute(query, (route_id,))
            self.conn.commit()
            cursor.close()
        except psycopg2.Error as e:
            print(f"Error deleting ride route: {e}")

    def create_ride_request(self, ride_request: RideRequest) -> RideRequest:
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO ride_requests (id, ride_route_id, passenger_id, pickup_request_location_name, pickup_time, is_approved) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
            cursor.execute(query, (ride_request.id, ride_request.ride_route_id, ride_request.passenger_id, ride_request.pickup_request_location_name, ride_request.pickup_time, ride_request.is_approved))
            ride_request.id = cursor.fetchone()[0]
            self.conn.commit()
            cursor.close()
            return ride_request
        except psycopg2.Error as e:
            print(f"Error creating ride request: {e}")
            return None

    def get_ride_request(self, request_id: UUID) -> Optional[RideRequest]:
        try:
            cursor = self.conn.cursor()
            query = "SELECT id, ride_route_id, passenger_id, pickup_request_location_name, pickup_time, is_approved FROM ride_requests WHERE id = %s"
            cursor.execute(query, (request_id,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return RideRequest(**{
                    "id": row[0],
                    "ride_route_id": row[1],
                    "passenger_id": row[2],
                    "pickup_request_location_name": row[3],
                    "pickup_time": row[4],
                    "is_approved": row[5]
                })
            return None
        except psycopg2.Error as e:
            print(f"Error getting ride request: {e}")
            return None

    def find_ride_requests(
        self,
        ride_route_id: Optional[UUID] = None,
        passenger_id: Optional[UUID] = None,
        is_approved: Optional[bool] = None,
    ) -> List[RideRequest]:
        try:
            cursor = self.conn.cursor()
            query = "SELECT id, ride_route_id, passenger_id, pickup_request_location_name, pickup_time, is_approved FROM ride_requests WHERE TRUE"
            conditions = []
            if ride_route_id:
                conditions.append(f"ride_route_id = '{ride_route_id}'")
            if passenger_id:
                conditions.append(f"passenger_id = '{passenger_id}'")
            if is_approved is not None:
                conditions.append(f"is_approved = {is_approved}")

            if conditions:
                query += " AND " + " AND ".join(conditions)

            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [RideRequest(**{
                    "id": row[0],
                    "ride_route_id": row[1],
                    "passenger_id": row[2],
                    "pickup_request_location_name": row[3],
                    "pickup_time": row[4],
                    "is_approved": row[5]
                }) for row in rows]
        except psycopg2.Error as e:
            print(f"Error finding ride requests: {e}")
            return []

    def approve_ride_request(self, request_id: UUID) -> Optional[RideRequest]:
        try:
            cursor = self.conn.cursor()
            query = "UPDATE ride_requests SET is_approved = TRUE WHERE id = %s RETURNING id, ride_route_id, passenger_id, pickup_request_location_name, pickup_time, is_approved"
            cursor.execute(query, (request_id,))
            row = cursor.fetchone()
            self.conn.commit()
            cursor.close()
            if row:
                return RideRequest(**{
                    "id": row[0],
                    "ride_route_id": row[1],
                    "passenger_id": row[2],
                    "pickup_request_location_name": row[3],
                    "pickup_time": row[4],
                    "is_approved": row[5]
                })
            return None
        except psycopg2.Error as e:
            print(f"Error approving ride request: {e}")
            return None
