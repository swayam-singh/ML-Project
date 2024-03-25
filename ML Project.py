import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def read_stock_data(folder_path):
    """
    Read all CSV files in the specified folder and return a dictionary of DataFrames.
    Keys are company symbols extracted from filenames.
    """
    stock_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            symbol = filename.split("_")[0]
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path, index_col="Date", parse_dates=True)
            stock_data[symbol] = df
    return stock_data

def plot_stock_chart(company_symbol):
    """
    Plot stock chart for the selected company.
    """
    if company_symbol not in stock_data:
        messagebox.showerror("Error", "Company data not found.")
        return

    df = stock_data[company_symbol]
    plt.figure(figsize=(8, 5))
    plt.plot(df.index, df['Close'], label='Close Price', color='blue')
    plt.title(f"Stock Chart for {company_symbol}", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Price", fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True)
    
    # Create a Tkinter canvas to embed Matplotlib plot
    canvas = FigureCanvasTkAgg(plt.gcf(), master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Path to the folder containing CSV files
folder_path = r"C:\Users\Singh\Desktop\archive"

# Read stock data
stock_data = read_stock_data(folder_path)

# Create Tkinter window
root = tk.Tk()
root.title("Stock Chart Viewer")
root.geometry("800x600")

# Create main frame
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create sidebar frame for company selection
sidebar_frame = ttk.Frame(main_frame)
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

company_label = ttk.Label(sidebar_frame, text="Select Company:", font=("Arial", 12))
company_label.pack(pady=5)

company_listbox = tk.Listbox(sidebar_frame, font=("Arial", 11), width=20, height=15)
for company in stock_data.keys():
    company_listbox.insert(tk.END, company)
company_listbox.pack(pady=5)
company_listbox.bind("<<ListboxSelect>>", lambda event: plot_stock_chart(company_listbox.get(tk.ACTIVE)))

# Create frame for plot
plot_frame = ttk.Frame(main_frame)
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
