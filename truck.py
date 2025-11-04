import datetime


class Truck:
    # Truck constructor
    def __init__ (self, packages):
        self.max_capacity = 16 # Given in the project requirements
        self.avg_speed = 18 # Given in the project requirements
        self.packages = packages
        self.miles = 0
        self.current_location = "4001 South 700 East" #Starts at the hub
        self.next_location = ''
        self.departure_time = datetime.timedelta(0)
        self.total_time = datetime.timedelta(0)

    def __str__(self):
        return f"{self.packages},{self.miles},{self.departure_time},{self.current_location},{self.next_location}"

    def __repr__(self):
        return f"{self.packages},{self.miles},{self.departure_time},{self.current_location},{self.next_location}"
