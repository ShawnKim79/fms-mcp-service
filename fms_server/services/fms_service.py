import asyncpg
from uuid import UUID
from datetime import datetime
from typing import Optional, List

from domains.passenger import Passenger
from domains.route import Route
from domains.trip import trip as RideRequest

DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "user"
DB_PASSWORD = "password"
DB_NAME = "fms"

class FmsService:
    def __init__(self):
        self.pool = None

    async def connect_db(self):
        self.pool = await asyncpg.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )

    async def close_db(self):
        if self.pool:
            await self.pool.close()

    async def create_passenger(self, passenger: Passenger) -> Passenger:
        async with self.pool.acquire() as conn:
            query = "INSERT INTO passengers (id, name, contact_info) VALUES ($1, $2, $3) RETURNING id"
            passenger.id = await conn.fetchval(query, passenger.id, passenger.name, passenger.contact_info)
            return passenger

    async def create_ride_route(self, route: Route) -> Route:
        async with self.pool.acquire() as conn:
            query = "INSERT INTO ride_routes (id, driver_id, car_plate_number, departure_location_name, departure_time, destination_location_name) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id"
            route.id = await conn.fetchval(query, route.id, route.driver_id, route.car_plate_number, route.departure_location_name, route.departure_time, route.destination_location_name)
            return route

    async def get_ride_route(self, route_id: UUID) -> Optional[Route]:
        async with self.pool.acquire() as conn:
            query = "SELECT id, driver_id, car_plate_number, departure_location_name, departure_time, destination_location_name FROM ride_routes WHERE id = $1"
            row = await conn.fetchrow(query, route_id)
            if row:
                return Route(**row)
            return None

    async def find_ride_routes(
        self,
        driver_id: Optional[UUID] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        departure_location_name: Optional[str] = None,
        destination_location_name: Optional[str] = None,
    ) -> List[Route]:
        async with self.pool.acquire() as conn:
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

            rows = await conn.fetch(query)
            return [Route(**row) for row in rows]

    async def update_ride_route(self, route_id: UUID, route: Route) -> Optional[Route]:
        async with self.pool.acquire() as conn:
            query = "UPDATE ride_routes SET car_plate_number = $1, departure_location_name = $2, departure_time = $3, destination_location_name = $4 WHERE id = $5 RETURNING id, driver_id, car_plate_number, departure_location_name, departure_time, destination_location_name"
            row = await conn.fetchrow(query, route.car_plate_number, route.departure_location_name, route.departure_time, route.destination_location_name, route_id)
            if row:
                return Route(**row)
            return None

    async def delete_ride_route(self, route_id: UUID):
        async with self.pool.acquire() as conn:
            query = "DELETE FROM ride_routes WHERE id = $1"
            await conn.execute(query, route_id)

    async def create_ride_request(self, ride_request: RideRequest) -> RideRequest:
        async with self.pool.acquire() as conn:
            query = "INSERT INTO ride_requests (id, ride_route_id, passenger_id, pickup_request_location_name, pickup_time, is_approved) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id"
            ride_request.id = await conn.fetchval(query, ride_request.id, ride_request.ride_route_id, ride_request.passenger_id, ride_request.pickup_request_location_name, ride_request.pickup_time, ride_request.is_approved)
            return ride_request

    async def get_ride_request(self, request_id: UUID) -> Optional[RideRequest]:
        async with self.pool.acquire() as conn:
            query = "SELECT id, ride_route_id, passenger_id, pickup_request_location_name, pickup_time, is_approved FROM ride_requests WHERE id = $1"
            row = await conn.fetchrow(query, request_id)
            if row:
                return RideRequest(**row)
            return None

    async def find_ride_requests(
        self,
        ride_route_id: Optional[UUID] = None,
        passenger_id: Optional[UUID] = None,
        is_approved: Optional[bool] = None,
    ) -> List[RideRequest]:
        async with self.pool.acquire() as conn:
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

            rows = await conn.fetch(query)
            return [RideRequest(**row) for row in rows]

    async def approve_ride_request(self, request_id: UUID) -> Optional[RideRequest]:
        async with self.pool.acquire() as conn:
            query = "UPDATE ride_requests SET is_approved = TRUE WHERE id = $1 RETURNING id, ride_route_id, passenger_id, pickup_request_location_name, pickup_time, is_approved"
            row = await conn.fetchrow(query, request_id)
            if row:
                return RideRequest(**row)
            return None
