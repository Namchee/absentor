class Server:
    def __init__(self, role):
        self.is_absen = False # State which determines if the server is receiving presence message
        self.absentee = [] # The current list of absentee ID on an absen session

        self.role = role # Role object to be mentioned

    def add_absentee(self, id):
        self.absentee.append(id)

    def start_absen(self):
        self.is_absen = True

    def stop_absen(self):
        absentee = self.absentee.copy()
        
        self.absentee.clear()
        self.is_absen = False

        return absentee