print("SCRIPT STARTED")

import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ---------------- CONFIG ---------------- #

folder_path = Path("C:\\Users\\arzoo\\Downloads")

image_exts = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"]
audio_exts = [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"]
video_exts = [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv"]
doc_exts = [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"]
sheet_exts = [".xls", ".xlsx", ".csv"]
presentation_exts = [".ppt", ".pptx"]
code_exts = [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json", ".sql"]
archive_exts = [".zip", ".rar", ".7z", ".tar", ".gz"]
software_exts = [".exe", ".msi", ".apk"]
design_exts = [".psd", ".ai", ".fig", ".xd"]
ebook_exts = [".epub", ".mobi", ".azw"]
database_exts = [".db", ".sqlite", ".mdb"]

# Chrome temporary extensions
temp_exts = [".crdownload", ".tmp"]

# ---------------- LOGIC ---------------- #

def get_folder(extension):
    if extension in image_exts:
        return "Images"
    elif extension in audio_exts:
        return "Audio"
    elif extension in video_exts:
        return "Video"
    elif extension in doc_exts:
        return "Docs"
    elif extension in sheet_exts:
        return "Sheets"
    elif extension in presentation_exts:
        return "Presentations"
    elif extension in code_exts:
        return "Code"
    elif extension in archive_exts:
        return "Archives"
    elif extension in software_exts:
        return "Software"
    elif extension in design_exts:
        return "Design"
    elif extension in ebook_exts:
        return "Ebooks"
    elif extension in database_exts:
        return "Databases"
    else:
        return "Others"


def is_file_complete(path):
    """Check if file size stops changing"""
    path = Path(path)

    if not path.exists():
        return False

    size1 = path.stat().st_size
    time.sleep(2)
    size2 = path.stat().st_size

    return size1 == size2


def move_file(file_path):
    file_path = Path(file_path)

    if not file_path.exists() or file_path.is_dir():
        return

    extension = file_path.suffix.lower()

    # Ignore temporary files
    if extension in temp_exts:
        return

    folder_name = get_folder(extension)

    new_folder = folder_path / folder_name
    new_folder.mkdir(exist_ok=True)

    destination = new_folder / file_path.name

    try:
        shutil.move(str(file_path), str(destination))
        print(f"Moved: {file_path.name} → {folder_name}")
    except Exception as e:
        print(f"Error moving {file_path.name}: {e}")


# ---------------- INITIAL SORT ---------------- #

print("Sorting existing files...")

for file in folder_path.glob("*"):
    move_file(file)


# ---------------- WATCHDOG ---------------- #

class FolderHandler(FileSystemEventHandler):

    def process(self, path):
        file_path = Path(path)

        extension = file_path.suffix.lower()

        # Ignore Chrome temp files
        if extension in temp_exts:
            return

        print(f"Detected: {file_path.name}")

        # Small delay (lets Chrome settle)
        time.sleep(2)

        # Wait until file is stable
        while not is_file_complete(file_path):
            time.sleep(1)

        move_file(file_path)

    def on_created(self, event):
        if not event.is_directory:
            self.process(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.process(event.src_path)


observer = Observer()
observer.schedule(FolderHandler(), str(folder_path), recursive=False)
observer.start()

print("Watching Downloads folder in real-time...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
