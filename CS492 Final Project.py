import tkinter as tk
from tkinter import messagebox
import os
import hashlib
import random
import Crypto.Cipher
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class Car:
    def __init__(self,make,color):
        self.make=make
        self.color = color
        self.key = None
        self.reg_status = "Not Registered"
        self.owner = None
        self.status = None

    def generate_key(self):
        self.key = get_random_bytes(8)
        self.reg_status = "Registered"

    def set_status(self, status):
        self.status = status

    def set_owner(self,owner):
        self.owner = owner

        #I want to make a DES key that can encrypt the code of the function and the decrypted to be secure.
        #So when the 'lock' button is selected LOCK is encrypted with the DES key and sent to the car.
        #the car will then verify that the command sent can be executed by decrypting the incoming encrypted message.
def generate_random_car():
    makes = ["Toyota","Honda", "Ford", "Chevrolet", "BMW"]
    colors = ["Red", "Blue", "Green", "Black","White"]
    make = random.choice(makes)
    color = random.choice(colors)
    return Car(make,color)

#login credentials admin,admin
class myGUI:
    def __init__(self):
        self.current_directory = os.getcwd()
        self.main_window = tk.Tk()
        self.main_window.title('Key Fob Sim')
        self.main_window.geometry("500x450")
        self.main_frame = tk.Frame(self.main_window,height=1000,width=800)
        self.main_frame.pack()

        self.main_button_frame = tk.Frame(self.main_frame)
        self.main_button_frame.pack()
        self.user_label = tk.Label(self.main_button_frame,text='Username: ')
        self.user_label.pack()
        self.user_login_entry = tk.Entry(self.main_button_frame)
        self.user_login_entry.pack()
        self.pass_label = tk.Label(self.main_button_frame, text='Password: ')
        self.pass_label.pack()
        self.pass_login_entry = tk.Entry(self.main_button_frame, show='*')
        self.pass_login_entry.pack()
        self.login_button = tk.Button(self.main_button_frame,text="Login", command=self.login_verification)
        self.login_button.pack(padx=10, pady=10)
        self.create_account_button = tk.Button(self.main_button_frame,text="Create Account",command=self.create_account)
        self.create_account_button.pack(padx=10, pady=10)

    def create_account(self):
        self.create_account_window = tk.Toplevel()
        self.create_account_window.title("Account Creation")
        self.create_frame = tk.Frame(self.create_account_window)
        self.create_frame.pack()
        self.username_frame = tk.Frame(self.create_frame)
        self.username_frame.pack()
        self.username_label = tk.Label(self.username_frame,text='Username:')
        self.username_label.pack(side='left', padx=1, pady=10)
        self.username_entry = tk.Entry(self.username_frame)
        self.username_entry.pack(side='left',padx=10,pady=10)
        self.password_frame = tk.Frame(self.create_frame)
        self.password_frame.pack()
        self.password_label = tk.Label(self.password_frame, text='Password: ')
        self.password_label.pack(side='left',padx=10,pady=10)
        self.password_entry = tk.Entry(self.password_frame)
        self.password_entry.pack(side='left')
        self.confpassword_frame = tk.Frame(self.create_frame)
        self.confpassword_frame.pack()
        self.confpassword_label = tk.Label(self.confpassword_frame,text='re-enter Password: ')
        self.confpassword_label.pack(side='left',padx=10,pady=10)
        self.confpassword_entry = tk.Entry(self.confpassword_frame)
        self.confpassword_entry.pack(side='left')
        self.button_frame = tk.Frame(self.create_frame)
        self.button_frame.pack()
        self.create_button = tk.Button(self.button_frame,text='Create',command = self.account_creation)
        self.create_button.pack()

    def account_creation(self):
        self.username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        password_hash = hashlib.md5(password.encode()).hexdigest()
        account_creation = 0
        try:
            with open("./information.txt", "a") as file:  # Open in append mode
                with open("./information.txt", "r") as read_file:  # Open for reading
                    for line in read_file:
                        stored_user, stored_pass = line.split(',')
                        if self.username == stored_user:
                            messagebox.showinfo('Error', "Username is already in use")
                            break
                    else:
                        #need a check to make sure passwords match.
                        #need a check to ensure password is within parameters
                        file.write(f"{self.username},{password_hash}\n")
                        account_creation = 1
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        if account_creation == 1:
            messagebox.showinfo("confirm","account creation successful")
            self.key_fob_window()

    def key_fob_window(self):
        self.main_frame.pack_forget()
        #generate key, simulation, account info, logout, exit
        #creation of the button frame top left of application
        self.menu_button_frame = tk.Frame(self.main_window)
        self.menu_button_frame.pack(fill='x',expand=True)
        self.generate_button = tk.Button(self.menu_button_frame, text='Generate Key', command=self.generation_button)
        self.simulate_button = tk.Button(self.menu_button_frame,text="Simulate Key", command=self.key_simulation)
        self.account_button = tk.Button(self.menu_button_frame,text="Account")
        self.generate_button.pack(side='left', padx=15, pady=15)
        self.simulate_button.pack(side='left', padx=15, pady=15)
        self.account_button.pack(side='left', padx=15, pady=15)
        #creation of the display information frame
        self.info_frame = tk.Frame(self.main_window)
        self.info_frame.pack(fill='x',expand=True)
        self.info_label = tk.Label(text='This is a test')
        self.info_label.pack(side='top' ,padx=15, pady=15)
        #creation of logout and exit buttons
        self.exit_frame = tk.Frame(self.main_window)
        self.exit_frame.pack(fill='x',expand=True)
        self.logout_button = tk.Button(self.exit_frame,text="Logout")
        self.exit_button = tk.Button(self.exit_frame,text="Exit")
        self.logout_button.pack(side='right',padx=15,pady=15)
        self.exit_button.pack(side='right',padx=15,pady=15)

    def generation_button(self):
        self.users_car = generate_random_car()
        self.info_label.config(text=f"Your car: {self.users_car.color} {self.users_car.make}")
        self.get_key_button = tk.Button(self.info_frame,text="Get Key",command=self.generate_key)
        self.get_key_button.pack(side='right', padx=15,pady=15)

    def generate_key(self):
        self.users_car.generate_key()
        owner = self.username
        self.users_car.set_owner(owner)
        self.get_key_button.pack_forget()
        self.exit_frame.pack_forget()
        self.info_reg_label = tk.Label(self.info_frame, text=f"Registration status: {self.users_car.reg_status}")
        self.info_reg_label.pack()
        self.info_owner_label = tk.Label(self.info_frame, text=f"Owner: {self.users_car.owner}")
        self.info_owner_label.pack()
        self.info_status_label = tk.Label(self.info_frame, text=f"Status: {self.users_car.status}")
        self.info_status_label.pack()
        self.key_fob_frame = tk.Frame(self.main_window)
        self.key_fob_frame.pack(fill='x',expand=True)
        self.exit_frame.pack()
        self.unlock_button = tk.Button(self.key_fob_frame,text="Unlock")
        self.lock_button = tk.Button(self.key_fob_frame,text="Lock")
        self.trunk_button = tk.Button(self.key_fob_frame,text="Trunk")
        self.start_button = tk.Button(self.key_fob_frame,text="Start")
        self.start_button.pack(side='top', padx=10,pady=10)
        self.unlock_button.pack(side='right', padx=10,pady=10)
        self.lock_button.pack(side='left',padx=10,pady=10)
        self.trunk_button.pack(side='bottom',padx=10,pady=10)

    def key_simulation(self):
        self.simulation_window = tk.Toplevel()
        self.simulation_window.geometry('800x600')
        self.grid_frame1 = tk.Frame(self.simulation_window)
        self.grid_frame2 = tk.Frame(self.simulation_window)
        self.grid_frame1.pack(side='left', padx=10, pady=10)
        self.grid_frame2.pack(side='left', padx=10, pady=10)

        self.buttons1 = []
        self.buttons2 = []
        for i in range(2):
            for j in range(6):
                button = tk.Button(self.grid_frame1, text=f"Button {i * 6 + j + 1}")
                button.grid(row=j, column=i, padx=5, pady=5)
                self.buttons1.append(button)

                button = tk.Button(self.grid_frame2, text=f"Button {i * 6 + j + 13}")
                button.grid(row=j, column=i, padx=5, pady=5)
                self.buttons2.append(button)
        self.key_fob_frame = tk.Frame(self.simulation_window)
        self.key_fob_frame.pack(fill='x', expand=True)
        self.unlock_button = tk.Button(self.key_fob_frame, text="Unlock")
        self.lock_button = tk.Button(self.key_fob_frame, text="Lock", command=self.lock_button_simulation)
        self.trunk_button = tk.Button(self.key_fob_frame, text="Trunk")
        self.start_button = tk.Button(self.key_fob_frame, text="Start")
        self.start_button.pack(side='top', padx=10, pady=10)
        self.unlock_button.pack(side='right', padx=10, pady=10)
        self.lock_button.pack(side='left', padx=10, pady=10)
        self.trunk_button.pack(side='bottom', padx=10, pady=10)
        self.populate_car_array()

    def lock_button_simulation(self):
        command = "lock"
        cipher = DES.new(self.users_car.key, DES.MODE_ECB)
        padded_command = pad(command.encode(), DES.block_size)
        encrypted_command = cipher.encrypt(padded_command)
        for index, car in enumerate(self.car_array):
            print(f"{index} car: {car.owner}")
            decryptor = DES.new(car.key, DES.MODE_ECB)
            decrypted_command = decryptor.decrypt(encrypted_command)
            if padded_command == decrypted_command:

                if index < len(self.buttons1):
                    self.buttons1[index].config(bg='red')
                    print("test")
                else:
                    index = index-12
                    self.buttons2[index].config(bg='red')
                print(f"Car: {car.owner} {index}")

    def populate_car_array(self):
        self.car_array = []
        self.car_array.append(self.users_car)
        for _ in range(23):
            car = generate_random_car()
            car.generate_key()
            self.car_array.append(car)
        random.shuffle(self.car_array)


    def login_verification(self):
        user_in_system_flag =0
        correct_password=0
        try:
            with open("./information.txt", 'r')as file:
                file.seek(0)
                for line in file:
                    #parse each line to extract username/passwords
                    username, password = line.strip().split(',')
                    username = username.strip()
                    password = password.strip()
                    self.username = self.user_login_entry.get().strip()
                    input_password = self.pass_login_entry.get().strip()
                    if username == self.username:
                        print("user is found")
                        user_in_system_flag =1
                        #send password through encryption here
                        input_password_hash = hashlib.md5(input_password.encode()).hexdigest()
                        print(f"hash: {input_password_hash}\n")
                        if password == input_password_hash:
                            correct_password=1
                            print("This user is in the system.")
                    if user_in_system_flag and correct_password:
                        self.key_fob_window()
        except FileNotFoundError:
            messagebox.showerror("Error","File not found.")


if __name__ == '__main__':
    mygui = myGUI()
    tk.mainloop()