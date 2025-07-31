import customtkinter as ctk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import threading
import os
import tkinter.font as tkfont
from PIL import Image

# --- Constants ---
FONT_FAMILY = "Poppins"
FALLBACK_FONT = "Arial"
FONT_SIZE = 14
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# --- Asset Paths ---
ASSETS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
SELECT_FILES_ICON_PATH = os.path.join(ASSETS_PATH, "select_files.png")
SELECT_FOLDER_ICON_PATH = os.path.join(ASSETS_PATH, "select_folder.png")
CONVERT_ICON_PATH = os.path.join(ASSETS_PATH, "convert.png")

class VideoConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Video to Audio Converter by Zihad Hasan")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(600, 500)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        # --- Font Setup ---
        self.title_font = self.get_font(size=28, weight="bold")
        self.button_font = self.get_font(size=16, weight="bold")
        self.label_font = self.get_font(size=14)
        self.footer_font = self.get_font(size=10)

        # --- Load Icons ---
        self.select_files_icon = self.load_icon(SELECT_FILES_ICON_PATH)
        self.select_folder_icon = self.load_icon(SELECT_FOLDER_ICON_PATH)
        self.convert_icon = self.load_icon(CONVERT_ICON_PATH)

        # --- Member Variables ---
        self.video_files = []
        self.destination_folder = ""

        # --- Main Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- UI Components ---
        self.create_widgets()

    def get_font(self, size=FONT_SIZE, weight="normal"):
        try:
            if FONT_FAMILY in tkfont.families():
                return ctk.CTkFont(family=FONT_FAMILY, size=size, weight=weight)
            return ctk.CTkFont(family=FALLBACK_FONT, size=size, weight=weight)
        except Exception:
            return ctk.CTkFont(family=FALLBACK_FONT, size=size, weight=weight)

    def load_icon(self, path):
        try:
            return ctk.CTkImage(Image.open(path), size=(24, 24))
        except FileNotFoundError:
            print(f"Icon not found at {path}. Please ensure the file exists.")
            return None

    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        title_label = ctk.CTkLabel(self.main_frame, text="Video to Audio Converter", font=self.title_font, text_color=("#333", "#EEE"))
        title_label.grid(row=0, column=0, pady=(30, 15), sticky="n")

        top_button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_button_frame.grid(row=1, column=0, sticky="ew", pady=10, padx=20)
        top_button_frame.grid_columnconfigure((0, 1), weight=1)

        self.select_files_button = ctk.CTkButton(top_button_frame, text="Select Videos", image=self.select_files_icon, compound="left", command=self.select_video_files, font=self.button_font, corner_radius=8)
        self.select_files_button.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")

        self.select_dest_button = ctk.CTkButton(top_button_frame, text="Select Destination", image=self.select_folder_icon, compound="left", command=self.select_destination_folder, font=self.button_font, corner_radius=8)
        self.select_dest_button.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="ew")

        self.file_list_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Selected Files", label_font=self.label_font, corner_radius=8)
        self.file_list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.dest_path_label = ctk.CTkLabel(self.main_frame, text="Destination: Not Selected", font=self.label_font)
        self.dest_path_label.grid(row=3, column=0, pady=10, padx=20, sticky="ew")

        bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        bottom_frame.grid(row=4, column=0, sticky="ew", pady=10, padx=20)
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.start_button = ctk.CTkButton(bottom_frame, text="Start Conversion", image=self.convert_icon, compound="left", command=self.start_conversion_thread, font=self.button_font, corner_radius=8)
        self.start_button.grid(row=0, column=0, pady=10, sticky="ew")

        self.progress_bar = ctk.CTkProgressBar(bottom_frame)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, pady=10, sticky="ew")

        self.status_label = ctk.CTkLabel(bottom_frame, text="Ready", font=self.label_font)
        self.status_label.grid(row=2, column=0, pady=10, sticky="ew")

        footer_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        footer_frame.grid(row=5, column=0, sticky="sew", pady=(20, 0))
        footer_frame.grid_columnconfigure(0, weight=1)

        branding_label = ctk.CTkLabel(footer_frame, text="Created by Zihad Hasan", font=self.footer_font)
        branding_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.appearance_mode_menu = ctk.CTkOptionMenu(footer_frame, values=["Light", "Dark", "System"], command=ctk.set_appearance_mode, font=self.label_font)
        self.appearance_mode_menu.grid(row=0, column=1, padx=15, pady=10, sticky="e")

    def select_video_files(self):
        self.video_files = filedialog.askopenfilenames(title="Select Video Files", filetypes=([("Video Files", "*.mp4 *.mkv *.avi *.mov"), ("All files", "*.*")]))
        self.update_file_listbox()

    def update_file_listbox(self):
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
        for file_path in self.video_files:
            file_name = os.path.basename(file_path)
            label = ctk.CTkLabel(self.file_list_frame, text=file_name, font=self.label_font)
            label.pack(anchor="w", padx=10, pady=5)

    def select_destination_folder(self):
        self.destination_folder = filedialog.askdirectory(title="Select Destination Folder")
        if self.destination_folder:
            self.dest_path_label.configure(text=f"Destination: {self.destination_folder}")

    def start_conversion_thread(self):
        if not self.video_files or not self.destination_folder:
            messagebox.showerror("Error", "Please select video files and a destination folder.")
            return
        self.set_ui_state("disabled")
        threading.Thread(target=self.run_conversion, daemon=True).start()

    def run_conversion(self):
        total_files = len(self.video_files)
        for i, video_path in enumerate(self.video_files):
            file_name = os.path.basename(video_path)
            self.update_status(f"Converting file {i+1} of {total_files}: {file_name}...")
            try:
                with VideoFileClip(video_path) as video:
                    audio_path = os.path.join(self.destination_folder, f"{os.path.splitext(file_name)[0]}.mp3")
                    video.audio.write_audiofile(audio_path, logger=None)
            except Exception as e:
                self.update_status(f"Error converting {file_name}: {e}")
                continue
            self.animate_progress((i + 1) / total_files)
        self.update_status(f"Conversion complete! {total_files} files converted.")
        self.set_ui_state("normal")

    def update_status(self, message):
        self.after(0, lambda: self.status_label.configure(text=message))

    def animate_progress(self, target_value, current_value=0, step=0.01):
        current_value = self.progress_bar.get()
        if current_value < target_value:
            new_value = min(current_value + step, target_value)
            self.progress_bar.set(new_value)
            if new_value < target_value:
                self.after(10, self.animate_progress, target_value)

    def set_ui_state(self, state):
        self.start_button.configure(state=state)
        self.select_files_button.configure(state=state)
        self.select_dest_button.configure(state=state)

if __name__ == "__main__":
    app = VideoConverterApp()
    app.mainloop()