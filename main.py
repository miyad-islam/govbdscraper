import tkinter as tk
from tkinter import messagebox
from webscrap import WebScraper
import extract_information
import pyfiglet

# Make base_url a global variable
base_url = ""

# Function to handle the scraping process
def start_scraping():
    global base_url

    base_url = url_entry.get().strip()  # Get URL from user input

    # Automatically add 'https://' if not present
    if not base_url.startswith("http://") and not base_url.startswith("https://"):
        base_url = "https://" + base_url

    # Check if URL is valid
    if not base_url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    try:
        # Initialize the WebScraper and start crawling
        scraper = WebScraper(base_url)
        scraper.start_crawling()

        # After scraping is complete, ask for data extraction
        messagebox.showinfo("Scraping Complete", "Scraping is complete. Now proceed to data extraction.")

        # Enable the extraction button after scraping is done
        extraction_button.config(state=tk.NORMAL)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to prompt the user to choose class or id and input the target name
def ask_for_extraction():
    # Clear the current window to show extraction options
    clear_window()

    # Add prompt for class or id extraction
    extract_type_label = tk.Label(root, text="Do you want to extract by 'class' or 'id'?")
    extract_type_label.grid(row=1, column=0, padx=10, pady=10)

    # Create radio buttons for class or id extraction
    extract_type_var.set("class")  # Default to 'class'
    class_radio = tk.Radiobutton(root, text="Class", variable=extract_type_var, value="class")
    class_radio.grid(row=2, column=0, padx=10, pady=10)
    id_radio = tk.Radiobutton(root, text="ID", variable=extract_type_var, value="id")
    id_radio.grid(row=2, column=1, padx=10, pady=10)

    # Add prompt for class/id name input
    target_name_label = tk.Label(root, text="Enter class or id name:")
    target_name_label.grid(row=3, column=0, padx=10, pady=10)
    target_name_entry.grid(row=3, column=1)

    # Add 'Start Extraction' button
    start_button.config(text="Start Extraction", command=perform_extraction)
    start_button.grid(row=4, column=0, columnspan=2, pady=20)


# Function to handle the extraction of data (class/id)
def perform_extraction():
    global base_url
    extract_type = extract_type_var.get()
    target_name = target_name_entry.get().strip()

    if not target_name:
        messagebox.showerror("Error", "Please enter a valid class or id name.")
        return

    try:
        # Call the extract_data function from the webscraper module
        extract_information.extract_data(extract_type, target_name, base_url)
        messagebox.showinfo("Success", f"Extraction completed for {extract_type}: {target_name}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during extraction: {e}")


# Function to clear the window for the next set of widgets
def clear_window():
    for widget in root.winfo_children():
        widget.grid_forget()


# Create the main tkinter window
root = tk.Tk()
root.title("Web Scraper")

# Display ASCII Art title
ascii_art = pyfiglet.figlet_format("Web Scraper")
ascii_label = tk.Label(root, text=ascii_art, font=("Courier", 12))
ascii_label.grid(row=0, column=0, columnspan=2)

# Create URL input field
url_label = tk.Label(root, text="Enter URL:")
url_label.grid(row=1, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=1, column=1)

# Create the start button to trigger scraping
start_button = tk.Button(root, text="Start Scraping", command=start_scraping)
start_button.grid(row=2, column=0, columnspan=2, pady=20)

# Create extraction button, initially disabled
extraction_button = tk.Button(root, text="Start Extraction", command=ask_for_extraction, state=tk.DISABLED)
extraction_button.grid(row=3, column=0, columnspan=2, pady=20)

# Variable to hold the extraction type (class or id)
extract_type_var = tk.StringVar(value="class")

# Create target name input field for class/id name (initially hidden)
target_name_entry = tk.Entry(root, width=50)

# Run the tkinter event loop
root.mainloop()
