import os
import shutil
from datetime import datetime
from tkinter import*
from tkinter import ttk, messagebox
from tkinter.font import Font

file_types ={
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.doc'],
    'Audio': ['.mp3', '.wav', '.m4a','mov'],
    'Videos': ['.mp4', '.mkv', '.avi'],
    'Compressed': ['.zip', '.rar', '.tar'],
    'Archives': ['.7z','.rar','.tar','.gz'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Code': ['.py', '.java', '.css', '.js', '.html', '.cpp', '.c'],
}

log_entries = []

def move_file(src_path, base_path, folder_name):
    target_folder = os.path.join(base_path, folder_name)
    os.makedirs(target_folder, exist_ok=True)

    file_name, file_ext = os.path.splitext(os.path.basename(src_path))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_file_name = f"{file_name}_{timestamp}{file_ext}"
    new_path = os.path.join(target_folder, new_file_name)

    shutil.move(src_path, new_path)
    log_entries.append(f"Moved: {src_path} -> {new_path}")

def organize_files(path):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if not os.path.isfile(file_path):
            continue

        file_ext = os.path.splitext(file_name)[1].lower()
        moved = False

        for folder, extensions in file_types.items():
            if file_ext in extensions:
                move_file(file_path, path, folder)
                moved = True
                break
        if not moved:
            move_file(file_path, path, 'Others')

            log_path = os.path.join(path, 'organizer_log.txt')
            with open(log_path, 'w') as log_file:
                log_file.write("\n".join(log_entries))

def run_organizer():
    download_path = os.path.expanduser("~/Downloads")
    organize_files
    messagebox.showinfo("File Organizer", "✅ Downloads folder organized successfully!")

def create_gui():
    window = Tk()
    window.title("Smart File Organizer")
    window.geometry("400x250")
    window.resizable(False, False)

    #colors
    bg_color = "#f5f5f5"
    primary_color = "#6200ee"
    secondary_color = "#03dac6"
    text_color = "#333333"

    window.configure(bg=bg_color)

    #fonts
    title_font = Font(family="Segoe UI", size=16, weight="bold")
    text_font = Font(family="Segoe UI", size=10)
    button_font = Font(family="Segoe UI", size=12, weight="bold")

    #header
    header_frame = Frame(window, bg=primary_color)
    header_frame.pack(fill=X)

    Label(header_frame,
          text="📁 Smart File Organizer",
            bg=primary_color,
            fg="white",
            padx=10,
            pady=10,
    ).pack()


    # Main Content Frame
    content_frame = Frame(window, bg=bg_color, padx=20, pady=10)
    content_frame.pack(expand=True, fill=BOTH)

    Label(content_frame,
          text="Organize your Downloads folder with one click!",
          font=text_font,
          bg=bg_color,
          fg=text_color).pack(pady=(0, 15))

    # Progress bar (will be shown during operation)
    progress = ttk.Progressbar(content_frame, orient=HORIZONTAL, length=300, mode='indeterminate')

    # Organize Button with modern style
    organize_btn = Button(content_frame,
                         text="🧹 Organize Now",
                         font=button_font,
                         bg=primary_color,
                         fg="white",
                         activebackground="#3700b3",
                         activeforeground="white",
                         bd=0,
                         padx=20,
                         pady=10,
                         command=lambda: [progress.pack(pady=10),
                                        progress.start(10),
                                        window.after(100, run_organizer),
                                        window.after(2000, lambda: [progress.stop(), progress.pack_forget()])])

    organize_btn.pack(pady=10)

    # Footer
    footer_frame = Frame(window, bg=bg_color, pady=5)
    footer_frame.pack(fill=X)

    Label(footer_frame,
          text="© 2025 Shanzitech",
          font=("Segoe UI", 8),
          bg=bg_color,
          fg="#777777").pack()

    # Hover effects
    def on_enter(e):
        organize_btn['background'] = '#3700b3'

    def on_leave(e):
        organize_btn['background'] = primary_color

    organize_btn.bind("<Enter>", on_enter)
    organize_btn.bind("<Leave>", on_leave)

    window.mainloop()

if __name__ == "__main__":
    create_gui()

