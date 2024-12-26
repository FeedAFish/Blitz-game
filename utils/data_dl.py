import os
import urllib.request
import py7zr
import shutil
import tkinter as tk
import threading
import datetime


class Download_UI:
    def __init__(self, version, url):
        self.root = tk.Tk()
        self.root.title("Status")
        self.root.overrideredirect(True)
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the position to center the window
        position_top = int((screen_height - 300) / 2)
        position_left = int((screen_width - 100) / 2)

        self.root.geometry(f"{300}x{100}+{position_left}+{position_top}")
        self.root.resizable(False, False)
        try:
            self.label = tk.Label(
                self.root, text="Checking data...", font=("asdasaf", 12)
            )
        except:
            self.label = tk.Label(self.root, text="Checking data...", font=(None, 12))

        self.label.pack(expand=True)
        self.thread = threading.Thread(target=self.main, args=(version, url))
        self.thread.start()
        self.root.mainloop()
        self.thread.join()

    def main(self, version, url):
        if self.checking(version):
            # Download the data
            self.root.after(1000, self.create_popup_message, "Downloading data...")
            try:
                self.download_data(version, url)
                self.root.after(1000, self.create_popup_message, "Data is up to date !")
                # Close the window after 2 seconds
            except Exception as e:
                self.root.after(
                    1000, self.create_popup_message, f"Error downloading data !"
                )
                with open("error.log", "a") as f:
                    f.writelines("\n")
                    f.writelines(
                        "At "
                        + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        + " :\n"
                    )
                    f.writelines(f"Error downloading data ! " + str(e))
        else:
            self.root.after(1000, self.create_popup_message, "Data is up to date !")
        self.root.after(2000, self.root.destroy)

    def create_popup_message(self, message):
        self.label.config(text=message)

    def checking(self, version):
        return (
            not os.path.exists("data/version.ini")
            or open("data/version.ini").read() != version
        )

    def download_data(self, version, url):
        if os.path.exists("data.7z"):
            os.remove("data.7z")
        # Download the zip file
        urllib.request.urlretrieve(url, "data.7z")

        # Remove the old data folder

        if os.path.exists("data"):
            shutil.rmtree("data")

        # Unzip the 7z file
        with py7zr.SevenZipFile("data.7z", mode="r") as z:
            z.extractall("./")
        os.remove("data.7z")
