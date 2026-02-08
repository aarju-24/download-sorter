import time
import logging
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# =====================================================
# BOOT DELAY
# =====================================================
time.sleep(15)

# =====================================================
# LOGGING
# =====================================================
LOG_FILE = r"D:\startup_log.txt"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("DOWNLOAD SORTER STARTED (SAFE VERSION)")

# =====================================================
# TARGET FOLDER
# =====================================================
DOWNLOADS = Path(r"C:\Users\arzoo\Downloads")

if not DOWNLOADS.exists():
    logging.error("Downloads folder not found")
    raise SystemExit

# =====================================================
# TEMP DOWNLOAD EXTENSIONS (CRITICAL)
# =====================================================
TEMP_EXTENSIONS = {
    ".crdownload",  # Chrome
    ".part",        # Firefox
    ".tmp",         # Edge / system
    ".download"
}

# =====================================================
# EXTENSION GROUPS
# =====================================================
image_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"}
audio_exts = {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"}
video_exts = {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv"}
doc_exts = {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"}
sheet_exts = {".xls", ".xlsx", ".csv"}
presentation_exts = {".ppt", ".pptx"}
code_exts = {
    ".py", ".ipynb", ".js", ".html", ".css",
    ".java", ".cpp", ".c", ".json", ".sql"
}
archive_exts = {".zip", ".rar", ".7z", ".tar", ".gz"}
software_exts = {".exe", ".msi", ".apk"}
design_exts = {".psd", ".ai", ".fig", ".xd"}
ebook_exts = {".epub", ".mobi", ".azw"}
database_exts = {".db", ".sqlite", ".mdb"}

# =====================================================
# WAIT UNTIL FILE IS FULLY DOWNLOADED
# =====================================================
def wait_until_stable(path, timeout=60):
    last_size = -1
    start = time.time()

    while time.time() - start < timeout:
        try:
            current_size = path.stat().st_size
            if current_size == last_size:
                return True
            last_size = current_size
            time.sleep(1)
        except FileNotFoundError:
            return False

    return False

# =====================================================
# FOLDER DECIDER
# =====================================================
def get_folder(extension):
    if extension in image_exts:
        return "Images"
    if extension in audio_exts:
        return "Audio"
    if extension in video_exts:
        return "Video"
    if extension in doc_exts:
        return "Docs"
    if extension in sheet_exts:
        return "Sheets"
    if extension in presentation_exts:
        return "Presentations"
    if extension in code_exts:
        return "Code"
    if extension in archive_exts:
        return "Archives"
    if extension in software_exts:
        return "Software"
    if extension in design_exts:
        return "Design"
    if extension in ebook_exts:
        return "Ebooks"
    if extension in database_exts:
        return "Databases"
    return "Others"

# =====================================================
# MOVE FILE (SAFE)
# =====================================================
def move_file(path):
    try:
        file_path = Path(path)

        if not file_path.exists() or file_path.is_dir():
            return

        # Ignore temp download files
        if any(ext in file_path.name.lower() for ext in TEMP_EXTENSIONS):
            return

        if not wait_until_stable(file_path):
            logging.warning(f"File not stable: {file_path.name}")
            return

        extension = "".join(file_path.suffixes).lower()
        folder_name = get_folder(extension)

        destination_dir = DOWNLOADS / folder_name
        destination_dir.mkdir(exist_ok=True)

        destination = destination_dir / file_path.name
        if destination.exists():
            return

        shutil.move(str(file_path), str(destination))
        logging.info(f"Moved: {file_path.name} -> {folder_name}")

    except Exception as e:
        logging.error(f"Error processing {path}: {e}")

# =====================================================
# SORT EXISTING FILES (SAFE)
# =====================================================
logging.info("Sorting existing files on startup")

for item in DOWNLOADS.iterdir():
    move_file(item)

# =====================================================
# WATCHDOG HANDLER (IMPORTANT CHANGE)
# =====================================================
class FolderHandler(FileSystemEventHandler):
    def on_moved(self, event):
        if not event.is_directory:
            move_file(event.dest_path)

# =====================================================
# START WATCHDOG
# =====================================================
observer = Observer()
observer.schedule(FolderHandler(), str(DOWNLOADS), recursive=False)
observer.start()

logging.info("Watching Downloads folder (SAFE MODE)")

# =====================================================
# KEEP ALIVE
# =====================================================
try:
    while True:
        time.sleep(1)
except Exception as e:
    logging.error(f"Watcher crashed: {e}")
    observer.stop()

observer.join()
