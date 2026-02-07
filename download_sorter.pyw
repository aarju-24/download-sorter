import time
import logging
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# =====================================================
# BOOT DELAY (let Windows settle)
# =====================================================
time.sleep(15)

# =====================================================
# LOGGING (absolute path)
# =====================================================
LOG_FILE = r"D:\startup_log.txt"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("DOWNLOAD SORTER STARTED")

# =====================================================
# TARGET FOLDER
# =====================================================
DOWNLOADS = Path(r"C:\Users\arzoo\Downloads")

if not DOWNLOADS.exists():
    logging.error("Downloads folder not found")
    raise SystemExit

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
# SAFE FILE READY CHECK (CRITICAL FIX)
# =====================================================
def wait_until_ready(path, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with open(path, "rb"):
                return True
        except Exception:
            time.sleep(0.5)
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
# MOVE FILE (ROBUST)
# =====================================================
def move_file(path):
    try:
        file_path = Path(path)

        if not file_path.exists() or file_path.is_dir():
            return

        if not wait_until_ready(file_path):
            logging.warning(f"File not ready: {file_path.name}")
            return

        # SAFER extension detection
        extension = "".join(file_path.suffixes).lower()

        logging.info(f"Detected extension: {extension} for {file_path.name}")

        folder_name = get_folder(extension)
        destination_dir = DOWNLOADS / folder_name
        destination_dir.mkdir(exist_ok=True)

        destination = destination_dir / file_path.name

        if destination.exists():
            return  # avoid overwrite

        shutil.move(str(file_path), str(destination))
        logging.info(f"Moved: {file_path.name} -> {folder_name}")

    except Exception as e:
        logging.error(f"Error processing {path}: {e}")

# =====================================================
# SORT EXISTING FILES (ON STARTUP)
# =====================================================
logging.info("### NEW VERSION WITH IPYNB FIX IS RUNNING ###")

logging.info("Sorting existing files on startup")

for item in DOWNLOADS.iterdir():
    move_file(item)

# =====================================================
# WATCHDOG HANDLER
# =====================================================
class FolderHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            move_file(event.src_path)

# =====================================================
# START WATCHDOG
# =====================================================
observer = Observer()
observer.schedule(FolderHandler(), str(DOWNLOADS), recursive=False)
observer.start()

logging.info("Watching Downloads folder in real time")

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
