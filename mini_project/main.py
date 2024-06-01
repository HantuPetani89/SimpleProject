from root.data import Getdata
from root.display import Apputama

def main():
    update = Getdata()
    app = Apputama()
    update.ambil_data()
    app.mainloop()

if __name__ == "__main__":
    main()