import random
import time
import threading
import heapq
from datetime import datetime, timedelta

class Vehicle:
    def __init__(self, vehicle_id, capacity, current_location):
        self.vehicle_id = vehicle_id
        self.capacity = capacity
        self.current_location = current_location
        self.route = []
        self.current_load = 0

    def move_to(self, location):
        self.current_location = location

    def __str__(self):
        return f"Vehicle {self.vehicle_id}: Location {self.current_location}, Load {self.current_load}/{self.capacity}"

class DeliveryRoute:
    def __init__(self, start_location, end_location, distance, deadline, traffic_factor=1.0):
        self.start_location = start_location
        self.end_location = end_location
        self.distance = distance
        self.deadline = deadline
        self.traffic_factor = traffic_factor

    def get_travel_time(self):
        return self.distance * self.traffic_factor

class LogisticsSimulation:
    def __init__(self):
        self.vehicles = []
        self.routes = []
        self.simulation_running = False
        self.simulation_lock = threading.Lock()
        self.current_time = datetime.now()

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def add_route(self, route):
        heapq.heappush(self.routes, (route.deadline, route))

    def optimize_routes(self):
        # This is a simple optimization by deadline and distance.
        # In practice, this can be replaced with more sophisticated algorithms like Dijkstra's or A*.
        self.routes.sort(key=lambda x: (x[1].deadline, x[1].get_travel_time()))

    def simulate_movement(self):
        while self.simulation_running:
            with self.simulation_lock:
                self.current_time += timedelta(minutes=1)
                for vehicle in self.vehicles:
                    if vehicle.route:
                        route = vehicle.route[0]
                        travel_time = route.get_travel_time()
                        if travel_time <= 0:
                            vehicle.move_to(route.end_location)
                            vehicle.route.pop(0)
                        else:
                            route.distance -= 1  # Simulate movement
                            route.traffic_factor -= 0.01  # Simulate traffic change
                self.generate_reports()
            time.sleep(1)  # Simulate real-time by waiting

    def start_simulation(self):
        self.simulation_running = True
        self.simulation_thread = threading.Thread(target=self.simulate_movement)
        self.simulation_thread.start()

    def pause_simulation(self):
        self.simulation_running = False
        self.simulation_thread.join()

    def stop_simulation(self):
        self.simulation_running = False
        self.simulation_thread.join()
        with self.simulation_lock:
            self.current_time = datetime.now()
            for vehicle in self.vehicles:
                vehicle.route = []

    def generate_reports(self):
        print("\nSimulation Time:", self.current_time)
        for vehicle in self.vehicles:
            print(vehicle)
            if vehicle.route:
                print(f"  Next destination: {vehicle.route[0].end_location}, Distance: {vehicle.route[0].distance}, Traffic: {vehicle.route[0].traffic_factor:.2f}")
        print()

    def add_delivery_to_vehicle(self, vehicle_id, route):
        vehicle = next((v for v in self.vehicles if v.vehicle_id == vehicle_id), None)
        if vehicle:
            vehicle.route.append(route)

# Example usage
if __name__ == "__main__":
    sim = LogisticsSimulation()
    v1 = Vehicle("V1", 100, "Warehouse A")
    v2 = Vehicle("V2", 80, "Warehouse B")

    sim.add_vehicle(v1)
    sim.add_vehicle(v2)

    r1 = DeliveryRoute("Warehouse A", "Customer 1", 10, datetime.now() + timedelta(hours=1))
    r2 = DeliveryRoute("Warehouse B", "Customer 2", 15, datetime.now() + timedelta(hours=2), traffic_factor=1.2)

    sim.add_delivery_to_vehicle("V1", r1)
    sim.add_delivery_to_vehicle("V2", r2)

    sim.start_simulation()

    # Let the simulation run for a while
    time.sleep(10)
    sim.pause_simulation()

    sim.generate_reports()

    sim.stop_simulation()
