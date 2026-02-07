import time
import logging
import os
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# =========================
# BOOT DELAY (CRITICAL)
# =========================
time.sleep(15)  # wait for Windows to fully start

# =========================
# LOGGING (ABSOLUTE PATH)
# =========================
LOG_FILE = r"D:\startup_log.txt"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("DOWNLOAD SORTER STARTED")

# =========================
# TARGET FOLDER
# =========================
folder_path = Path(r"C:\Users\arzoo\Downloads")

if not folder_path.exists():
    logging.error("Downloads folder not found")
    raise SystemExit

# =========================
# EXTENSION GROUPS
# =========================
image_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"}
audio_exts = {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"}
video_exts = {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv"}
doc_exts = {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"}
sheet_exts = {".xls", ".xlsx", ".csv"}
presentation_exts = {".ppt", ".pptx"}
code_exts = {".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json", ".sql",".ipynb"}
archive_exts = {".zip", ".rar", ".7z", ".tar", ".gz"}
software_exts = {".exe", ".msi", ".apk"}
design_exts = {".psd", ".ai", ".fig", ".xd"}
ebook_exts = {".epub", ".mobi", ".azw"}
database_exts = {".db", ".sqlite", ".mdb"}

# =========================
# FOLDER DECIDER
# =========================
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

# =========================
# MOVE FILE
# =========================
def move_file(file_path):
    try:
        file_path = Path(file_path)

        if not file_path.exists() or file_path.is_dir():
            return

        folder_name = get_folder(file_path.suffix.lower())
        destination_folder = folder_path / folder_name
        destination_folder.mkdir(exist_ok=True)

        destination = destination_folder / file_path.name
        shutil.move(str(file_path), str(destination))

        logging.info(f"Moved: {file_path.name} -> {folder_name}")

    except Exception as e:
        logging.error(f"Error moving file: {e}")

# =========================
# SORT EXISTING FILES
# =========================
logging.info("Sorting existing files")
for file in folder_path.glob("*"):
    move_file(file)

# =========================
# WATCHDOG HANDLER
# =========================
class FolderHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(2)
            move_file(event.src_path)

observer = Observer()
observer.schedule(FolderHandler(), str(folder_path), recursive=False)
observer.start()

logging.info("Watching Downloads folder")

# =========================
# KEEP ALIVE
# =========================
try:
    while True:
        time.sleep(1)
except Exception as e:
    logging.error(f"Watcher crashed: {e}")
    observer.stop()

observer.join()
