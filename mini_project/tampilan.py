"""
The `MainApp` class is the main entry point of the application. It sets up the main window, including the title, size, and background image. The `main()` method creates the main frame and adds the title, subtitle, and a button to enter the application.

The `App` class is responsible for managing the different tabs of the application, including the `MenuTambah`, `MenuDaftar`, `MenuTampil`, and `MenuHapus` tabs.

The `Messagebox` class provides static methods for displaying different types of message boxes, such as information, error, warning, question, and checkmark messages.

The `MenuDaftar` class is responsible for displaying a list of all the plants in the database in a text box. The `load_data()` method retrieves the data from the database and updates the text box.

The `MenuTambah` class provides an interface for adding a new plant to the database. The `tambah()` method handles the logic for adding a new plant.

The `MenuTampil` class provides an interface for displaying graphs of sensor data for a single plant or the mean of all sensor data for all plants. The `satu_tanaman()` and `show_mean()` methods handle the logic for displaying the respective graphs.

The `SatuTanaman` class is a custom `CTkToplevel` window that is used to display the graph for a single plant. The `minta_id()`, `pilih_type_sensor()`, `minta_waktu()`, and `grafik_sensor()` methods handle the logic for displaying the graph.

The `meanTanaman` class is a custom `CTkToplevel` window that is used to display the mean graph for all plants. The `minta_data()` and `tampilkan_grafik()` methods handle the logic for displaying the graph.

The `MenuHapus` class provides an interface for deleting a plant from the database. The `hapus()` method handles the logic for deleting a plant.
"""

import customtkinter
from CTkMessagebox import CTkMessagebox
from ambil_data.proses import CRUD
from PIL import Image, ImageTk
import tkinter as tk
from database import Database
from ambil_data.proses import Grafik
import tkcalendar
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates


class UtamaApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x640")
        self.title("Data Sensor Collector")
        self.img1 = ImageTk.PhotoImage(Image.open("assets/image.jpg"))
        self.l1 = customtkinter.CTkLabel(master=self, image=self.img1, text="")
        self.l1.pack(padx=1, pady=1, fill="both", expand=True)
        self.main()

    def main(self):
        self.frame = customtkinter.CTkFrame(master=self.l1, corner_radius=32)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.title_label = customtkinter.CTkLabel(master=self.frame, text="Data Sensor Collector Application", corner_radius=32, height=30, font=("Arial", 30, "bold"), text_color="#ccff33")
        self.title_label.pack(padx=10, pady=30)
        self.subtitle = customtkinter.CTkLabel(master=self.frame, text="Sayidil Anam\n2304111010073", corner_radius=32, height=30, font=("Arial", 15, "bold"))
        self.subtitle.pack(padx=10, pady=10)
        self.button = customtkinter.CTkButton(master=self.frame, text="Masuk", corner_radius=32, command=self.masuk, fg_color="green", hover_color="#066839")
        self.button.pack(padx=10, pady=100)

    def masuk(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.app = App(self)
        self.app

class App():
    def __init__(self, parent):
        self.parent = parent
        self.tabview = customtkinter.CTkTabview(master=self.parent.l1, corner_radius=32)
        self.tabview.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.menu_tambah = MenuTambah(self.tabview)
        self.menu_daftar = MenuDaftar(self.tabview)
        self.menu_tampil = MenuTampil(self.tabview)
        self.menu_hapus = MenuHapus(self.tabview)

class Messagebox:
    def __init__(self):
        pass

    @staticmethod
    def show_info(message):
        CTkMessagebox(title="Info", message=message)

    @staticmethod
    def show_error(message):
        CTkMessagebox(title="Error", message=message)

    @staticmethod
    def show_warning(message):
        CTkMessagebox(title="Warning", message=message, icon="warning")

    @staticmethod
    def show_question(message):
        return CTkMessagebox(title="Question", message=message, icon="question", option_1="Delete", option_2="Cancel").get()

    @staticmethod
    def show_checkmark(message):
        CTkMessagebox(title="Checkmark", message=message, icon="check")

class MenuDaftar:
    def __init__(self, parent):
        self.tab = parent.add("Daftar ID Tree")
        self.textbox = customtkinter.CTkTextbox(master=self.tab, state="disabled", height=400, width=700)
        self.textbox.pack(padx=10, pady=10)
        self.button = customtkinter.CTkButton(master=self.tab, text="Refresh", command=self.load_data, corner_radius=32)
        self.button.pack(padx=10, pady=10)

        self.load_data()

    def load_data(self):
        db = Database()
        pesan = Messagebox()
        data = db.get_all_plants_data()
        if not data:
            pesan.show_info("Tidak ada data")
            return

        textbox_data = "\n".join(f"ID Tree: {row[0]:<5}, Latitude: {row[1]:<25}, Longitude: {row[2]:<25}, Waktu: {row[3]:<10}" for row in data)
        
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("0.0", textbox_data)
        self.textbox.configure(state="disabled")

class MenuTambah:
    def __init__(self, parent):
        self.tab = parent.add("Tambah")
        self.entry = customtkinter.CTkEntry(corner_radius=32, master=self.tab, placeholder_text="Masukkan ID")
        self.entry.pack(padx=10, pady=10)
        self.button = customtkinter.CTkButton(corner_radius=32, master=self.tab, text="Tambah", command=self.tambah)
        self.button.pack(padx=10, pady=10)

    def tambah(self):
        data = self.entry.get()
        crud = CRUD()
        pesan = Messagebox()
        if data.strip() and data.isdigit():
            if crud.id_tree_exists(data):
                pesan.show_error(f"ID {data} sudah ada")
                return
            crud.tambah_tanaman(data)
            pesan.show_checkmark(f"Berhasil menambahkan data dengan ID: {data}")
            self.entry.delete(0, 'end')
        else:
            pesan.show_warning("ID tidak boleh kosong atau harus berupa angka")

class MenuTampil:
    def __init__(self, parent):
        self.tab = parent.add("Tampil")
        self.button1 = customtkinter.CTkButton(corner_radius=32, master=self.tab, text="Grafik 1 Tanaman", command=self.satu_tanaman, width=205, )
        self.button1.pack(padx=10, pady=10)
        self.button2 = customtkinter.CTkButton(corner_radius=32, master=self.tab, text="Mean Semua Sensor Tanaman", command=self.show_mean)
        self.button2.pack(padx=10, pady=10)
        self.toplevel = None

    def satu_tanaman(self):
        if self.toplevel is None or not self.toplevel.winfo_exists():
            self.toplevel = SatuTanaman()  # create window if its None or destroyed
        else:
            self.toplevel.focus()  # if window exists focus it

    def show_mean(self):
        if self.toplevel is None or not self.toplevel.winfo_exists():
            self.toplevel = meanTanaman()  # create window if its None or destroyed
        else:
            self.toplevel.focus()  # if window exists focus it

class SatuTanaman(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("440x500")
        self.title("Tampilkan")
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.minta_id()

    def minta_id(self):
        self.clear_frame()
        self.l = customtkinter.CTkLabel(master=self.frame, text="Tampilkan Grafik 1 Tanaman", font=("Arial", 20, "bold"))
        self.l.pack(pady=50)
        self.entry = customtkinter.CTkEntry(corner_radius=32, master=self.frame, width=177, placeholder_text="Masukkan ID")
        self.entry.pack(pady=4, padx=10)
        self.button = customtkinter.CTkButton(corner_radius=32, master=self.frame, text="Tampilkan", command=lambda: self.pilih_type_sensor(self.entry.get()))
        self.button.pack(pady=4, padx=10)

    def pilih_type_sensor(self, id):
        data = id
        pesan = Messagebox()
        label_sensor = {
        0: "Suhu udara (°C)",
        1: "Kelembaban udara (%)",
        2: "Curah hujan (mm)",
        3: "Tingkat sinar UV",
        4: "Suhu tanah (°C)",
        5: "Kelembaban tanah (%)",
        6: "pH tanah",
        7: "Kadar N dalam tanah (mg/kg)",
        8: "Kadar P dalam tanah (mg/kg)",
        9: "Kadar K dalam tanah (mg/kg)"
    }
        if data.strip() and data.isdigit():
            crud = CRUD()
            if crud.id_tree_exists(data):
                self.clear_frame()
                self.geometry("440x630")
                self.l = customtkinter.CTkLabel(master=self.frame, text="Pilih Tipe Sensor", font=("Arial", 20, "bold"))
                self.l.pack(pady=50)
                for sensor_type, label in label_sensor.items():
                    button = customtkinter.CTkButton(master=self.frame, text=label, command=lambda id=data, sn = label, st=sensor_type: self.minta_waktu(id, st, sn))
                    button.pack(pady=5)
                self.button1 = customtkinter.CTkButton(corner_radius=32, master=self.frame, fg_color="red",text="Kembali", command=self.minta_id)
                self.button1.pack(pady=20, padx=10)
            else:
                pesan.show_error(f"ID {data} tidak ditemukan")
        else:
            pesan.show_warning("ID tidak boleh kosong")

    def minta_waktu(self, id, type_sensor, nama_sensor):
        data = id
        pesan = Messagebox()
        if data.strip() and data.isdigit():
            crud = CRUD()
            if crud.id_tree_exists(data):
                self.clear_frame()
                self.l = customtkinter.CTkLabel(master=self.frame, text="Tampilkan Grafik 1 Tanaman", font=("Arial", 20, "bold"))
                self.l.pack(pady=50)
                self.start_date_label = customtkinter.CTkLabel(master=self.frame, text="Tanggal Mulai:")
                self.start_date_label.pack(pady=5)
                self.start_date_entry = tkcalendar.DateEntry(master=self.frame, date_pattern='yyyy-mm-dd')
                self.start_date_entry.pack(pady=5)
                
                self.end_date_label = customtkinter.CTkLabel(master=self.frame, text="Tanggal Akhir:")
                self.end_date_label.pack(pady=5)
                self.end_date_entry = tkcalendar.DateEntry(master=self.frame, date_pattern='yyyy-mm-dd')
                self.end_date_entry.pack(pady=5)

                self.show_button = customtkinter.CTkButton(corner_radius=32, master=self.frame, fg_color="green",text="Tampilkan", command=lambda : self.take_datetime(data, type_sensor, nama_sensor))
                self.button1 = customtkinter.CTkButton(corner_radius=32, master=self.frame, fg_color="red",text="Kembali", command=lambda id = data : self.pilih_type_sensor(id))
                self.button1.pack(pady=20, side="left", padx=10)
                self.show_button.pack(pady=20, side="right", padx=10)
            else:
                pesan.show_error(f"ID {data} tidak ditemukan")
        else:
            pesan.show_warning("ID tidak boleh kosong")

    def take_datetime(self, id, type_sensor, nama_sensor):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"
        id = id
        type_sensor = type_sensor
        nama_sensor = nama_sensor

        return self.grafik_sensor(id, type_sensor, nama_sensor, start_datetime, end_datetime)

    def grafik_sensor(self, id_tree, sensor_type, nama_sensor, waktu_mulai, waktu_akhir):
        update = Grafik()
        pesan = Messagebox()
        data = update.ambil_data_sensor(id_tree, sensor_type, waktu_mulai, waktu_akhir)

        if not data:
            pesan.show_error(f"Tidak ada data untuk grafik ID tanaman = {id_tree}")
            return

        nilai, timestamps = zip(*data)
        timestamps = [dt.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]

        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'brown', 'orange', 'purple', 'brown']
        plt.style.use('dark_background')
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, nilai, marker='o', linestyle='-', label=nama_sensor, color=colors[sensor_type % len(colors)])
        plt.title(f'Grafik {nama_sensor} untuk ID Tanaman {id_tree}')
        plt.xlabel('Waktu')
        plt.ylabel(nama_sensor)

        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

        plt.gcf().autofmt_xdate()
        plt.grid(True)

        plt.legend()
        plt.show()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

class meanTanaman(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("440x500")
        self.title("Tampilkan Grafik Mean")
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.l = customtkinter.CTkLabel(master=self.frame, text="Tampilkan Grafik Mean", font=("Arial", 20, "bold"))
        self.l.pack(pady=10)
        
        self.start_date_label = customtkinter.CTkLabel(master=self.frame, text="Tanggal Mulai:")
        self.start_date_label.pack(pady=5)
        self.start_date_entry = tkcalendar.DateEntry(master=self.frame, date_pattern='yyyy-mm-dd')
        self.start_date_entry.pack(pady=5)
        
        self.end_date_label = customtkinter.CTkLabel(master=self.frame, text="Tanggal Akhir:")
        self.end_date_label.pack(pady=5)
        self.end_date_entry = tkcalendar.DateEntry(master=self.frame, date_pattern='yyyy-mm-dd')
        self.end_date_entry.pack(pady=5)
        
        self.show_button = customtkinter.CTkButton(corner_radius=32, master=self.frame, text="Tampilkan", command=self.minta_data)
        self.show_button.pack(pady=20)

    def minta_data(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        
        pesan = Messagebox()
        try:
            update = Grafik()
            start_datetime = f"{start_date} 00:00:00"
            end_datetime = f"{end_date} 23:59:59"
            data = update.ambil_rata_rata_sensor(start_datetime, end_datetime)
            
            if not data:
                pesan.show_info("Tidak ada data sensor untuk rentang tanggal yang dipilih.")
                return

            self.tampilkan_grafik(data, start_datetime, end_datetime)
        
        except Exception as e:
            pesan.show_error(f"Terjadi kesalahan: {str(e)}")

    def tampilkan_grafik(self, rata_rata, waktu_mulai, waktu_akhir):
        label_sensor = {
            0: "Suhu udara (°C)",
            1: "Kelembaban udara (%)",
            2: "Curah hujan (mm)",
            3: "Tingkat sinar UV",
            4: "Suhu tanah (°C)",
            5: "Kelembaban tanah (%)",
            6: "pH tanah",
            7: "Kadar N dalam tanah (mg/kg)",
            8: "Kadar P dalam tanah (mg/kg)",
            9: "Kadar K dalam tanah (mg/kg)"
        }

        jumlah_sensor = len(label_sensor)
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 8))
        # Menyiapkan array untuk posisi bar
        bar_positions = np.arange(jumlah_sensor)
        # Menyiapkan array untuk lebar bar
        bar_width = 0.35
        # Menyiapkan array untuk label bar
        bar_labels = [label_sensor[i] for i in range(jumlah_sensor)]
        # Menyiapkan warna untuk setiap bar
        colors = ['skyblue', 'salmon', 'lightgreen', 'gold', 'lightcoral', 
                'lightskyblue', 'orange', 'mediumseagreen', 'lightpink', 'lightgrey']
        # Plot garis untuk rata-rata pembacaan sensor, satu garis untuk setiap sensor
        jitter = np.linspace(-0.2, 0.2, jumlah_sensor)  # Menambahkan jitter untuk nilai x
        for i in range(jumlah_sensor):
            x_values = bar_positions + jitter[i]  # Menambahkan jitter pada posisi x
            y_values = [rata_rata[j] for j in range(jumlah_sensor)]
            ax.plot(x_values, y_values, marker='o', linestyle='-', color=colors[i], linewidth=2, label=label_sensor[i])
        # Tambahkan label pada sumbu-x
        ax.set_xticks(bar_positions)
        ax.set_xticklabels(bar_labels, rotation=45, ha='right')
        # Tambahkan label pada sumbu-y
        ax.set_ylabel('Rata-rata Nilai Sensor')
        # Tambahkan judul dengan keterangan rentang waktu
        ax.set_title(f'Rata-rata Sensor untuk Setiap Tipe Sensor Semua Tanaman\nRentang Waktu: {waktu_mulai} - {waktu_akhir}')
        # Tambahkan grid
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        # Tambahkan legend
        ax.legend()
        plt.tight_layout()
        plt.show()
        # Plot bar untuk rata-rata pembacaan sensor dengan warna yang berbeda
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.bar(bar_positions, [rata_rata[i] if rata_rata[i] is not None else 0 for i in range(jumlah_sensor)], 
                    bar_width, color=colors, label='Rata-rata Nilai Sensor')
        # Tambahkan label pada sumbu-x
        ax.set_xticks(bar_positions)
        ax.set_xticklabels(bar_labels, rotation=45, ha='right')
        # Tambahkan label pada sumbu-y
        ax.set_ylabel('Rata-rata Nilai Sensor')
        # Tambahkan judul dengan keterangan rentang waktu
        ax.set_title(f'Rata-rata Sensor untuk Setiap Tipe Sensor Semua Tanaman\nRentang Waktu: {waktu_mulai} - {waktu_akhir}')
        # Tambahkan grid
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        # Tambahkan legend
        ax.legend()
        # Tambahkan nilai rata-rata di atas bar
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')
        plt.tight_layout()
        plt.show()

class MenuHapus:
    def __init__(self, parent):
        self.tab = parent.add("Hapus")
        self.entry = customtkinter.CTkEntry(corner_radius=32, master=self.tab, placeholder_text="Masukkan ID")
        self.entry.pack(padx=10, pady=10)
        self.button = customtkinter.CTkButton(corner_radius=32, master=self.tab, text="Hapus", command=self.hapus)
        self.button.pack(padx=10, pady=10)

    def hapus(self):
        crud = CRUD()
        pesan = Messagebox()
        data = self.entry.get()
        if not data.isdigit():
            pesan.show_warning("ID tidak boleh kosong atau harus berupa angka")
            return

        if not crud.id_tree_exists(data):
            pesan.show_warning(f"ID {data} tidak ditemukan")
            return
        
        if pesan.show_question(f"Apakah anda yakin ingin menghapus ID {data}?") == "Delete":
            crud.hapus(data)
            pesan.show_checkmark(f"Berhasil menghapus data dengan ID: {data}")
            self.entry.delete(0, 'end')

if __name__ == "__main__":
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("blue")
    app = App()
    app.mainloop()
