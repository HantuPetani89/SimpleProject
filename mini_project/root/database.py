import sqlite3

class Database:
    def __init__(self, db_path="tanaman.db"):
        self.db_path = db_path

    def buatTabelTanaman(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS plants (
                    id_tree INTEGER PRIMARY KEY,
                    latitude REAL,
                    longitude REAL,
                    added_timestamp TEXT
                )
            ''')
            conn.commit()
            print("Plants table created or verified successfully.")

    def buatTabelSensorData(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id_tree INTEGER,
                    sensors INTEGER,
                    value REAL,
                    time TEXT,
                    PRIMARY KEY (id_tree, sensors, time)
                )
            ''')
            conn.commit()
            print("Sensor data table created or verified successfully.")

    def ambil_semua_id_tree(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT DISTINCT id_tree FROM plants")
            id_trees = c.fetchall()
            print(f"Retrieved all ID trees: {id_trees}")
            return id_trees
    
    def ambil_semua_data_sensor(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM plants")
            plants = c.fetchall()
            print(f"Retrieved all plants data: {plants}")
            return plants

if __name__ == "__main__":
    db = Database()