# Name: Tyriq Williams
# C950 - Data Structures and Algorithms II
# Performance Assessment Task 2

from hashmap import HashMap
from package import Package
from truck import Truck
import csv
import datetime

package_map = HashMap() # Creates a new hash map object
dist_dictionary = {} # Creates an empty dictionary for distance values. NOT USED FOR HASHMAP

# Reads the package file, creates a new package object for each package, and adds that
# package object to the hash map
with open("WGUPS Package File.csv", encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        # sets the status as either delayed or at hub for each package object
        if int(row[0]) in (6,25,28,32):
            status = "Delayed"
        else:
            status = "At Hub"
        package = Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], status)
        package_map.add(package.package_id-1, package)

# Opens the distance table and travers each row and column to get headers.
# Those headers are saved as current_address and next_address.
with open("WGUPS Distance Table.csv", newline='') as f:

    reader = csv.reader(f)
    headers = next(reader)
    #distance_csv = list(reader)
    for row in reader:
        current_address = row[0]
        for i in range(1, len(row)):
            next_address = headers[i]
            value = row[i]

            # if the value is not empty gets the distance value for x and y (or y and x) coordinates
            # using the address row and column headers.
            if value != '':
                dist_value = float(row[i])
                dist_dictionary[(current_address, next_address)] = dist_value
                dist_dictionary[(next_address, current_address)] = dist_value

# Calculates the distance using the values stored in the dictionary that was filled
# when reading the distance table CSV file
def distance(current_addr, next_addr):
    return dist_dictionary[(current_addr, next_addr)]

# User interface function that prompts the user for the time, and asks for a
# specific package or to show all packages
def interface():
    terminate = False # Boolean to terminate the program

    while not terminate:
        try:
            #  Received the users desired time as a string, or exit to exit the interface
            user_time_input = input("Please enter a time to see status of packages of that time. Format - HH:MM:SS.\n" +
                                    "Type \"exit\" when finished to close the interface.\n")

            # Parses the user time input and separates into hours, minutes, and seconds
            (h, m, s) = user_time_input.split(":")

            # Saves the int values of hours, minutes, seconds into a variable
            time_conversion = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            # Prompts the user for either a specific package, or to show all packages
            user_selection = input("Please enter a package ID between 1 and 40 to see the status of a single package, " +
                                   "or enter \"all\" to see the status of all packages at the entered time.\n")
            try:
                # Executes if user enters a valid time, and user also enters all
                if user_selection.lower() == "all":
                    # Stores the applicable truck for each package
                    for package_id in range(1,41):
                        if package_id in truck1.packages:
                            truck = "Truck 1"
                        elif package_id in truck2.packages:
                            truck = "Truck 2"
                        else:
                            truck = "Truck 3"
                        pkg = package_map.get(package_id)
                        # Passes users entered time and applicable truck as parameters for update_status method
                        # and prints accurate package information for that entered time
                        pkg.update_status(time_conversion, truck)
                        print(package_map.get(package_id))
                else:
                    # does the same as above, except for one specific package only
                    package_id = int(user_selection)
                    if package_id in truck1.packages:
                        truck = "Truck 1"
                    elif package_id in truck2.packages:
                        truck = "Truck 2"
                    else:
                        truck = "Truck 3"
                    try:
                        pkg = package_map.get(package_id)
                        pkg.update_status(time_conversion, truck)
                        print(package_map.get(package_id))
                    # Throws these exceptions if package ID entered is not between 1 and 40
                    except IndexError:
                        print("Value entered is not between 1 and 40. Please enter \"all\" or a value "
                              "between 1 and 40\n")
                    except AttributeError:
                        print("Value entered is not between 1 and 40. Please enter \"all\" or a value "
                              "between 1 and 40\n")
            # Prints if value is not a package ID or all
            except ValueError:
                print("Invalid entry, please enter the package ID or all to see delivery information.\n")

        # Executes if the user input is not HH:MM:SS format
        except ValueError:
            try:
                # If exit is entered, total truck mileage is printed and terminate is set to true
                if user_time_input.lower() == "exit":
                    print("\nTotal miles after all packages have been delivered:\n" +
                          f"Truck 1: {round(truck1.miles, 2)}\n" +
                          f"Truck 2: {round(truck2.miles, 2)}\n" +
                          f"Truck 3: {round(truck3.miles, 2)}\n" +
                          f"Total: {round(truck1.miles + truck2.miles + truck3.miles, 3)}")
                    terminate = True
                    break
                else:
                    # Prints if input is not exit
                    print("Invalid entry, please use the format HH:MM:SS or type exit.\n")
            # Prints if input is not exit or follow the HH:MM:SS format, continues the loop
            except ValueError:
                print("Invalid entry, please use the format HH:MM:SS or type exit.\n")
                continue

def deliver_packages(truck):
    # creates a copy of the values in truck.packages
    pending = truck.packages.copy()
    truck.packages.clear() # clears values from truck.packages
    truck.total_time = datetime.timedelta(0)
    reroute_applied = False

    # executes while pending still has package IDs
    while pending:
        # Re-routes package 9 to the correct address after 10:20
        if (
            truck is truck3 and
            not reroute_applied and
            (truck.departure_time + truck.total_time) > datetime.timedelta(hours=10, minutes=20) and
            9 in pending
        ):
            package_map.get(9).address = '410 S State St'
            package_map.get(9).zip_code = '84111'
            reroute_applied = True
            continue
        # Ensures package 9 address is the original address before 10:20
        elif(
            truck is truck3 and
            not reroute_applied and
            (truck.departure_time + truck.total_time) < datetime.timedelta(hours=10, minutes=20) and
            9 in pending
        ):
            package_map.get(9).address = '300 State St'
            package_map.get(9).zip_code = '84103'
            reroute_applied = False


        next_distance = float('inf') # Sets next_distance to infinity float
        closest_package = None

        # Nearest neighbor algorithm
        for pkg_id in pending:
            dist = distance(truck.current_location, package_map.get(pkg_id).address)
            # replaces the closest package one is found with a shorter distance
            if dist < next_distance:
                next_distance = dist
                closest_package = pkg_id
        # Adds the closest package back to the list of truck packages
        truck.packages.append(closest_package)
        # Sets the trucks current location to the location of the next package to "deliver" it
        truck.current_location = package_map.get(closest_package).address
        # removes the closest package so it is not considered in the next iteration
        pending.remove(closest_package)

        # Adds the traveled distance to the truck's miles counter
        truck.miles += next_distance
        # Sets the trucks next location
        truck.next_location = package_map.get(closest_package).address
        # Calculates the time it to took to travel to the package, and add it to elapsed time
        truck.total_time += datetime.timedelta(hours=next_distance / truck.avg_speed)

        # Updates the packages departure and delivery time
        pkg = package_map.get(closest_package)
        pkg.departure_time = truck.departure_time
        pkg.delivery_time = truck.departure_time + truck.total_time

    # Returns the truck to the hub and also accounts for the time and miles to do so
    truck.next_location = "4001 South 700 East"
    return_dist = distance(truck.current_location, truck.next_location)
    truck.miles += return_dist
    truck.total_time += datetime.timedelta(hours=return_dist / truck.avg_speed)
    truck.current_location = truck.next_location


# Manually loads packages onto each truck
truck1 = Truck([1,13,14,15,16,19,20,29,30,31,34,37,40])
truck1.departure_time = datetime.timedelta(hours=8) # Departure time for Truck 1
truck2 = Truck([3,6,18,25,27,28,32,33,35,36,38,39])
truck2.departure_time = datetime.timedelta(hours=9,minutes=5) # Departure time for Truck 2
truck3 = Truck([2,4,5,7,8,9,10,11,12,17,21,22,23,24,26])

deliver_packages(truck1) # Deliver Truck 1 packages
deliver_packages(truck2) # Deliver Truck 2 packages

# Deliver Truck 3 packages once the driver of Truck 1 returns
truck3.departure_time = (truck1.departure_time + truck1.total_time)
deliver_packages(truck3)

#Start the user interface in order to perform package lookup
interface()