class Nodo:
    def __init__(self, row):
        self.name = row[0]
        self.mac_address = row[1]
        self.sleep_mesh = row[2]
        self.active = row[3]

class Gateway:
    def __init__(self, row):
        self.name = row[0]
        self.debug = row[1]
        self.mesh_mode = row[2]
        self.chunk_size = row[3]
        self.frecuency = row[4]
        self.sf = row[5]
        self.min_timeout = row[6]
        self.max_timeout = row[7]
        self.state = row[8]