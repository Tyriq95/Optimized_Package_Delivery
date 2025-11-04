import datetime

class Package:
    # Package constructor
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.truck = None
        self.departure_time = None
        # Sets temp value for interface without altering actual package data
        self.temp_departure_time = self.departure_time
        self.delivery_time = None
        # Sets temp value for interface without altering actual package data
        self.temp_delivery_time = self.delivery_time
        self.original_address = address

    # Method to update the various data of the packages in order to provide accurate data
    # when entering times in the user interface.
    def update_status(self, time_conversion, truck):
        self.truck = truck
        # Changes the address output for package 9 according to the time that is entered by the user
        if self.package_id == 9 and time_conversion < datetime.timedelta(hours=10, minutes=20):
            self.address = self.original_address
            self.zip_code = '84103'
        elif self.package_id == 9 and time_conversion >= datetime.timedelta(hours=10, minutes=20):
            self.address = '410 S State St'
            self.zip_code = '84111'

        # Sets the status of the package based on details in project documentation, package departure time,
        # package delivery time, and time entered by the user
        if self.package_id in (6, 25, 28, 32) and time_conversion < datetime.timedelta(hours=9, minutes=5):
            self.status = "Delayed"
        elif self.delivery_time is not None and time_conversion >= self.delivery_time:
            self.status = "Delivered"
        elif self.departure_time is not None and self.departure_time <= time_conversion < self.delivery_time:
            self.status = "En Route"
        elif self.departure_time is not None and time_conversion < self.departure_time:
            self.status = "At Hub"

        # Sets delivery time to none (for interface use) if the time entered by the user is less than the
        # packages actual delivery time
        if self.delivery_time and time_conversion < self.delivery_time:
            self.temp_delivery_time = None
        else:
            self.temp_delivery_time = self.delivery_time

        # Sets departure time to none (for interface use) if the time entered by the user is less than the
        # packages actual departure time
        if self.departure_time and time_conversion < self.departure_time:
            self.temp_departure_time = None
        else:
            self.temp_departure_time = self.departure_time

    def __str__(self):
        return f"\nPackage ID: {self.package_id}\nDelivery Address: {self.address}, {self.city}, {self.state} {self.zip_code}\nDelivery Deadline: {self.deadline}\nPackage Weight: {self.weight}\nTruck: {self.truck}\nDeparture Time: {self.temp_departure_time}\nDelivery Time: {self.temp_delivery_time}\nStatus: {self.status}\n"

    def __repr__(self):
        return f"\nPackage ID: {self.package_id}\n Delivery Address: {self.address}, {self.city}, {self.state} {self.zip_code}\n Delivery Deadline: {self.deadline}\n Package Weight: {self.weight}\n Truck: {self.truck}\n Departure Time: {self.temp_departure_time}\n Delivery Time: {self.temp_delivery_time}\n Status: {self.status}\n"