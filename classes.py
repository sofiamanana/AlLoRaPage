class Nodo:
    def __init__(self, row):
        self.name = row[0]
        self.mac_address = row[1]
        self.sleep_mesh = row[2]
        self.active = row[3]
        self.listening_time = row[4]

class Gateway:
    def __init__(self, row):
        self.name = row[0]
        self.debug = row[1]
        self.mesh_mode = row[2]
        self.chunk_size = row[3]
        self.result_path = row[4]
        self.frecuency = row[5]
        self.sf = row[6]
        self.min_timeout = row[7]
        self.max_timeout = row[8]
        self.serial_port = row[9]
        self.baud = row[10]
        self.timeout = row[11]
        self.state = row[12]