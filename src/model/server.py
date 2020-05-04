class Server:
    def __init__(self, role):
        self.absentee = [] # The current list of absentee ID on an absen session
        self.timer = None # Timer object, if 

        self.role = role # Role object to be mentioned

    def add_absentee(self, id):
        self.absentee.append(id)

    def has_absentee(self, id):
        return id in self.absentee

    def start_absen(self, timer):
        self.timer = timer

        self.absentee.clear()
        self.timer.start()

    def stop_absen(self):        
        self.timer.cancel()
        self.timer = None
        
        return self.absentee