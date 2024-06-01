import json
from urllib.request import urlopen
import time
from threading import Thread
from root.database import Database 
import sqlite3
import datetime as dt
import random
import numpy as np
import matplotlib.dates as mdates

class Getdata:
    def __init__(self):
        self.sensors = []
    
    # Simpan data
    def fetchdata(self, id_tree):
        for sensor in range(10):
            try:
                link = f"https://belajar-python-unsyiah.an.r.appspot.com/sensor/read?npm=2304111010073&id_tree={id_tree}&sensor_type={sensor}"
                print(f"Mengambil data dari {link}")
                url = urlopen(link)
                document = url.read().decode("utf-8")
                data = json.loads(document)
                
                waktu_str = data.get("when")
                tipe_sensor = data.get("sensor_type")
                nilai = data.get("value")
                
                waktu = dt.datetime.strptime(waktu_str, "%a, %d %b %Y %H:%M:%S %Z")
                local = dt.timedelta(hours=7)
                adjusted_time = waktu + local
                
                data = {
                    "id_tree": id_tree,
                    "sensor_type": tipe_sensor,
                    "value": nilai,
                    "time": adjusted_time
                }
                self.sensors.append(data)
                print(f"Data fetched: {data}")
                self.simpan_datadb(data)
            except Exception as e:
                print(f"Gagal menyimpan atau mengambil data untuk {sensor} dan tree {id_tree}: {e}")
        return self.sensors
    
    # Fungsi simpan data ke database
    def simpan_datadb(self, data):
        try:
            with sqlite3.connect("database.db") as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO sensor_data (id_tree, sensors, value, time)
                    VALUES (?, ?, ?, ?)
                ''', (data["id_tree"], data["sensor_type"], data["value"], data["time"]))
                conn.commit()
                print(f"Data tersimpan di database: {data}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Gagal menyimpan data: {e}")
    
    # Fungsi ambil data secara berkala
    def ambil_data(self):
        def getdata_periodic():
            while True:
                try:
                    db = Database()
                    id_trees = db.get_all_id_trees()
                    for id_tree in id_trees:
                        self.fetchdata(id_tree[0])
                    time.sleep(60)
                except Exception as e:
                    print(f"Error pada saat pengambilan data berkala: {e}")
        
        thread = Thread(target=getdata_periodic)
        thread.daemon = True
        thread.start()

# class KoneksiDatabase
class KoneksiDatabase:
    def __enter__(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

# Class CRUD (Create, Read, Update, Delete)
class PROSES:
    def __init__(self):
        pass

    def ada_id_tree(self, id_tree):
        with KoneksiDatabase() as cursor:
            cursor.execute('SELECT 1 FROM plants WHERE id_tree = ?', (id_tree,))
            return cursor.fetchone() is not None

    def tambah_id(self, id_tree):
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)
        waktu = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with KoneksiDatabase() as cursor:
            cursor.execute('''
                INSERT INTO plants (id_tree, latitude, longitude, added_timestamp)
                VALUES (?, ?, ?, ?)
            ''', (id_tree, lat, lon, waktu))

    def tampilkanSensor(self):
        with KoneksiDatabase() as cursor:
            cursor.execute('SELECT id_tree, sensors, value, time FROM sensor_data')
            return cursor.fetchall()

    def tampilkanTanaman(self):
        with KoneksiDatabase() as cursor:
            cursor.execute('SELECT id_tree, latitude, longitude, added_timestamp FROM plants')
            return cursor.fetchall()

    def hapusId(self, id_tree):
        with KoneksiDatabase() as cursor:
            cursor.execute('DELETE FROM plants WHERE id_tree = ?', (id_tree,))
            cursor.execute('DELETE FROM sensor_data WHERE id_tree = ?', (id_tree,))

class Data4Grafik:
    def __init__(self):
        pass

    def ambil_avg_sensor(self, waktu_mulai, waktu_akhir):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        data_rata_rata = {i: None for i in range(10)}  # Inisialisasi dictionary dengan 10 sensor

        cursor.execute('''
        SELECT sensors, AVG(value)
        FROM sensor_data
        WHERE time BETWEEN ? AND ?
        GROUP BY sensors
        ''', (waktu_mulai, waktu_akhir))

        baris_baris = cursor.fetchall()
        for baris in baris_baris:
            sensor_type, avg_nilai = baris
            data_rata_rata[sensor_type] = avg_nilai

        conn.close()
        return data_rata_rata
    
    def ambil_data_sensor(self, id_tree, sensor_type, waktu_mulai, waktu_akhir):
        print(f"Mengambil data dari {waktu_mulai} hingga {waktu_akhir}")

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT value, time
        FROM sensor_data
        WHERE id_tree = ? AND sensors = ? AND time BETWEEN ? AND ?
        ORDER BY time
        ''', (id_tree, sensor_type, waktu_mulai, waktu_akhir))
        data = cursor.fetchall()
        conn.close()
        print(f"Data yang ditemukan: {data}")
        return data
    
if __name__ == "__main__":
    db = Data4Grafik()
    data = db.ambil_data_sensor(1, 0, "2024-05-28 00:00:00", "2024-05-29 23:59:59")
    print(data)
