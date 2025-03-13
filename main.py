import customtkinter as ctk
from tkinter import messagebox, filedialog
from webscrap import WebScraper
import extract_information
import pyfiglet
import threading

# Set appearance and color theme
ctk.set_appearance_mode("Dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# Make base_url a global variable
base_url = ""


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Modern Web Scraper")
        self.geometry("800x600")
        self.resizable(True, True)

        # Initialize animation variables
        self.loading_label = None
        self.animation_active = False
        self.current_thread = None

        # Create main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # ASCII Art Title
        self.create_ascii_art()

        # URL Input Section
        self.create_url_input()

        # Buttons
        self.create_action_buttons()

        # Initialize extraction variables
        self.extract_type_var = ctk.StringVar(value="class")
        self.file_path = ""

    def create_ascii_art(self):
        ascii_art = pyfiglet.figlet_format("Web Scraper")
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text=ascii_art,
            font=ctk.CTkFont(family="Courier", size=14),
            text_color="#2CC985"
        )
        self.title_label.pack(pady=20)

    def create_url_input(self):
        url_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        url_frame.pack(pady=10, fill="x", padx=40)

        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="Enter website URL...",
            width=400,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14)
        )
        self.url_entry.pack(side="left", expand=True)

    def create_action_buttons(self):
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        self.scrape_btn = ctk.CTkButton(
            button_frame,
            text="Start Scraping",
            command=self.start_scraping,
            width=200,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2CC985",
            hover_color="#207A4B"
        )
        self.scrape_btn.pack(pady=10)

        self.extract_btn = ctk.CTkButton(
            button_frame,
            text="Start Extraction",
            command=self.ask_for_extraction,
            width=200,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3B8ED0",
            hover_color="#265A8C"
        )
        self.extract_btn.pack(pady=10)

    def show_loading_animation(self):
        # Always create a new loading label
        self.hide_loading_animation()  # Clean up any existing label
        self.loading_label = ctk.CTkLabel(
            self.main_frame,
            text="Loading",
            font=ctk.CTkFont(size=14),
            text_color="#2CC985"
        )
        self.loading_label.pack(pady=10)
        self.animation_active = True
        self.update_animation()

    def update_animation(self):
        if self.animation_active:
            current_text = self.loading_label.cget("text")
            if current_text.endswith("..."):
                new_text = "Loading"
            else:
                new_text = current_text + "."
            self.loading_label.configure(text=new_text)
            self.after(500, self.update_animation)

    def hide_loading_animation(self):
        self.animation_active = False
        if self.loading_label:
            self.loading_label.destroy()
            self.loading_label = None

    def start_scraping_thread(self):
        global base_url
        try:
            scraper = WebScraper(base_url)
            scraper.start_crawling()
            self.after(0, self.on_scraping_success)
        except Exception as e:
            self.after(0, self.on_scraping_error, e)

    def start_scraping(self):
        global base_url
        base_url = self.url_entry.get().strip()

        if not base_url.startswith(("http://", "https://")) and base_url!="":
            base_url = f"https://{base_url}"

        if not base_url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        self.scrape_btn.configure(state="disabled")
        self.extract_btn.configure(state="disabled")
        self.show_loading_animation()

        self.current_thread = threading.Thread(target=self.start_scraping_thread, daemon=True)
        self.current_thread.start()

    def on_scraping_success(self):
        self.hide_loading_animation()
        self.scrape_btn.configure(state="normal")
        self.extract_btn.configure(state="normal")
        messagebox.showinfo("Success", "Scraping complete!\nReady to extraction.")

    def on_scraping_error(self, error):
        self.hide_loading_animation()
        self.scrape_btn.configure(state="normal")
        self.extract_btn.configure(state="normal")
        messagebox.showerror("Error", f"Scraping failed: {str(error)}")

    def ask_for_extraction(self):
        self.clear_main_frame()

        # File Selection
        file_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        file_frame.pack(pady=10)

        self.file_entry = ctk.CTkEntry(
            file_frame,
            placeholder_text="Select JSON file (optional)",
            width=400,
            height=35
        )
        self.file_entry.pack(side="left", padx=10)

        browse_btn = ctk.CTkButton(
            file_frame,
            text="Browse",
            command=self.browse_file,
            width=80,
            height=35,
            fg_color="#3B8ED0",
            hover_color="#265A8C"
        )
        browse_btn.pack(side="left")

        # Extraction Type
        type_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        type_frame.pack(pady=15)

        ctk.CTkLabel(type_frame, text="Extract by:", font=ctk.CTkFont(size=14)).pack(side="left")

        class_radio = ctk.CTkRadioButton(
            type_frame,
            text="Class",
            variable=self.extract_type_var,
            value="class",
            font=ctk.CTkFont(size=14)
        )
        class_radio.pack(side="left", padx=10)

        id_radio = ctk.CTkRadioButton(
            type_frame,
            text="ID",
            variable=self.extract_type_var,
            value="id",
            font=ctk.CTkFont(size=14)
        )
        id_radio.pack(side="left", padx=10)

        # Target Input
        self.target_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter class/ID name...",
            width=300,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        self.target_entry.pack(pady=15)

        # Start Button
        self.start_btn = ctk.CTkButton(
            self.main_frame,
            text="Start Extraction",
            command=self.perform_extraction,
            width=200,
            height=40,
            fg_color="#2CC985",
            hover_color="#207A4B",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.start_btn.pack(pady=20)

        # Start Over Button
        start_over_btn = ctk.CTkButton(
            self.main_frame,
            text="Start Over",
            command=self.reset_to_main,
            width=200,
            height=40,
            fg_color="#D33F49",
            hover_color="#9A2B32",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        start_over_btn.pack(pady=50)

    def reset_to_main(self):
        """Reset the UI to the initial state"""
        self.clear_main_frame()
        self.file_path = ""
        self.extract_type_var.set("class")
        self.create_url_input()
        self.create_action_buttons()
        self.hide_loading_animation()  # Ensure loading is hidden
    def perform_extraction(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter a class/ID name.")
            return

        self.start_btn.configure(state="disabled")
        self.show_loading_animation()

        extract_type = self.extract_type_var.get()
        file_path = self.file_path
        self.current_thread = threading.Thread(
            target=lambda: self.run_extraction(extract_type, target, file_path),
            daemon=True
        )
        self.current_thread.start()

    def run_extraction(self, extract_type, target, file_path=None):
        try:
            if file_path:
                extract_information.extract_data_from_file(
                    extract_type,
                    target,
                    file_path
                )
            else:
                if not base_url:
                    self.after(0, lambda: messagebox.showerror("Error", "No URL or file selected!"))
                    return
                extract_information.extract_data(
                    extract_type,
                    target,
                    base_url
                )
            self.after(0, self.on_extraction_success)
        except Exception as e:
            self.after(0, self.on_extraction_error, e)

    def on_extraction_success(self):
        self.hide_loading_animation()
        self.start_btn.configure(state="normal")
        messagebox.showinfo("Success", "Extraction completed!")

    def on_extraction_error(self, error):
        self.hide_loading_animation()
        self.start_btn.configure(state="normal")
        messagebox.showerror("Error", f"Extraction failed: {str(error)}")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, file_path)
            self.file_path = file_path

    def clear_main_frame(self):
        self.hide_loading_animation()  # Clean up loading animation
        for widget in self.main_frame.winfo_children():
            if widget not in [self.title_label]:
                widget.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()