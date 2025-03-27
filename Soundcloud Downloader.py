import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter.ttk import Progressbar, Style, Combobox

# Function to get available audio formats
def get_audio_formats(url, oauth_token):
    try:
        command = f'yt-dlp -F "{url}"'
        if oauth_token:
            command += f' --add-header "Authorization: OAuth {oauth_token}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        formats = result.stdout.split("\n")
        formatted_output = "\n".join([line for line in formats if line.strip() and not line.startswith("[info]")])
        return formatted_output
    except Exception as e:
        return f"Error fetching formats: {str(e)}"

# Function to display available formats
def show_audio_formats():
    url = url_entry.get("1.0", tk.END).strip().split("\n")[0]
    oauth_token = oauth_entry.get().strip()
    if not url:
        return

    formats = get_audio_formats(url, oauth_token)

    format_window = tk.Toplevel(root)
    format_window.title("Available Formats")
    format_window.geometry("600x400")
    format_window.resizable(True, True)

    text_area = scrolledtext.ScrolledText(format_window, wrap=tk.WORD, height=20, width=70)
    text_area.insert(tk.END, formats)
    text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
    text_area.config(state=tk.DISABLED)

# Function to update progress bar smoothly
def update_progress(value):
    progress_bar["value"] = value
    root.update_idletasks()

# Function to handle audio download
def download_audio():
    threading.Thread(target=download_audio_thread, daemon=True).start()

def download_audio_thread():
    urls = url_entry.get("1.0", tk.END).strip().split("\n")
    oauth_token = oauth_entry.get().strip()
    if not urls or urls == [""]:
        return

    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        return

    selected_format = format_var.get()
    progress_bar["value"] = 0
    status_text.set("Downloading...")
    root.update_idletasks()

    total_urls = len(urls)
    for index, url in enumerate(urls, start=1):
        if url.strip():
            # Download best available audio quality
            command = f'yt-dlp -o "{output_folder}/%(title)s.%(ext)s" --embed-thumbnail --embed-metadata -f bestaudio "{url}"'
            if oauth_token:
                command += f' --add-header "Authorization: OAuth {oauth_token}"'
            subprocess.run(command, shell=True)

            update_progress((index / total_urls) * 100)

    convert_audio(output_folder, selected_format)
    status_text.set("Download & Conversion Complete")

# Function to convert audio files
def convert_audio(output_folder, selected_format):
    for file in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file)

        if file.endswith((".m4a", ".opus", ".flac", ".aiff", ".aac")):
            new_file = file_path.rsplit(".", 1)[0] + f".{selected_format}"
            conversion_command = f'ffmpeg -i "{file_path}" -ar 44100 -ac 2 -q:a 0 -map_metadata 0 "{new_file}"'
            subprocess.run(conversion_command, shell=True)
            os.remove(file_path)
            file_path = new_file  # Update file path to converted file

        # Embed thumbnail
        if file_path.endswith(selected_format):
            base_name = file_path.rsplit(".", 1)[0]
            for ext in [".png", ".jpg"]:
                thumbnail_path = base_name + ext
                if os.path.exists(thumbnail_path):
                    try:
                        subprocess.run(f'ffmpeg -i "{file_path}" -i "{thumbnail_path}" -map 0:a -map 1:v -c:a copy -c:v mjpeg -map_metadata 0 -id3v2_version 3 "{file_path}"', shell=True)
                        os.remove(thumbnail_path)  # Remove thumbnail after embedding
                        break
                    except Exception as e:
                        print(f"Error embedding thumbnail: {str(e)}")
                        continue

# GUI Setup
root = tk.Tk()
root.title("SoundCloud Downloader")
root.geometry("520x520")
root.configure(bg="#2c3e50")  # Dark background
root.resizable(False, False)

style = Style()
style.configure("TButton", font=("Arial", 10, "bold"), padding=6, background="#3498db", foreground="white")
style.configure("TLabel", font=("Arial", 10, "bold"), background="#2c3e50", foreground="white")

frame = tk.Frame(root, padx=10, pady=10, bg="#2c3e50")
frame.pack(pady=15)

#Soundcloud URL Input Box
tk.Label(frame, text="Enter SoundCloud URLs (one per line):", font=("Arial", 12, "bold"), bg="#2c3e50", fg="white").pack()
url_entry = scrolledtext.ScrolledText(frame, height=5, width=55, bg="#34495e", fg="white", insertbackground="white")
url_entry.pack(pady=5)

#Enter OAuth Token Input Box
tk.Label(frame, text="Enter OAuth Token (optional):", font=("Arial", 10, "bold"), bg="#2c3e50", fg="white").pack(pady=5)
oauth_entry = tk.Entry(frame, show="*", bg="#34495e", fg="white", insertbackground="white")
oauth_entry.pack()

#Select Output Format Dropdown
tk.Label(frame, text="Select Output Format:", font=("Arial", 10, "bold"), bg="#2c3e50", fg="white").pack(pady=5)
format_var = tk.StringVar()
format_combobox = Combobox(frame, textvariable=format_var, values=["mp3", "wav", "flac", "aiff", "aac", "opus"], state="readonly")
format_combobox.set("mp3")
format_combobox.pack()

#Show Available Formats Button
formats_button = tk.Button(frame, text="Show Available Formats", command=show_audio_formats, font=("Arial", 10, "bold"), bg="#e67e22", fg="white", relief="flat")
formats_button.pack(pady=10)

#Download Button
download_button = tk.Button(frame, text="Download", command=download_audio, font=("Arial", 12, "bold"), bg="#27ae60", fg="white", relief="flat")
download_button.pack(pady=5)

#Download/Conversion Status
status_text = tk.StringVar()
status_text.set("Ready")
status_label = tk.Label(frame, textvariable=status_text, font=("Arial", 10, "italic"), bg="#2c3e50", fg="white")
status_label.pack()

#Progress Bar
progress_bar = Progressbar(frame, length=420, mode="determinate", style="Horizontal.TProgressbar")
progress_bar.pack(pady=10)

style.configure("Horizontal.TProgressbar", background="#1abc9c", troughcolor="#34495e", thickness=10)

root.mainloop()
