class Server:
    def __init__(self, role):
        self.is_absen = False  # State which determines if the server is receiving presence message
        self.absentee = {}  # The current list of absentee ID on an absen session

        self.role = role # Role object to be mentioned

    def add_absentee(self,key, id):
        self.absentee[key] = id

    def get_absentee(self):
        return self.absentee

    def already_absent(self,key):
        if key in self.absentee:
            return True

        return False

    def delete_entry(self, key):
        del self.absentee[key]

    def get_absentee_value(self):
        return self.absentee.values()

    def start_absen(self):
        self.is_absen = True

    def stop_absen(self):
        absentee = self.absentee.copy()
        
        self.absentee.clear()
        self.is_absen = False

        return absentee