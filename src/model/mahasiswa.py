class Mahasiswa:
    def __init__(self, npm, name):
        self.npm = npm
        self.name = name

    def __lt__ (self, other):
        if self.npm == other.npm:
            return self.name < other.name

        return self.npm < other.npm

    def __gt__(self, other):
        if self.npm == other.npm:
            return self.name > other.name

        return self.npm > other.npm

    def __eq__(self, other):
        return self.npm == other.npm