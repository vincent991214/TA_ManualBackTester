import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

"""
21/May/2022
08:45(UTC-5)
"""


class TradeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trade Record Keeper")
        self.root.geometry("600x450")  # Adjust the size of GUI window
        self.root.configure(bg='grey')  # Set background color to grey

        # Create labels, entries and buttons with increased size and padding
        self.entrance_price = tk.DoubleVar()
        tk.Label(root, text="Entrance Price", bg='grey', font=("Arial", 15)).grid(row=0, column=0, pady=20, padx=20)
        self.entrance_entry = tk.Entry(root, textvariable=self.entrance_price, width=40)
        self.entrance_entry.grid(row=0, column=1, pady=20, padx=20)

        self.exit_price = tk.DoubleVar()
        tk.Label(root, text="Exit Price", bg='grey', font=("Arial", 15)).grid(row=1, column=0, pady=20, padx=20)
        self.exit_entry = tk.Entry(root, textvariable=self.exit_price, width=40)
        self.exit_entry.grid(row=1, column=1, pady=20, padx=20)

        self.volumes = tk.DoubleVar()
        tk.Label(root, text="Volumes", bg='grey', font=("Arial", 15)).grid(row=2, column=0, pady=20, padx=20)
        self.volumes_entry = tk.Entry(root, textvariable=self.volumes, width=40)
        self.volumes_entry.grid(row=2, column=1, pady=20, padx=20)

        self.short_long = tk.StringVar()
        tk.Label(root, text="Short/Long", bg='grey', font=("Arial", 15)).grid(row=3, column=0, pady=20, padx=20)
        tk.Radiobutton(root, text="Short", variable=self.short_long, value="short", bg='grey', font=("Arial", 10)).grid(
            row=3, column=1)
        tk.Radiobutton(root, text="Long", variable=self.short_long, value="long", bg='grey', font=("Arial", 10)).grid(
            row=3, column=2)

        tk.Button(root, text="Add Record", command=self.add_record, width=20).grid(row=4, column=0, columnspan=3)
        tk.Label(root, text="", bg='grey', font=("Arial", 15)).grid(row=5, column=0, pady=20, padx=20)
        tk.Button(root, text="Get Trade Summary", command=self.summerize_record, width=40).grid(row=6, column=0, columnspan=3)

    def add_record(self):
        # Validate
        if self.short_long.get() not in ["short", "long"]:
            messagebox.showerror("Invalid Input", "Please select either short or long")
            return

        # Calculate gain/loss
        if self.short_long.get() == "short":
            gain_loss = (self.entrance_price.get() - self.exit_price.get()) * self.volumes.get()
        else:
            gain_loss = (self.exit_price.get() - self.entrance_price.get()) * self.volumes.get()

        # Prepare data
        data = {
            "entrance_price": [self.entrance_price.get()],
            "exit_price": [self.exit_price.get()],
            "volumes": [self.volumes.get()],
            "short_long": [self.short_long.get()],
            "gain_loss": [gain_loss],
        }

        df = pd.DataFrame(data)

        # Save to CSV
        if not os.path.isfile('trade_data.csv'):
            df.to_csv('trade_data.csv', index=False)
        else:  # else it exists so append without writing the header
            df.to_csv('trade_data.csv', mode='a', header=False, index=False)

        # Clear entries
        self.entrance_entry.delete(0, tk.END)
        self.exit_entry.delete(0, tk.END)
        self.volumes_entry.delete(0, tk.END)
        self.short_long.set('')

        # Messagebox
        messagebox.showinfo("Success", "Record added successfully")

    def summerize_record(self):
        # Load the data
        trade_data = pd.read_csv('trade_data.csv')

        # Calculate win rate
        winning_trades = trade_data[trade_data['gain_loss'] > 0]
        win_rate = len(winning_trades) / len(trade_data)
        # print(f'The win rate is {win_rate * 100:.2f}%')

        # Calculate total gain/loss
        total_gain_loss = trade_data['gain_loss'].sum()
        # print(f'The total gain/loss is {total_gain_loss}')

        # Calculate largest number of consecutive wins and losses
        trade_data['win'] = trade_data['gain_loss'] > 0
        trade_data['consecutive_wins'] = trade_data['win'] * (
                    trade_data['win'].groupby((trade_data['win'] != trade_data['win'].shift()).cumsum()).cumcount() + 1)
        trade_data['consecutive_losses'] = (~trade_data['win']) * ((~trade_data['win']).groupby(
            ((~trade_data['win']) != (~trade_data['win']).shift()).cumsum()).cumcount() + 1)
        max_consecutive_wins = trade_data['consecutive_wins'].max()
        max_consecutive_losses = trade_data['consecutive_losses'].max()
        # print(f'The largest number of consecutive wins is {max_consecutive_wins}')
        # print(f'The largest number of consecutive losses is {max_consecutive_losses}')


        messagebox.showinfo(
            "Success", f'The win rate is {win_rate * 100:.2f}%'
                       + f'\nThe total gain/loss is {total_gain_loss}'
                       + f'\nThe largest number of consecutive wins is {max_consecutive_wins}'
                       + f'\nThe largest number of consecutive losses is {max_consecutive_losses}'
        )

root = tk.Tk()
app = TradeApp(root)
root.mainloop()
