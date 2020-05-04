class Server:
    def __init__(self, role):
        self.absentee = {} # Dictionary of user
        self.timer = None # Timer object

        self.role = role # Role object to be mentioned

    def add_absentee(self, id, mahasiswa):
        self.absentee[id] = mahasiswa

    def has_absentee(self, id):
        return id in self.absentee 

    def get_absentees(self):
        return self.absentee

    def start_absen(self, timer):
        self.timer = timer

        self.absentee.clear()
        self.timer.start()

    def stop_absen(self):        
        self.timer.cancel()
        self.timer = None
        
        return self.absentee