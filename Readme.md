# Automated Downloads Organizer (Python)

A Python-based **background automation tool** that monitors the Windows **Downloads** folder in real time and automatically organizes files into categorized folders based on file type.

Built using **Watchdog**, **Pathlib**, and **Shutil**, this project demonstrates efficient, low-resource, event-driven file system automation.

---

##  Features

- Automatically sorts downloaded files by type  
- Monitors the Downloads folder in **real time** (event-based, low CPU usage)  
- Organizes files into categorized folders:
  - Images  
  - Audio  
  - Videos  
  - Documents  
  - Archives  
  - Code  
  - Software  
  - Others  
- Creates folders automatically if they do not exist  
- Sorts existing files on startup  
- Runs silently in the background using `.pyw` (no terminal window)  
- Supports auto-start on Windows boot  
- Safely handles missing or moved files without crashing  

---

## Why This Project?

The Downloads folder is one of the most commonly cluttered locations on a system.  
Manually organizing downloaded files is repetitive, time-consuming, and error-prone.

This project solves that real-world productivity problem by:

- Continuously watching the Downloads folder  
- Detecting file types automatically  
- Organizing files instantly without user interaction  

Beyond functionality, this project demonstrates **practical Python engineering**, including background execution, OS-level automation, and event-driven programming — not just theoretical scripting.

---

## Technologies Used
- **Python 3**
- **Watchdog** — File system event monitoring
- **Pathlib** — Modern and safe path handling
- **OS & Shutil** — File operations and directory management
- **Windows OS** — Startup and background execution

---

##  How It Works

1. Scans existing files in the Downloads folder on startup  
2. Identifies file extensions  
3. Maps each file to a category folder  
4. Creates category folders if missing  
5. Moves files safely to their respective folders  
6. Starts a Watchdog observer  
7. Listens for new downloads in real time  
8. Automatically sorts new files as soon as they appear  

---

##  How to Run

###  Run manually (for testing)

Execute the script using Python to verify correct behavior:


python downloads_sorter.py

### Run silently in the background 

Rename the file:

downloads_sorter.py → downloads_sorter.pyw
 Auto-Start on Windows 

### 
Press Win + R
Type:
shell:startup

Copy the .pyw file into the Startup folder

The script will now start automatically every time Windows boots.

### Supported File Categories
Category:	File Types
Images:	jpg, jpeg, png, gif, webp
Audio:	mp3, wav, aac
Video:	mp4, mkv, mov
Documents:	pdf, docx, txt
Archives:	zip, rar, 7z
Code:	py, js, html
Software:	exe, apk
Others:	uncategorized

### Future Improvements

1. Activity logging to file
2. Desktop notifications
3. Duplicate-file handling
4. GUI interface
5. AI-based smart file classification
6. Conversion to .exe installer