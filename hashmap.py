class HashMap:
    # Constructor
    def __init__(self):
        self.size = 40
        self.map = [None] * self.size

    # Adds as well as updates values (package details) when passed the key (Package ID)
    def add(self, key, value):
        key_value = [key,value]
        # If there is no key matching the key parameter, creates one and creates a list for package values
        if self.map[key] is None:
            self.map[key] = list([key_value])
            return True
        # If key exists, navigates to the value for that key and enters what was passed in the value method parameter
        else:
            for pair in self.map[key]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key].append(value)
            return True

    # Retrieves the value for the corresponding key parameter that is passed in.
    def get(self, key):
        key -= 1 # In order to get applicable package data that is meant by the user
        if self.map[key] is not None:
            for pair in self.map[key]:
                if pair[0] == key:
                    return pair[1]
        return None
    # Prints everything that is stored in the hashmap
    def print(self):
        for package in self.map:
            if package is not None:
                print(str(package))