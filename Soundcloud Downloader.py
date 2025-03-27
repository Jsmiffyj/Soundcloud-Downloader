import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter.ttk import Progressbar, Style, Combobox
import time

def download_audio():
    # Clear any previous status messages before starting a new download
    status_text.set("Downloading...")  # Initial status message
    progress_bar['value'] = 0
    root.update_idletasks()

    # Get URLs and check for validity
    urls = url_entry.get("1.0", tk.END).strip().split("\n")
    if not urls or urls == ['']:
        messagebox.showwarning("Warning", "Please enter at least one SoundCloud URL.")
        return
    
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        return
    
    selected_format = format_var.get()

    total_urls = len(urls)
    for index, url in enumerate(urls, start=1):
        if url.strip():
            command = f'yt-dlp -o "{output_folder}/%(title)s.%(ext)s" --embed-thumbnail --embed-metadata -f bestaudio "{url}" '
            subprocess.run(command, shell=True)
            progress_bar['value'] = (index / total_urls) * 100
            root.update_idletasks()

    convert_audio(output_folder, selected_format)
    
    # Reset status text to 'Download and conversion complete!' after process finishes
    status_text.set("Download and conversion complete!")
    
    # Only show the completion message box once
    if not hasattr(download_audio, "completed"):
        messagebox.showinfo("Done", "Download and conversion complete!")
        download_audio.completed = True  # Mark as completed

# Reset the flag when a new download is started
def reset_download():
    # Clear previous status and reset completion flag
    status_text.set("Ready")
    download_audio.completed = False  # Reset the flag for new download
    progress_bar['value'] = 0


def convert_audio(output_folder, selected_format):
    for file in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file)
        
        # Check for the file format and whether it's already converted
        if file.endswith(".opus") or file.endswith(".aac"):
            new_file = file_path.rsplit(".", 1)[0] + f".{selected_format}"
            
            # Check if the new file already exists, if it does, add a suffix
            if os.path.exists(new_file):
                timestamp = time.strftime("%Y%m%d%H%M%S")
                new_file = file_path.rsplit(".", 1)[0] + f"_{timestamp}.{selected_format}"
            
            subprocess.run(f'ffmpeg -i "{file_path}" -ar 44100 -ac 2 -q:a 0 -map_metadata 0:s:a:0 "{new_file}"', shell=True)
            os.remove(file_path)
            
            if selected_format == "mp3":
                thumbnail = new_file.replace(".mp3", ".png")
                if os.path.exists(thumbnail):
                    final_mp3 = new_file.replace(".mp3", "_with_thumbnail.mp3")
                    subprocess.run(f'ffmpeg -i "{new_file}" -i "{thumbnail}" -map 0 -map 1 -c copy -id3v2_version 3 "{final_mp3}"', shell=True)
                    os.remove(new_file)
                    os.rename(final_mp3, new_file)
                    os.remove(thumbnail)

# GUI Setup
root = tk.Tk()
root.title("SoundCloud Downloader")
root.geometry("500x400")
root.resizable(False, False)

style = Style()
style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
style.configure("TLabel", font=("Arial", 10))

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=20)

tk.Label(frame, text="Enter SoundCloud URLs (one per line):", font=("Arial", 12, "bold")).pack()
url_entry = scrolledtext.ScrolledText(frame, height=5, width=50)
url_entry.pack()

tk.Label(frame, text="Select Output Format:", font=("Arial", 10, "bold")).pack(pady=5)
format_var = tk.StringVar()
format_combobox = Combobox(frame, textvariable=format_var, values=["mp3", "wav", "flac", "aiff", "aac", "opus"], state="readonly")
format_combobox.set("mp3")  # Default selection
format_combobox.pack()

download_button = tk.Button(frame, text="Download", command=download_audio, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
download_button.pack(pady=5)

status_text = tk.StringVar()
status_text.set("Ready")
status_label = tk.Label(frame, textvariable=status_text, font=("Arial", 10, "italic"))
status_label.pack()

progress_bar = Progressbar(frame, length=400, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()
