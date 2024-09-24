import tkinter as tk
from tkinter import filedialog, Text

import requests
import json


#The API key is in a file called 'apikey' in the same directory as this python file
filename = 'apikey'

#function that gets the contents from a file, removing any leading and trialing whitespace
def get_file_contents(nameOfFile):
    #return the contents of a given file
    try:
        with open(nameOfFile, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"'{nameOfFile}' file not found")
            
#get API key and use in the latest endpoint URL
api_key = get_file_contents(filename)
latest_endpoint_url = f"https://data.fixer.io/api/latest?access_key={api_key}"
symbols_endpoint_url = f"https://data.fixer.io/api/symbols?access_key={api_key}"

#function that returns the latest conversion rate from the 'initial' currency to the 'final' currency
def getLatestCoversionRate(initial, final):
    querystring = {"base": initial, "symbols": final}
    response = requests.get(latest_endpoint_url, params=querystring)
    if response.status_code == 200:
        responseJSON = response.json()
        return responseJSON["rates"][final]
    else:
        print(f"Error: {response.status_code}")
        return None

#function that converts what is written in the text box from the base currency to the target currency
def convert():
    rate = getLatestCoversionRate(start.get(), target.get())
    val = startText.get(1.0, "1.0 lineend") 
    conversion = round(int(val) * rate, 2)
    conversionLabel.config(text = str(conversion) + " " + target.get())

# Create object
root = tk.Tk()
root.title('Currency Converter')

canvas = tk.Canvas(root, height=300, width=400, bg = "#D3B683", borderwidth=3)
canvas.pack()

frame = tk.Frame(root, bg="#420D09")
frame.place(relwidth= 0.9, relheight=0.8, relx=0.05, rely=0.1)

#currency options, only base currency allowed in Fixer's free account is 'EUR'
startOptions = ['EUR']
targetOptions = ['AED', 'AUD', 'CAD', 'CNY', 'GBP', 'HKD', 'IDR', 'JPY', 'KRW', 'NGN', 'NOK', 'USD']


#datatype of menu text
start = tk.StringVar()
target = tk.StringVar()

#intial text of menus
start.set(startOptions[0])
target.set(targetOptions[0])

#create dropdown menus
startMenu = tk.OptionMenu(frame, start, *startOptions)
targetMenu = tk.OptionMenu(frame, target, *targetOptions)

startMenu.place(relwidth= 0.25, relheight=0.1, relx=0.375, rely=0.15)
targetMenu.place(relwidth= 0.25, relheight=0.1, relx=0.375, rely=0.3)

# Textbox creation
startText = tk.Text(frame, height = 1)
startText.place(relwidth = 0.4, relx=0.3, rely=0.47)

# Button Creation 
convertButton = tk.Button(frame, text = "Convert", command = convert, bg="#D3B683")
convertButton.place(relwidth= 0.4, relheight=0.15, relx=0.3, rely=0.64)
  
# Create labels
conversionLabel = tk.Label(frame, text = "", bg="#420D09", fg="#D3B683")
conversionLabel.place(relwidth= 0.4, relx=0.3, rely=0.84)

fromLabel = tk.Label(frame, text = "From: ", bg="#420D09", fg="#D3B683")
fromLabel.place(relwidth= 0.1, relx=0.27, rely=0.15)

toLabel = tk.Label(frame, text = "To:", bg="#420D09", fg="#D3B683")
toLabel.place(relwidth= 0.07, relx=0.3, rely=0.3)


root.mainloop()




