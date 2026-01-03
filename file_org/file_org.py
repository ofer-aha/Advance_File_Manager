import customtkinter as ctk
import json
import os
import shutil
import hashlib
import datetime
import threading
import queue
from concurrent.futures import ThreadPoolExecutor

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

CONFIG_FILE = "config.json"
LOG_DIR = "logs"

# ---------------------------------------------------------
# Load / Save Config
# ---------------------------------------------------------
def load_config():
	if not os.path.exists(CONFIG_FILE):
		return {
			"language": "he",
			"theme_mode": "auto",
			"smart_move_threshold": 50,
			"log_retention_days": 7
		}
	with open(CONFIG_FILE, "r", encoding="utf-8") as f:
		return json.load(f)


def save_config(cfg):
	with open(CONFIG_FILE, "w", encoding="utf-8") as f:
		json.dump(cfg, f, indent=4, ensure_ascii=False)


# ---------------------------------------------------------
# Language System
# ---------------------------------------------------------
LANG = {
	"he": {
		"tab_move": "העברת/העתקת קבצים",
		"tab_undo": "ביטול העברה",
		"tab_duplicates": "כפילויות",
		"tab_hash": "בדיקת תקינות",
		"tab_settings": "הגדרות",
		"tab_logs": "לוגים",
		"title": "מנהל קבצים מתקדם",
		"smart_threshold": "סף Smart Move (MB)",
		"custom": "מותאם אישית...",
		"undo_col_action": "פעולה",
		"undo_col_src": "מקור",
		"undo_col_dst": "יעד",
		"undo_col_status": "סטטוס",
		"undo_col_time": "זמן",
		"btn_undo_selected": "Undo נבחרים",
		"btn_undo_last": "Undo אחרון",
		"btn_undo_all": "Undo הכל",
		# Move/Copy panel
		"source_folder": "תיקיית מקור:",
		"dest_folder": "תיקיית יעד:",
		"browse": "עיון",
		"operation_mode": "מצב פעולה:",
		"move_files": "העבר קבצים",
		"copy_files": "העתק קבצים",
		"multithreading": "ריבוי תהליכונים",
		"dry_run": "הרצה ניסיונית",
		"clean_empty": "נקה תיקיות ריקות",
		"group_by_ext": "קבץ לפי סיומת",
		"batch_size": "גודל אצווה:",
		"start_move": "התחל העברה",
		"start_copy": "התחל העתקה",
		# Hash panel
		"select_file": "בחר קובץ:",
		"hash_algorithm": "אלגוריתם Hash:",
		"calculate_hash": "חשב Hash",
		"calculated_hash": "Hash מחושב:",
		"compare_with": "השווה עם:",
		"check_match": "בדוק התאמה",
		"export_hash": "יצא Hash לקובץ",
		"folder": "תיקייה:",
		"algorithms": "אלגוריתמים:",
		"start_folder_hash": "התחל Hash תיקייה",
		"export_txt": "יצא TXT",
		"export_json": "יצא JSON",
		"filter": "סינון:",
		"apply": "החל",
		"clear": "נקה",
		"build_hash_tree": "בנה עץ Hash",
		"find_duplicates": "מצא כפילויות",
		"actions_on_selected": "פעולות על נבחרים:",
		"select_all_but_one": "בחר הכל מלבד 1 לקבוצה",
		"delete_selected": "מחק נבחרים",
		"move_selected": "העבר נבחרים...",
		# Compare panel
		"source_folder_compare": "תיקיית מקור:",
		"dest_folder_compare": "תיקיית יעד:",
		"start_compare": "התחל השוואה",
		"export_results": "יצא תוצאות",
		# Settings panel
		"language": "שפה / Language:",
		"theme_mode": "מצב ערכת נושא:",
		"log_retention": "שמירת לוגים (ימים):",
		"save_settings": "שמור הגדרות",
		# Logs panel
		"log_files": "קבצי לוג:",
		"refresh": "רענן",
		"delete_selected_log": "מחק נבחר",
		"log_content": "תוכן לוג:",
		# Table headers
		"path": "נתיב",
		"size": "גודל (בתים)",
		"md5": "MD5",
		"sha1": "SHA-1",
		"sha256": "SHA-256",
		"sha512": "SHA-512",
		"hash": "Hash",
		"status": "סטטוס",
		"relpath": "נתיב יחסי",
		"src_hash": "Hash מקור",
		"dst_hash": "Hash יעד",
	},
	"en": {
		"tab_move": "Move/Copy Files",
		"tab_undo": "Undo",
		"tab_duplicates": "Duplicates",
		"tab_hash": "Hash Check",
		"tab_settings": "Settings",
		"tab_logs": "Logs",
		"title": "Advanced File Manager",
		"smart_threshold": "Smart Move Threshold (MB)",
		"custom": "Custom...",
		"undo_col_action": "Action",
		"undo_col_src": "Source",
		"undo_col_dst": "Destination",
		"undo_col_status": "Status",
		"undo_col_time": "Time",
		"btn_undo_selected": "Undo Selected",
		"btn_undo_last": "Undo Last",
		"btn_undo_all": "Undo All",
		# Move/Copy panel
		"source_folder": "Source Folder:",
		"dest_folder": "Destination Folder:",
		"browse": "Browse",
		"operation_mode": "Operation Mode:",
		"move_files": "Move Files",
		"copy_files": "Copy Files",
		"multithreading": "Multithreading",
		"dry_run": "Dry Run",
		"clean_empty": "Clean Empty Folders",
		"group_by_ext": "Group by Extension",
		"batch_size": "Batch Size:",
		"start_move": "Start Move",
		"start_copy": "Start Copy",
		# Hash panel
		"select_file": "Select File:",
		"hash_algorithm": "Hash Algorithm:",
		"calculate_hash": "Calculate Hash",
		"calculated_hash": "Calculated Hash:",
		"compare_with": "Compare With:",
		"check_match": "Check Match",
		"export_hash": "Export Hash to File",
		"folder": "Folder:",
		"algorithms": "Algorithms:",
		"start_folder_hash": "Start Folder Hash",
		"export_txt": "Export TXT",
		"export_json": "Export JSON",
		"filter": "Filter:",
		"apply": "Apply",
		"clear": "Clear",
		"build_hash_tree": "Build Hash Tree",
		"find_duplicates": "Find Duplicates",
		"actions_on_selected": "Actions on selected:",
		"select_all_but_one": "Select All But 1 per Group",
		"delete_selected": "Delete Selected Files",
		"move_selected": "Move Selected Files...",
		# Compare panel
		"source_folder_compare": "Source Folder:",
		"dest_folder_compare": "Destination Folder:",
		"start_compare": "Start Compare",
		"export_results": "Export Results",
		# Settings panel
		"language": "Language / שפה:",
		"theme_mode": "Theme Mode:",
		"log_retention": "Log Retention (days):",
		"save_settings": "Save Settings",
		# Logs panel
		"log_files": "Log Files:",
		"refresh": "Refresh",
		"delete_selected_log": "Delete Selected",
		"log_content": "Log Content:",
		# Table headers
		"path": "Path",
		"size": "Size (bytes)",
		"md5": "MD5",
		"sha1": "SHA-1",
		"sha256": "SHA-256",
		"sha512": "SHA-512",
		"hash": "Hash",
		"status": "Status",
		"relpath": "Relative Path",
		"src_hash": "Source Hash",
		"dst_hash": "Destination Hash",
	}
}


# ---------------------------------------------------------
# Auto Theme Mode
# ---------------------------------------------------------
def get_auto_theme():
	hour = datetime.datetime.now().hour
	return "dark" if hour < 7 or hour >= 19 else "light"


# ---------------------------------------------------------
# Logging System
# ---------------------------------------------------------
def ensure_log_dir():
	if not os.path.exists(LOG_DIR):
		os.makedirs(LOG_DIR)


def cleanup_old_logs(retention_days):
	ensure_log_dir()
	now = datetime.datetime.now()
	for file in os.listdir(LOG_DIR):
		path = os.path.join(LOG_DIR, file)
		if os.path.isfile(path):
			mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
			if (now - mtime).days > retention_days:
				os.remove(path)


def get_today_log_file():
	ensure_log_dir()
	today = datetime.datetime.now().strftime("%Y-%m-%d")
	return os.path.join(LOG_DIR, f"{today}.log")


def write_log_to_file(text):
	with open(get_today_log_file(), "a", encoding="utf-8") as f:
		f.write(text)


# ---------------------------------------------------------
# Hash Function
# ---------------------------------------------------------
def file_hash(path):
	h = hashlib.sha256()
	with open(path, "rb") as f:
		for chunk in iter(lambda: f.read(8192), b""):
			h.update(chunk)
	return h.hexdigest()


# ---------------------------------------------------------
# Main Application
# ---------------------------------------------------------
class App(ctk.CTk):
	def __init__(self):
		super().__init__()

		# Load config
		self.cfg = load_config()
		self.lang = self.cfg["language"]

		# Theme
		if self.cfg["theme_mode"] == "auto":
			ctk.set_appearance_mode(get_auto_theme())
		else:
			ctk.set_appearance_mode(self.cfg["theme_mode"])

		ctk.set_default_color_theme("blue")

		# Window
		self.title(LANG[self.lang]["title"])
		self.geometry("1000x700")

		# Logging queue
		self.log_queue = queue.Queue()

		# Undo log (list of dicts)
		self.undo_log = []  # each: {"action","src","dst","time","status"}

		# Thread executor
		self.executor = ThreadPoolExecutor(max_workers=8)

		# Smart Move threshold
		self.smart_threshold = ctk.StringVar(value=str(self.cfg["smart_move_threshold"]))       

		# GUI vars
		self.source_path = ctk.StringVar()
		self.dest_path = ctk.StringVar()
		self.batch_size = ctk.IntVar(value=100)
		self.use_multithread = ctk.BooleanVar(value=False)
		self.use_dryrun = ctk.BooleanVar(value=False)
		self.clean_empty = ctk.BooleanVar(value=True)
		self.group_by_ext = ctk.BooleanVar(value=True)
		self.use_copy_mode = ctk.BooleanVar(value=False)  # False = Move, True = Copy

		# Tabs
		self.tabs = ctk.CTkTabview(self)
		self.tabs.pack(fill="both", expand=True)

		self.tab_move = self.tabs.add(LANG[self.lang]["tab_move"])
		self.tab_undo = self.tabs.add(LANG[self.lang]["tab_undo"])
		#self.tab_duplicates = self.tabs.add(LANG[self.lang]["tab_duplicates"])
		self.tab_hash = self.tabs.add(LANG[self.lang]["tab_hash"])
		self.tab_settings = self.tabs.add(LANG[self.lang]["tab_settings"])
		self.tab_logs = self.tabs.add(LANG[self.lang]["tab_logs"])

		# Initialize hash sub-tabs
		self.hash_tabview = ctk.CTkTabview(self.tab_hash)
		self.hash_tabview.pack(fill="both", expand=True)
		
		self.hash_tab_file = self.hash_tabview.add("File Hash")
		self.hash_tab_folder = self.hash_tabview.add("Folder Hash")
		self.hash_tab_tree = self.hash_tabview.add("Hash Tree")
		self.hash_tab_compare = self.hash_tabview.add("Compare")
		self.hash_tab_duplicates = self.hash_tabview.add("Duplicates")

		# Folder hash results storage
		self.folder_hash_results = []
		self.compare_results = []  # list of dicts: {"status", "relpath", "src_path", "dst_path", "algo", "src_hash", "dst_hash"}
		self.hash_tree_data = None  # will hold the last built JSON structure

		# Build panels
		self.build_move_panel()
		self.build_undo_panel()
		#self.build_duplicate_panel()
		self.build_hash_tab_file()
		self.build_hash_tab_folder()
		self.build_hash_tab_tree()  
		self.build_hash_tab_compare()
		self.build_hash_tab_duplicates()
		self.build_settings_panel()
		self.build_logs_panel()

		# Initialize duplicate tracking variables
		self.dup_results = []       # flat list of {"hash", "size", "path"}
		self.dup_groups = {}        # hash -> list of {"size", "path"}

		# Start log updater
		self.after(100, self.process_log_queue)

		# Cleanup logs
		cleanup_old_logs(self.cfg["log_retention_days"])

	# ---------------------------------------------------------
	# Logging
	# ---------------------------------------------------------
	def log(self, level, text):
		timestamp = datetime.datetime.now().strftime("%H:%M:%S")
		msg = f"[{timestamp}] [{level}] {text}\n"
		self.log_queue.put(msg)
		write_log_to_file(msg)

	def process_log_queue(self):
		while not self.log_queue.empty():
			msg = self.log_queue.get()
			self.move_log.insert("end", msg)
			self.move_log.see("end")
		self.after(100, self.process_log_queue)

	# ---------------------------------------------------------
	# Move Panel
	# ---------------------------------------------------------
	def build_move_panel(self):
		frame = ctk.CTkFrame(self.tab_move)
		frame.pack(fill="both", expand=True, padx=20, pady=20)

		# Source
		ctk.CTkLabel(frame, text=LANG[self.lang]["source_folder"]).grid(row=0, column=0, sticky="w")
		ctk.CTkEntry(frame, textvariable=self.source_path, width=400).grid(row=0, column=1, padx=10)
		ctk.CTkButton(frame, text=LANG[self.lang]["browse"], command=self.browse_source).grid(row=0, column=2)

		# Destination
		ctk.CTkLabel(frame, text=LANG[self.lang]["dest_folder"]).grid(row=1, column=0, sticky="w", pady=10)
		ctk.CTkEntry(frame, textvariable=self.dest_path, width=400).grid(row=1, column=1, padx=10)
		ctk.CTkButton(frame, text=LANG[self.lang]["browse"], command=self.browse_dest).grid(row=1, column=2)

		# Operation Mode (Move or Copy)
		ctk.CTkLabel(frame, text=LANG[self.lang]["operation_mode"]).grid(row=2, column=0, sticky="w")
		mode_frame = ctk.CTkFrame(frame)
		mode_frame.grid(row=2, column=1, sticky="w", padx=10)
		ctk.CTkRadioButton(mode_frame, text=LANG[self.lang]["move_files"], variable=self.use_copy_mode, value=False).pack(side="left", padx=10)
		ctk.CTkRadioButton(mode_frame, text=LANG[self.lang]["copy_files"], variable=self.use_copy_mode, value=True).pack(side="left", padx=10)

		# Smart Move Threshold
		ctk.CTkLabel(frame, text=LANG[self.lang]["smart_threshold"]).grid(row=3, column=0, sticky="w")
		self.threshold_menu = ctk.CTkOptionMenu(
			frame,
			values=["10", "25", "50", "100", "250", "500", LANG[self.lang]["custom"]],
			variable=self.smart_threshold,
			command=self.threshold_changed
		)
		self.threshold_menu.grid(row=3, column=1, sticky="w")

		# Custom threshold entry
		self.custom_threshold_entry = ctk.CTkEntry(frame, width=80)
		if self.smart_threshold.get() == LANG[self.lang]["custom"]:
			self.custom_threshold_entry.grid(row=3, column=2, padx=10)

		# Options
		opt_frame = ctk.CTkFrame(frame)
		opt_frame.grid(row=4, column=0, columnspan=3, pady=20, sticky="w")

		ctk.CTkCheckBox(opt_frame, text=LANG[self.lang]["multithreading"], variable=self.use_multithread).grid(row=0, column=0, padx=10)
		ctk.CTkCheckBox(opt_frame, text=LANG[self.lang]["dry_run"], variable=self.use_dryrun).grid(row=0, column=1, padx=10)
		ctk.CTkCheckBox(opt_frame, text=LANG[self.lang]["clean_empty"], variable=self.clean_empty).grid(row=1, column=0, padx=10)
		ctk.CTkCheckBox(opt_frame, text=LANG[self.lang]["group_by_ext"], variable=self.group_by_ext).grid(row=1, column=1, padx=10)

		ctk.CTkLabel(opt_frame, text=LANG[self.lang]["batch_size"]).grid(row=2, column=0, sticky="w", pady=10)
		ctk.CTkEntry(opt_frame, textvariable=self.batch_size, width=80).grid(row=2, column=1, sticky="w")

		# Start Button
		self.start_button = ctk.CTkButton(frame, text=LANG[self.lang]["start_move"], height=40, command=self.start_move)
		self.start_button.grid(row=5, column=0, columnspan=3, pady=20)

		# Progress Bar
		self.progress = ctk.CTkProgressBar(frame)
		self.progress.grid(row=6, column=0, columnspan=3, sticky="ew", pady=10)
		self.progress.set(0)

		# Log Window
		self.move_log = ctk.CTkTextbox(frame, height=250)
		self.move_log.grid(row=7, column=0, columnspan=3, sticky="nsew", pady=10)

		frame.grid_rowconfigure(7, weight=1)
		frame.grid_columnconfigure(1, weight=1)

	# ---------------------------------------------------------
	# Undo Panel
	# ---------------------------------------------------------
	def build_undo_panel(self):
		frame = ctk.CTkFrame(self.tab_undo)
		frame.pack(fill="both", expand=True, padx=20, pady=20)

		# Use ttk Treeview inside CTk frame
		columns = ("action", "src", "dst", "status", "time")
		self.undo_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

		self.undo_tree.heading("action", text=LANG[self.lang]["undo_col_action"])
		self.undo_tree.heading("src", text=LANG[self.lang]["undo_col_src"])
		self.undo_tree.heading("dst", text=LANG[self.lang]["undo_col_dst"])
		self.undo_tree.heading("status", text=LANG[self.lang]["undo_col_status"])
		self.undo_tree.heading("time", text=LANG[self.lang]["undo_col_time"])

		self.undo_tree.column("action", width=80, anchor="center")
		self.undo_tree.column("src", width=260)
		self.undo_tree.column("dst", width=260)
		self.undo_tree.column("status", width=80, anchor="center")
		self.undo_tree.column("time", width=100, anchor="center")

		# Scrollbars
		y_scroll = ttk.Scrollbar(frame, orient="vertical", command=self.undo_tree.yview)
		x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.undo_tree.xview)
		self.undo_tree.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)

		self.undo_tree.grid(row=0, column=0, columnspan=3, sticky="nsew")
		y_scroll.grid(row=0, column=3, sticky="ns")
		x_scroll.grid(row=1, column=0, columnspan=3, sticky="ew")

		# ---------- Progress Bar and Current File Label ----------
		progress_frame = ctk.CTkFrame(frame)
		progress_frame.grid(row=2, column=0, columnspan=4, pady=5, sticky="ew")

		self.undo_progress = ctk.CTkProgressBar(progress_frame)
		self.undo_progress.pack(fill="x", padx=5, pady=5)
		self.undo_progress.set(0)

		self.undo_current_file = ctk.CTkLabel(progress_frame, text="", anchor="w")
		self.undo_current_file.pack(fill="x", padx=5, pady=2)

		# Buttons
		btn_frame = ctk.CTkFrame(frame)
		btn_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky="w")

		self.btn_undo_selected = ctk.CTkButton(
			btn_frame,
			text=LANG[self.lang]["btn_undo_selected"],
			command=self.undo_selected
		)
		self.btn_undo_selected.grid(row=0, column=0, padx=10)

		self.btn_undo_last = ctk.CTkButton(
			btn_frame,
			text=LANG[self.lang]["btn_undo_last"],
			command=self.undo_last
		)
		self.btn_undo_last.grid(row=0, column=1, padx=10)

		self.btn_undo_all = ctk.CTkButton(
			btn_frame,
			text=LANG[self.lang]["btn_undo_all"],
			command=self.undo_all
		)
		self.btn_undo_all.grid(row=0, column=2, padx=10)

		frame.grid_rowconfigure(0, weight=1)
		frame.grid_columnconfigure(0, weight=1)

	# ---------------------------------------------------------
	# Threshold change
	# ---------------------------------------------------------
	def threshold_changed(self, value):
		if value == LANG[self.lang]["custom"]:
			self.custom_threshold_entry.grid(row=3, column=2, padx=10)
		else:
			self.custom_threshold_entry.grid_forget()

	# ---------------------------------------------------------
	# Browse
	# ---------------------------------------------------------
	def browse_source(self):
		path = filedialog.askdirectory()
		if path:
			self.source_path.set(path)

	def browse_dest(self):
		path = filedialog.askdirectory()
		if path:
			self.dest_path.set(path)

	# ---------------------------------------------------------
	# Start Move
	# ---------------------------------------------------------
	def start_move(self):
		src = self.source_path.get()
		dst = self.dest_path.get()

		if not src or not dst:
			self.log("ERROR", "Source or destination missing.")
			return

		# Determine threshold
		if self.smart_threshold.get() == LANG[self.lang]["custom"]:
			try:
				threshold = int(self.custom_threshold_entry.get())
			except Exception:
				self.log("ERROR", "Invalid custom threshold.")
				return
		else:
			threshold = int(self.smart_threshold.get())

		self.cfg["smart_move_threshold"] = threshold
		save_config(self.cfg)

		# Update button text based on mode
		mode = "Copy" if self.use_copy_mode.get() else "Move"
		self.start_button.configure(text=f"Start {mode}")
		
		self.log("INFO", f"Starting {mode.lower()}. Threshold={threshold}MB")

		threading.Thread(target=self.move_worker, args=(src, dst, threshold), daemon=True).start()

	# ---------------------------------------------------------
	# Move Worker
	# ---------------------------------------------------------
	def move_worker(self, src, dst, threshold):
		files = []
		for root, dirs, filenames in os.walk(src):
			for f in filenames:
				files.append(os.path.join(root, f))

		total = len(files)
		if total == 0:
			self.log("WARN", "No files found.")
			return

		mode = "Copy" if self.use_copy_mode.get() else "Move"
		self.log("INFO", f"Found {total} files.")
		count = 0

		for fpath in files:
			rel = os.path.relpath(fpath, src)
			ext = os.path.splitext(fpath)[1].lower().replace(".", "") or "OTHER"

			# Batch by extension
			if self.group_by_ext.get():
				target_dir = os.path.join(dst, ext.upper())
			else:
				target_dir = dst

			fname = os.path.basename(fpath)
			target_path = os.path.join(target_dir, fname)

			size_mb = os.path.getsize(fpath) / (1024 * 1024)

			if self.use_dryrun.get():
				self.log("DETAIL", f"DryRun: {fpath} → {target_path}")
			else:
				os.makedirs(target_dir, exist_ok=True)
				if self.use_copy_mode.get():
					# Copy mode - always copy with hash verification
					self.copy_file(fpath, target_path)
				else:
					# Move mode - use smart move logic
					if size_mb >= threshold:
						self.smart_move_large(fpath, target_path)
					else:
						self.smart_move_small(fpath, target_path)

			count += 1
			self.progress.set(count / total)

		# Only clean empty folders in move mode
		if not self.use_copy_mode.get() and self.clean_empty.get() and not self.use_dryrun.get():
			self.clean_empty_folders(src)

		self.log("INFO", f"{mode} completed.")

	# ---------------------------------------------------------
	# Smart Move Logic
	# ---------------------------------------------------------
	def add_undo_entry(self, action, src, dst):
		"""
		src = original location
		dst = new location
		"""
		ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		entry = {
			"action": action,
			"src": src,
			"dst": dst,
			"time": ts,
			"status": "Done"
		}
		self.undo_log.append(entry)

		idx = len(self.undo_log) - 1
		self.undo_tree.insert(
			"",
			"end",
			iid=str(idx),
			values=(entry["action"], entry["src"], entry["dst"], entry["status"], entry["time"])
		)

	def update_undo_tree_row(self, index):
		if 0 <= index < len(self.undo_log):
			e = self.undo_log[index]
			self.undo_tree.item(
				str(index),
				values=(e["action"], e["src"], e["dst"], e["status"], e["time"])
			)

	def smart_move_large(self, src, dst):
		try:
			# If target exists, change name to avoid overwrite
			final_dst = self.safe_target_path(dst)
			shutil.move(src, final_dst)
			self.log("INFO", f"MOVE: {src} → {final_dst}")
			self.add_undo_entry("move", src, final_dst)
		except Exception as e:
			self.log("ERROR", f"Move failed: {src} → {e}")

	def smart_move_small(self, src, dst):
		try:
			final_dst = self.safe_target_path(dst)
			shutil.copy2(src, final_dst)
			h1 = file_hash(src)
			h2 = file_hash(final_dst)

			if h1 == h2:
				os.remove(src)
				self.log("INFO", f"COPY+HASH+DELETE: {src} → {final_dst}")
				self.add_undo_entry("copy_delete", src, final_dst)
			else:
				self.log("WARN", f"Hash mismatch: {src}")
				# leave both files, do not log undo
		except Exception as e:
			self.log("ERROR", f"Copy failed: {src} → {e}")

	def copy_file(self, src, dst):
		"""Copy file with hash verification but keep source file"""
		try:
			final_dst = self.safe_target_path(dst)
			shutil.copy2(src, final_dst)
			h1 = file_hash(src)
			h2 = file_hash(final_dst)

			if h1 == h2:
				self.log("INFO", f"COPY+HASH: {src} → {final_dst}")
				self.add_undo_entry("copy", src, final_dst)
			else:
				self.log("WARN", f"Hash mismatch: {src} - Removing destination copy")
				# Remove the bad copy
				if os.path.exists(final_dst):
					os.remove(final_dst)
		except Exception as e:
			self.log("ERROR", f"Copy failed: {src} → {e}")

	def safe_target_path(self, dst):
		"""
		If dst exists, append _1, _2, ... before extension.
		"""
		base, ext = os.path.splitext(dst)
		candidate = dst
		counter = 1
		while os.path.exists(candidate):
			candidate = f"{base}_({counter}){ext}"
			counter += 1
		return candidate

	# ---------------------------------------------------------
	# Clean Empty Folders
	# ---------------------------------------------------------
	def clean_empty_folders(self, root):
		for dirpath, dirnames, filenames in os.walk(root, topdown=False):
			if not dirnames and not filenames:
				try:
					os.rmdir(dirpath)
					self.log("DETAIL", f"Removed empty folder: {dirpath}")
				except Exception:
					pass

	# ---------------------------------------------------------
	# Undo Logic
	# ---------------------------------------------------------
	def undo_entry(self, index):
		if not (0 <= index < len(self.undo_log)):
			return

		entry = self.undo_log[index]
		if entry["status"] != "Done":
			# already undone or failed before
			return

		action = entry["action"]
		src = entry["src"]  # original location
		dst = entry["dst"]  # current location

		if self.use_dryrun.get():
			self.log("WARN", f"Undo skipped (DryRun): {dst} → {src}")
			return

		if not os.path.exists(dst):
			self.log("WARN", f"Undo failed (missing file): {dst}")
			entry["status"] = "Missing"
			self.update_undo_tree_row(index)
			return

		try:
			if action == "copy":
				# For copy operations, just delete the destination file
				os.remove(dst)
				self.log("INFO", f"UNDO COPY: Deleted {dst}")
				entry["status"] = "Undone"
				self.update_undo_tree_row(index)
			else:
				# For move operations, move the file back
				final_src = src
				if os.path.exists(final_src):
					# original place taken - create restored path
					base, ext = os.path.splitext(src)
					final_src = self.safe_target_path(base + "_restored" + ext)

				shutil.move(dst, final_src)
				self.log("INFO", f"UNDO: {dst} → {final_src}")
				entry["status"] = "Undone"
				entry["src"] = final_src  # update original path for record
				self.update_undo_tree_row(index)
		except Exception as e:
			self.log("ERROR", f"Undo failed: {dst} → {src} ({e})")
			entry["status"] = "Error"
			self.update_undo_tree_row(index)

	def undo_selected(self):
		selected = self.undo_tree.selection()
		if not selected:
			self.log("WARN", "No undo items selected.")
			return

		# Work from last to first to reduce side effects
		indices = sorted([int(iid) for iid in selected], reverse=True)
		for idx in indices:
			self.undo_entry(idx)

	def undo_last(self):
		if not self.undo_log:
			self.log("WARN", "No undo entries.")
			return

		# last index with status "Done"
		for idx in range(len(self.undo_log) - 1, -1, -1):
			if self.undo_log[idx]["status"] == "Done":
				self.undo_entry(idx)
				return
		self.log("WARN", "No undoable entries left.")

	def undo_all(self):
		if not self.undo_log:
			self.log("WARN", "No undo entries.")
			return

		# undo all "Done" entries from last to first
		any_done = False
		for idx in range(len(self.undo_log) - 1, -1, -1):
			if self.undo_log[idx]["status"] == "Done":
				self.undo_entry(idx)
				any_done = True

		if not any_done:
			self.log("WARN", "No undoable entries left.")
	# ---------------------------------------------------------
	# Hash Check Panel
	# ---------------------------------------------------------
	def build_hash_tab_file(self):
		frame = ctk.CTkFrame(self.hash_tab_file)
		frame.pack(fill="both", expand=True, padx=20, pady=20)

		# ---------- File selection ----------
		ctk.CTkLabel(frame, text=LANG[self.lang]["select_file"]).grid(row=0, column=0, sticky="w", pady=10)
		self.hash_file_path = ctk.StringVar()

		ctk.CTkEntry(frame, textvariable=self.hash_file_path, width=400).grid(row=0, column=1, padx=10, sticky="w")
		ctk.CTkButton(frame, text=LANG[self.lang]["browse"], command=self.browse_hash_file).grid(row=0, column=2, padx=10)

		# ---------- Hash algorithm selection ----------
		ctk.CTkLabel(frame, text=LANG[self.lang]["hash_algorithm"]).grid(row=1, column=0, sticky="w", pady=10)
		self.hash_algo_var = ctk.StringVar(value="SHA-256")

		ctk.CTkOptionMenu(
			frame,
			values=["MD5", "SHA-1", "SHA-256", "SHA-512"],
			variable=self.hash_algo_var
		).grid(row=1, column=1, sticky="w", padx=10)

		# ---------- Calculate button ----------
		ctk.CTkButton(frame, text=LANG[self.lang]["calculate_hash"], command=self.calculate_file_hash).grid(
			row=2, column=0, columnspan=3, pady=20
		)

		# ---------- Calculated hash ----------
		ctk.CTkLabel(frame, text=LANG[self.lang]["calculated_hash"]).grid(row=3, column=0, sticky="nw")
		self.hash_result_box = ctk.CTkTextbox(frame, height=80, width=600)
		self.hash_result_box.grid(row=3, column=1, columnspan=2, pady=10, sticky="nsew")

		# ---------- Compare with ----------
		ctk.CTkLabel(frame, text=LANG[self.lang]["compare_with"]).grid(row=4, column=0, sticky="nw")
		self.hash_compare_box = ctk.CTkTextbox(frame, height=80, width=600)
		self.hash_compare_box.grid(row=4, column=1, columnspan=2, pady=10, sticky="nsew")

		# ---------- Compare + Export buttons ----------
		btn_frame = ctk.CTkFrame(frame)
		btn_frame.grid(row=5, column=0, columnspan=3, pady=15, sticky="w")

		ctk.CTkButton(btn_frame, text=LANG[self.lang]["check_match"], command=self.compare_file_hashes).grid(row=0, column=0, padx=5)
		ctk.CTkButton(btn_frame, text=LANG[self.lang]["export_hash"], command=self.export_file_hash).grid(row=0, column=1, padx=5)

		# ---------- Status ----------
		self.hash_status_label = ctk.CTkLabel(frame, text="", font=("Arial", 16))
		self.hash_status_label.grid(row=6, column=0, columnspan=3, pady=10)

		# Layout
		frame.grid_columnconfigure(1, weight=1)
		frame.grid_rowconfigure(3, weight=1)
		frame.grid_rowconfigure(4, weight=1)

	def browse_hash_file(self):
		path = filedialog.askopenfilename()
		if path:
			self.hash_file_path.set(path)

	def calculate_file_hash(self):
		path = self.hash_file_path.get()
		if not path or not os.path.exists(path):
			self.log("ERROR", "File Hash: File not found.")
			self.hash_status_label.configure(text="File not found.", text_color="red")
			return

		algo = self.hash_algo_var.get()
		try:
			h = self.compute_hash(path, algo)
			self.hash_result_box.delete("1.0", "end")
			self.hash_result_box.insert("end", h)
			self.hash_status_label.configure(text=f"{algo} calculated.", text_color="white")
			self.log("INFO", f"{algo} calculated for {path}")
		except Exception as e:
			self.hash_status_label.configure(text="Hash calculation failed.", text_color="red")
			self.log("ERROR", f"File hash calculation failed: {e}")

	def compare_file_hashes(self):
		calculated = self.hash_result_box.get("1.0", "end").strip()
		provided = self.hash_compare_box.get("1.0", "end").strip()

		if not calculated:
			self.hash_status_label.configure(text="No calculated hash.", text_color="orange")
			return

		if not provided:
			self.hash_status_label.configure(text="No comparison hash provided.", text_color="orange")
			return

		if calculated.lower() == provided.lower():
			self.hash_status_label.configure(text="MATCH", text_color="green")
			self.log("INFO", "File hash match confirmed.")
		else:
			self.hash_status_label.configure(text="NO MATCH", text_color="red")
			self.log("WARN", "File hash mismatch.")

	def export_file_hash(self):
		hash_value = self.hash_result_box.get("1.0", "end").strip()
		if not hash_value:
			self.hash_status_label.configure(text="No hash to export.", text_color="orange")
			return

		path = filedialog.asksaveasfilename(
			defaultextension=".txt",
			filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
		)
		if not path:
			return

		try:
			with open(path, "w", encoding="utf-8") as f:
				f.write(hash_value + "\n")
			self.hash_status_label.configure(text="Hash exported.", text_color="green")
			self.log("INFO", f"Exported file hash to {path}")
		except Exception as e:
			self.hash_status_label.configure(text="Export failed.", text_color="red")
			self.log("ERROR", f"Export hash failed: {e}")

	def compute_hash(self, path, algo_name):
		algo_name = algo_name.upper().replace("-", "")
		if algo_name == "MD5":
			h = hashlib.md5()
		elif algo_name == "SHA1":
			h = hashlib.sha1()
		elif algo_name == "SHA256":
			h = hashlib.sha256()
		elif algo_name == "SHA512":
			h = hashlib.sha512()
		else:
			raise ValueError(f"Unsupported hash algorithm: {algo_name}")

		with open(path, "rb") as f:
			for chunk in iter(lambda: f.read(8192), b""):
				h.update(chunk)
		return h.hexdigest()

	def build_hash_tab_folder(self):
		frame = ctk.CTkFrame(self.hash_tab_folder)
		frame.pack(fill="both", expand=True, padx=20, pady=20)

		# ---------- Top controls: folder + buttons ----------
		top_frame = ctk.CTkFrame(frame)
		top_frame.pack(fill="x", pady=5)

		ctk.CTkLabel(top_frame, text=LANG[self.lang]["folder"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
		self.folder_hash_path = ctk.StringVar()
		ctk.CTkEntry(top_frame, textvariable=self.folder_hash_path, width=400).grid(row=0, column=1, padx=5, sticky="w")
		ctk.CTkButton(top_frame, text=LANG[self.lang]["browse"], command=self.browse_folder_hash).grid(row=0, column=2, padx=5)

		# Algorithm selection
		algo_frame = ctk.CTkFrame(top_frame)
		algo_frame.grid(row=1, column=0, columnspan=3, sticky="w", padx=5, pady=5)

		ctk.CTkLabel(algo_frame, text=LANG[self.lang]["algorithms"]).grid(row=0, column=0, sticky="w", padx=5)

		self.folder_hash_use_md5 = ctk.BooleanVar(value=True)
		self.folder_hash_use_sha1 = ctk.BooleanVar(value=False)
		self.folder_hash_use_sha256 = ctk.BooleanVar(value=True)
		self.folder_hash_use_sha512 = ctk.BooleanVar(value=False)

		ctk.CTkCheckBox(algo_frame, text="MD5", variable=self.folder_hash_use_md5).grid(row=0, column=1, padx=5)
		ctk.CTkCheckBox(algo_frame, text="SHA-1", variable=self.folder_hash_use_sha1).grid(row=0, column=2, padx=5)
		ctk.CTkCheckBox(algo_frame, text="SHA-256", variable=self.folder_hash_use_sha256).grid(row=0, column=3, padx=5)
		ctk.CTkCheckBox(algo_frame, text="SHA-512", variable=self.folder_hash_use_sha512).grid(row=0, column=4, padx=5)

		# Buttons
		ctk.CTkButton(top_frame, text=LANG[self.lang]["start_folder_hash"], command=self.start_folder_hash_scan).grid(
			row=2, column=0, columnspan=1, padx=5, pady=10, sticky="w"
		)
		ctk.CTkButton(top_frame, text=LANG[self.lang]["export_txt"], command=self.export_folder_hash_txt).grid(
			row=2, column=1, padx=5, pady=10, sticky="w"
		)
		ctk.CTkButton(top_frame, text=LANG[self.lang]["export_json"], command=self.export_folder_hash_json).grid(
			row=2, column=2, padx=5, pady=10, sticky="w"
		)

		# ---------- Search/filter ----------
		search_frame = ctk.CTkFrame(frame)
		search_frame.pack(fill="x", pady=5)

		ctk.CTkLabel(search_frame, text=LANG[self.lang]["filter"]).pack(side="left", padx=5)
		self.folder_hash_filter = ctk.StringVar()
		ctk.CTkEntry(search_frame, textvariable=self.folder_hash_filter, width=250).pack(side="left", padx=5)
		ctk.CTkButton(search_frame, text=LANG[self.lang]["apply"], command=self.apply_folder_hash_filter).pack(side="left", padx=5)
		ctk.CTkButton(search_frame, text=LANG[self.lang]["clear"], command=self.clear_folder_hash_filter).pack(side="left", padx=5)

		# ---------- Table ----------
		table_frame = ctk.CTkFrame(frame)
		table_frame.pack(fill="both", expand=True, pady=5)

		columns = ["path", "md5", "sha1", "sha256", "sha512", "size"]
		self.folder_hash_tree = ttk.Treeview(table_frame, columns=columns, show="headings")

		self.folder_hash_tree.heading("path", text=LANG[self.lang]["path"])
		self.folder_hash_tree.heading("md5", text=LANG[self.lang]["md5"])
		self.folder_hash_tree.heading("sha1", text=LANG[self.lang]["sha1"])
		self.folder_hash_tree.heading("sha256", text=LANG[self.lang]["sha256"])
		self.folder_hash_tree.heading("sha512", text=LANG[self.lang]["sha512"])
		self.folder_hash_tree.heading("size", text=LANG[self.lang]["size"])

		self.folder_hash_tree.column("path", width=350)
		self.folder_hash_tree.column("md5", width=180)
		self.folder_hash_tree.column("sha1", width=180)
		self.folder_hash_tree.column("sha256", width=220)
		self.folder_hash_tree.column("sha512", width=260)
		self.folder_hash_tree.column("size", width=100, anchor="e")

		y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.folder_hash_tree.yview)
		x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.folder_hash_tree.xview)
		self.folder_hash_tree.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)

		self.folder_hash_tree.grid(row=0, column=0, sticky="nsew")
		y_scroll.grid(row=0, column=1, sticky="ns")
		x_scroll.grid(row=1, column=0, sticky="ew")

		table_frame.grid_rowconfigure(0, weight=1)
		table_frame.grid_columnconfigure(0, weight=1)

		# ---------- Status ----------
		self.folder_hash_status = ctk.CTkLabel(frame, text="", font=("Arial", 14))
		self.folder_hash_status.pack(fill="x", pady=5)

	def browse_folder_hash(self):
		path = filedialog.askdirectory()
		if path:
			self.folder_hash_path.set(path)

	def start_folder_hash_scan(self):
		folder = self.folder_hash_path.get()
		if not folder or not os.path.isdir(folder):
			self.folder_hash_status.configure(text="Folder not found.", text_color="red")
			self.log("ERROR", "Folder Hash: folder not found.")
			return

		# Determine algorithms
		algos = []
		if self.folder_hash_use_md5.get():
			algos.append("MD5")
		if self.folder_hash_use_sha1.get():
			algos.append("SHA-1")
		if self.folder_hash_use_sha256.get():
			algos.append("SHA-256")
		if self.folder_hash_use_sha512.get():
			algos.append("SHA-512")

		if not algos:
			self.folder_hash_status.configure(text="No algorithms selected.", text_color="orange")
			return

		# Clear previous
		self.folder_hash_tree.delete(*self.folder_hash_tree.get_children())
		self.folder_hash_results = []
		self.folder_hash_status.configure(text="Scanning...", text_color="white")
		self.log("INFO", f"Starting folder hash scan: {folder} (algos={algos})")

		threading.Thread(
			target=self.folder_hash_worker,
			args=(folder, algos),
			daemon=True
		).start()

	def folder_hash_worker(self, folder, algos):
		try:
			files = []
			for root, dirs, filenames in os.walk(folder):
				for name in filenames:
					full_path = os.path.join(root, name)
					files.append(full_path)

			total = len(files)
			if total == 0:
				self.folder_hash_status.configure(text="No files found in folder.", text_color="orange")
				self.log("WARN", "Folder Hash: no files in folder.")
				return

			for idx, path in enumerate(files, start=1):
				try:
					size = os.path.getsize(path)
				except OSError:
					size = 0

				result = {
					"path": path,
					"size": size,
					"md5": "",
					"sha1": "",
					"sha256": "",
					"sha512": ""
				}

				for algo in algos:
					try:
						hv = self.compute_hash(path, algo)
					except Exception as e:
						hv = f"ERROR: {e}"
					key = algo.lower().replace("-", "")
					if key == "md5":
						result["md5"] = hv
					elif key == "sha1":
						result["sha1"] = hv
					elif key == "sha256":
						result["sha256"] = hv
					elif key == "sha512":
						result["sha512"] = hv

				self.folder_hash_results.append(result)
				# Update UI row (must be in main thread)
				self.after(0, self.folder_hash_add_row, result)

				if idx % 50 == 0 or idx == total:
					self.folder_hash_status.configure(
						text=f"Hashed {idx}/{total} files...", text_color="white"
					)

			self.folder_hash_status.configure(text=f"Completed. {total} files hashed.", text_color="green")
			self.log("INFO", f"Folder hash completed: {folder} ({total} files)")
		except Exception as e:
			self.folder_hash_status.configure(text="Folder hash failed.", text_color="red")
			self.log("ERROR", f"Folder hash worker error: {e}")

	def folder_hash_add_row(self, result):
		self.folder_hash_tree.insert(
			"",
			"end",
			values=(
				result["path"],
				result["md5"],
				result["sha1"],
				result["sha256"],
				result["sha512"],
				result["size"]
			)
		)

	def apply_folder_hash_filter(self):
		text = self.folder_hash_filter.get().strip().lower()
		self.folder_hash_tree.delete(*self.folder_hash_tree.get_children())

		for r in self.folder_hash_results:
			if not text:
				match = True
			else:
				line = " ".join([
					r["path"],
					r["md5"],
					r["sha1"],
					r["sha256"],
					r["sha512"],
					str(r["size"])
				]).lower()
				match = text in line

			if match:
				self.folder_hash_tree.insert(
					"",
					"end",
					values=(
						r["path"],
						r["md5"],
						r["sha1"],
						r["sha256"],
						r["sha512"],
						r["size"]
					)
				)

	def clear_folder_hash_filter(self):
		self.folder_hash_filter.set("")
		self.apply_folder_hash_filter()

	def export_folder_hash_txt(self):
		if not self.folder_hash_results:
			self.folder_hash_status.configure(text="No data to export.", text_color="orange")
			return

		path = filedialog.asksaveasfilename(
			defaultextension=".txt",
			filetypes=[("Text Files", "*.txt"), ("All Files", "*")]
		)
		if not path:
			return

		try:
			with open(path, "w", encoding="utf-8") as f:
				for r in self.folder_hash_results:
					line = (
						f"{r['path']}\t"
						f"size={r['size']}\t"
						f"md5={r['md5']}\t"
						f"sha1={r['sha1']}\t"
						f"sha256={r['sha256']}\t"
						f"sha512={r['sha512']}"
					)
					f.write(line + "\n")
			self.folder_hash_status.configure(text="Exported TXT.", text_color="green")
			self.log("INFO", f"Folder hash exported TXT: {path}")
		except Exception as e:
			self.folder_hash_status.configure(text="TXT export failed.", text_color="red")
			self.log("ERROR", f"Folder hash TXT export failed: {e}")

	def export_folder_hash_json(self):
		if not self.folder_hash_results:
			self.folder_hash_status.configure(text="No data to export.", text_color="orange")
			return

		path = filedialog.asksaveasfilename(
			defaultextension=".json",
			filetypes=[("JSON Files", "*.json"), ("All Files", "*")]
		)
		if not path:
			return

		try:
			with open(path, "w", encoding="utf-8") as f:
				json.dump(self.folder_hash_results, f, indent=2, ensure_ascii=False)
			self.folder_hash_status.configure(text="Exported JSON.", text_color="green")
			self.log("INFO", f"Folder hash exported JSON: {path}")
		except Exception as e:
			self.folder_hash_status.configure(text="JSON export failed.", text_color="red")
			self.log("ERROR", f"Folder hash JSON export failed: {e}")

	def build_hash_tab_tree(self):
		frame = ctk.CTkFrame(self.hash_tab_tree)
		frame.pack(fill="both", expand=True, padx=20, pady=20)

		# ---------- Top controls ----------
		top_frame = ctk.CTkFrame(frame)
		top_frame.pack(fill="x", pady=5)

		ctk.CTkLabel(top_frame, text=LANG[self.lang]["folder"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
		self.hash_tree_folder = ctk.StringVar()
		ctk.CTkEntry(top_frame, textvariable=self.hash_tree_folder, width=400).grid(
			row=0, column=1, padx=5, sticky="w"
		)
		ctk.CTkButton(top_frame, text=LANG[self.lang]["browse"], command=self.browse_hash_tree_folder).grid(
			row=0, column=2, padx=5
		)

		# Algorithm selection
		algo_frame = ctk.CTkFrame(top_frame)
		algo_frame.grid(row=1, column=0, columnspan=3, sticky="w", padx=5, pady=5)

		ctk.CTkLabel(algo_frame, text=LANG[self.lang]["algorithms"]).grid(row=0, column=0, sticky="w", padx=5)

		self.tree_use_md5 = ctk.BooleanVar(value=True)
		self.tree_use_sha1 = ctk.BooleanVar(value=False)
		self.tree_use_sha256 = ctk.BooleanVar(value=True)
		self.tree_use_sha512 = ctk.BooleanVar(value=False)

		ctk.CTkCheckBox(algo_frame, text="MD5", variable=self.tree_use_md5).grid(row=0, column=1, padx=5)
		ctk.CTkCheckBox(algo_frame, text="SHA-1", variable=self.tree_use_sha1).grid(row=0, column=2, padx=5)
		ctk.CTkCheckBox(algo_frame, text="SHA-256", variable=self.tree_use_sha256).grid(row=0, column=3, padx=5)
		ctk.CTkCheckBox(algo_frame, text="SHA-512", variable=self.tree_use_sha512).grid(row=0, column=4, padx=5)

		# Buttons
		ctk.CTkButton(top_frame, text=LANG[self.lang]["build_hash_tree"], command=self.start_hash_tree_build).grid(
			row=2, column=0, padx=5, pady=10, sticky="w"
		)
		ctk.CTkButton(top_frame, text=LANG[self.lang]["export_json"], command=self.export_hash_tree_json).grid(
			row=2, column=1, padx=5, pady=10, sticky="w"
		)

		# ---------- TreeView instead of textbox ----------
		tree_frame = ctk.CTkFrame(frame)
		tree_frame.pack(fill="both", expand=True, pady=5)

		# Create treeview with columns for file info
		columns = ["name", "size", "hashes"]
		self.hash_tree_view = ttk.Treeview(tree_frame, columns=columns, show="tree headings")

		self.hash_tree_view.heading("#0", text="Path")
		self.hash_tree_view.heading("name", text="Name")
		self.hash_tree_view.heading("size", text="Size")
		self.hash_tree_view.heading("hashes", text="Hash Values")

		self.hash_tree_view.column("#0", width=300)
		self.hash_tree_view.column("name", width=150)
		self.hash_tree_view.column("size", width=100, anchor="e")
		self.hash_tree_view.column("hashes", width=350)

		y_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.hash_tree_view.yview)
		x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.hash_tree_view.xview)
		self.hash_tree_view.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)

		self.hash_tree_view.grid(row=0, column=0, sticky="nsew")
		y_scroll.grid(row=0, column=1, sticky="ns")
		x_scroll.grid(row=1, column=0, sticky="ew")

		tree_frame.grid_rowconfigure(0, weight=1)
		tree_frame.grid_columnconfigure(0, weight=1)

		# Configure tags for folders and files
		self.hash_tree_view.tag_configure("folder", font=("Arial", 10, "bold"))
		self.hash_tree_view.tag_configure("file", font=("Arial", 9))

		# ---------- Status ----------
		self.hash_tree_status = ctk.CTkLabel(frame, text="", font=("Arial", 14))
		self.hash_tree_status.pack(fill="x", pady=5)

	def browse_hash_tree_folder(self):
		path = filedialog.askdirectory()
		if path:
			self.hash_tree_folder.set(path)

	def start_hash_tree_build(self):
		folder = self.hash_tree_folder.get()
		if not folder or not os.path.isdir(folder):
			self.hash_tree_status.configure(text="Folder not found.", text_color="red")
			self.log("ERROR", "Hash Tree: folder not found.")
			return

		algos = []
		if self.tree_use_md5.get():
			algos.append("MD5")
		if self.tree_use_sha1.get():
			algos.append("SHA-1")
		if self.tree_use_sha256.get():
			algos.append("SHA-256")
		if self.tree_use_sha512.get():
			algos.append("SHA-512")

		if not algos:
			self.hash_tree_status.configure(text="No algorithms selected.", text_color="orange")
			return

		# Clear existing tree
		for item in self.hash_tree_view.get_children():
			self.hash_tree_view.delete(item)
		
		self.hash_tree_data = None
		self.hash_tree_status.configure(text="Building hash tree...", text_color="white")
		self.log("INFO", f"Starting hash tree build: {folder} (algos={algos})")

		threading.Thread(
			target=self.hash_tree_worker,
			args=(folder, algos),
			daemon=True
		).start()

	def hash_tree_worker(self, root_folder, algos):
		try:
			tree = self.build_hash_tree_recursive(root_folder, algos)
			self.hash_tree_data = tree

			# Update UI in main thread
			def update_ui():
				# Populate TreeView
				self.populate_hash_tree_view(tree, "")
				self.hash_tree_status.configure(text="Hash tree completed.", text_color="green")

			self.after(0, update_ui)
			self.log("INFO", f"Hash tree completed for {root_folder}")
		except Exception as e:
			def on_err():
				self.hash_tree_status.configure(text="Hash tree failed.", text_color="red")
			self.after(0, on_err)
			self.log("ERROR", f"Hash tree worker error: {e}")

	def populate_hash_tree_view(self, node, parent_id):
		"""Recursively populate the TreeView with hash tree data"""
		folder_name = os.path.basename(node["folder"]) or node["folder"]
		
		# Insert folder node
		folder_id = self.hash_tree_view.insert(
			parent_id, 
			"end", 
			text=folder_name,
			values=("", "", ""),
			tags=("folder",)
		)
		
		# Add files in this folder
		for file_info in node["files"]:
			# Format hash values
			hash_str = ", ".join([f"{algo}: {hash_val[:16]}..." 
								  for algo, hash_val in file_info["hashes"].items()])
			
			# Format size
			size = file_info["size"]
			if size < 1024:
				size_str = f"{size} B"
			elif size < 1024 * 1024:
				size_str = f"{size / 1024:.2f} KB"
			else:
				size_str = f"{size / (1024 * 1024):.2f} MB"
			
			self.hash_tree_view.insert(
				folder_id,
				"end",
				text=file_info["name"],
				values=(file_info["name"], size_str, hash_str),
				tags=("file",)
			)
		
		# Recursively add subfolders
		for subfolder in node["subfolders"]:
			self.populate_hash_tree_view(subfolder, folder_id)

	def build_hash_tree_recursive(self, folder, algos):
		node = {
			"folder": folder,
			"files": [],
			"subfolders": []
		}

		try:
			entries = os.listdir(folder)
		except Exception as e:
			self.log("ERROR", f"Cannot list folder in hash tree: {folder} ({e})")
			return node

		for name in entries:
			full_path = os.path.join(folder, name)
			if os.path.isdir(full_path):
				sub = self.build_hash_tree_recursive(full_path, algos)
				node["subfolders"].append(sub)
			elif os.path.isfile(full_path):
				try:
					size = os.path.getsize(full_path)
				except OSError:
					size = 0

				file_info = {
					"name": name,
					"path": full_path,
					"size": size,
					"hashes": {}
				}

				for algo in algos:
					try:
						hv = self.compute_hash(full_path, algo)
					except Exception as e:
						hv = f"ERROR: {e}"
					file_info["hashes"][algo] = hv

				node["files"].append(file_info)

		return node

	def export_hash_tree_json(self):
		if not self.hash_tree_data:
			self.hash_tree_status.configure(text="No hash tree to export.", text_color="orange")
			return

		path = filedialog.asksaveasfilename(
			defaultextension=".json",
			filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
		)
		if not path:
			return

		try:
			with open(path, "w", encoding="utf-8") as f:
				json.dump(self.hash_tree_data, f, indent=2, ensure_ascii=False)
			self.hash_tree_status.configure(text="Hash tree exported.", text_color="green")
			self.log("INFO", f"Hash tree exported JSON: {path}")
		except Exception as e:
			self.hash_tree_status.configure(text="JSON export failed.", text_color="red")
			self.log("ERROR", f"Hash tree JSON export failed: {e}")

	def browse_dup_folder(self):
		path = filedialog.askdirectory()
		if path:
			self.dup_folder.set(path)

	def browse_compare_src(self):
		path = filedialog.askdirectory()
		if path:
			self.compare_src_folder.set(path)

	def browse_compare_dst(self):
		path = filedialog.askdirectory()
		if path:
			self.compare_dst_folder.set(path)

	def start_hash_compare(self):
		src = self.compare_src_folder.get()
		dst = self.compare_dst_folder.get()

		if not src or not os.path.isdir(src):
			self.compare_status.configure(text="Source folder not found.", text_color="red")
			self.log("ERROR", "Hash Compare: source folder not found.")
			return

		if not dst or not os.path.isdir(dst):
			self.compare_status.configure(text="Destination folder not found.", text_color="red")
			self.log("ERROR", "Hash Compare: destination folder not found.")
			return

		algo = self.compare_algo_var.get()

		# Clear previous
		self.compare_tree.delete(*self.compare_tree.get_children())
		self.compare_results = []
		self.compare_status.configure(text="Comparing...", text_color="white")
		self.log("INFO", f"Starting hash compare: {src} vs {dst} (algo={algo})")

		threading.Thread(
			target=self.compare_worker,
			args=(src, dst, algo),
			daemon=True
		).start()

	def compare_worker(self, src_folder, dst_folder, algo):
		try:
			# Build list of files in source
			src_files = {}
			for root, dirs, filenames in os.walk(src_folder):
				for name in filenames:
					full_path = os.path.join(root, name)
					rel_path = os.path.relpath(full_path, src_folder)
					src_files[rel_path] = full_path

			total = len(src_files)
			if total == 0:
				self.compare_status.configure(text="No files in source folder.", text_color="orange")
				self.log("WARN", "Hash Compare: no files in source folder.")
				return

			idx = 0
			for rel_path, src_path in src_files.items():
				idx += 1
				dst_path = os.path.join(dst_folder, rel_path)

				# Compute source hash
				try:
					src_hash = self.compute_hash(src_path, algo)
				except Exception as e:
					src_hash = f"ERROR: {e}"

				# Check if file exists in destination
				if not os.path.exists(dst_path):
					result = {
						"status": "MISSING",
						"relpath": rel_path,
						"src_path": src_path,
						"dst_path": dst_path,
						"algo": algo,
						"src_hash": src_hash,
						"dst_hash": "N/A"
					}
				else:
					# Compute destination hash
					try:
						dst_hash = self.compute_hash(dst_path, algo)
					except Exception as e:
						dst_hash = f"ERROR: {e}"

					# Compare hashes
					if src_hash == dst_hash:
						status = "MATCH"
					else:
						status = "MISMATCH"

					result = {
						"status": status,
						"relpath": rel_path,
						"src_path": src_path,
						"dst_path": dst_path,
						"algo": algo,
						"src_hash": src_hash,
						"dst_hash": dst_hash
					}

				self.compare_results.append(result)
				# Update UI row (must be in main thread)
				self.after(0, self.compare_add_row, result)

				if idx % 10 == 0 or idx == total:
					self.compare_status.configure(
						text=f"Compared {idx}/{total} files...", text_color="white"
					)

			# Summary
			match_count = sum(1 for r in self.compare_results if r["status"] == "MATCH")
			mismatch_count = sum(1 for r in self.compare_results if r["status"] == "MISMATCH")
			missing_count = sum(1 for r in self.compare_results if r["status"] == "MISSING")

			summary = f"Completed. Match: {match_count}, Mismatch: {mismatch_count}, Missing: {missing_count}"
			self.compare_status.configure(text=summary, text_color="green")
			self.log("INFO", f"Hash compare completed: {summary}")
		except Exception as e:
			self.compare_status.configure(text="Hash compare failed.", text_color="red")
			self.log("ERROR", f"Hash compare worker error: {e}")

	def compare_add_row(self, result):
		status = result["status"]
		tag = status.lower()
		src_hash_display = result["src_hash"][:32] + "..." if len(result["src_hash"]) > 32 else result["src_hash"]
		dst_hash_display = result["dst_hash"][:32] + "..." if result["dst_hash"] != "N/A" and len(result["dst_hash"]) > 32 else result["dst_hash"]
		self.compare_tree.insert(
			"",
			"end",
			values=(status, result["relpath"], src_hash_display, dst_hash_display),
			tags=(tag,)
		)

	def apply_compare_filter(self):
		text = self.compare_filter.get().strip().lower()
		self.compare_tree.delete(*self.compare_tree.get_children())

		for r in self.compare_results:
			if not text:
				match = True
			else:
				line = " ".join([
					r["status"],
					r["relpath"],
					r["src_hash"],
					r["dst_hash"]
				]).lower()
				match = text in line

			if match:
				status = r["status"]
				tag = status.lower()
				src_hash_display = r["src_hash"][:32] + "..." if len(r["src_hash"]) > 32 else r["src_hash"]
				dst_hash_display = r["dst_hash"][:32] + "..." if r["dst_hash"] != "N/A" and len(r["dst_hash"]) > 32 else r["dst_hash"]
				self.compare_tree.insert(
					"",
					"end",
					values=(status, r["relpath"], src_hash_display, dst_hash_display),
					tags=(tag,)
				)

	def clear_compare_filter(self):
		self.compare_filter.set("")
		self.apply_compare_filter()

	def export_compare_results(self):
		if not self.compare_results:
			self.compare_status.configure(text="No results to export.", text_color="orange")
			return

		path = filedialog.asksaveasfilename(
			defaultextension=".json",
			filetypes=[("JSON Files", "*.json"), ("Text Files", "*.txt"), ("All Files", "*")]
		)
		if not path:
			return

		try:
			if path.endswith(".json"):
				with open(path, "w", encoding="utf-8") as f:
					json.dump(self.compare_results, f, indent=2, ensure_ascii=False)
			else:
				with open(path, "w", encoding="utf-8") as f:
					for r in self.compare_results:
						f.write(f"Status: {r['status']}\n")
						f.write(f"Path: {r['relpath']}\n")
						f.write(f"Source Hash: {r['src_hash']}\n")
						f.write(f"Dest Hash: {r['dst_hash']}\n")
						f.write("\n")

			self.compare_status.configure(text="Results exported.", text_color="green")
			self.log("INFO", f"Hash compare results exported: {path}")
		except Exception as e:
			self.compare_status.configure(text="Export failed.", text_color="red")
			self.log("ERROR", f"Compare results export failed: {e}")

	def select_duplicates_but_one(self):
		"""
		Select all duplicate files except one (the first) in each hash group.
		This allows users to easily delete duplicates while keeping one copy.
		"""
		if not hasattr(self, 'dup_groups') or not self.dup_groups:
			self.dup_status.configure(text="No duplicates scanned yet.", text_color="orange")
			return

		# Clear current selection
		self.dup_tree.selection_remove(self.dup_tree.selection())

		# Build a mapping of hash -> list of tree item IDs
		hash_to_items = {}
		for item_id in self.dup_tree.get_children():
			values = self.dup_tree.item(item_id, "values")
			if len(values) >= 1:
				file_hash = values[0]
				if file_hash not in hash_to_items:
					hash_to_items[file_hash] = []
				hash_to_items[file_hash].append(item_id)

		# For each hash group with 2+ items, select all but the first
		selected_count = 0
		for file_hash, items in hash_to_items.items():
			if len(items) >= 2:
				# Select all items except the first one (keep the first)
				for item_id in items[1:]:
					self.dup_tree.selection_add(item_id)
					selected_count += 1

		if selected_count > 0:
			self.dup_status.configure(text=f"Selected {selected_count} duplicate files (keeping 1 per group).", text_color="green")
			self.log("INFO", f"Selected {selected_count} duplicates for action (keeping first file in each group)")
		else:
			self.dup_status.configure(text="No duplicates to select.", text_color="orange")

	def start_find_duplicates(self):
		folder = self.dup_folder.get()
		if not folder or not os.path.isdir(folder):
			self.dup_status.configure(text="Folder not found.", text_color="red")
			self.log("ERROR", "Duplicates: folder not found.")
			return

		algo = self.dup_algo_var.get()

		self.dup_tree.delete(*self.dup_tree.get_children())
		self.dup_results = []
		self.dup_groups = {}
		self.dup_progress.set(0)
		self.dup_current_file.configure(text="")
		self.dup_status.configure(text=f"Scanning with {algo}...", text_color="white")
		self.log("INFO", f"Starting duplicate search: folder={folder}, algo={algo}")

		threading.Thread(
			target=self.dup_worker,
			args=(folder, algo),
			daemon=True
		).start()

	def dup_worker(self, folder, algo):
		try:
			files = []
			for base, dirs, names in os.walk(folder):
				for name in names:
					full_path = os.path.join(base, name)
					if os.path.isfile(full_path):
						files.append(full_path)

			total = len(files)
			if total == 0:
				self.dup_status.configure(text="No files found.", text_color="orange")
				self.log("WARN", "Duplicates: no files in folder.")
				return

			for idx, path in enumerate(files, start=1):
				# Update progress and current file display
				progress = idx / total
				self.dup_progress.set(progress)
				
				# Display current file being processed
				display_path = path if len(path) <= 80 else "..." + path[-77:]
				self.dup_current_file.configure(text=f"Processing ({idx}/{total}): {display_path}")
				
				try:
					size = os.path.getsize(path)
				except OSError:
					size = 0

				try:
					hv = self.compute_hash(path, algo)
				except Exception as e:
					hv = f"ERROR: {e}"

				entry = {"hash": hv, "size": size, "path": path}
				self.dup_results.append(entry)

				if hv not in self.dup_groups:
					self.dup_groups[hv] = []
				self.dup_groups[hv].append({"size": size, "path": path})

				if idx % 10 == 0 or idx == total:
					self.dup_status.configure(
						text=f"Hashed {idx}/{total} files...", text_color="white"
					)

			# After hashing everything, populate only true duplicates
			def update_ui():
				self.populate_duplicates_table()
				self.dup_progress.set(1.0)
				self.dup_current_file.configure(text="Scan completed!")
				self.dup_status.configure(text="Duplicate scan completed.", text_color="green")

			self.after(0, update_ui)
			self.log("INFO", f"Duplicates scan completed: {total} files")
		except Exception as e:
			self.dup_status.configure(text="Duplicate scan failed.", text_color="red")
			self.dup_current_file.configure(text="")
			self.log("ERROR", f"Duplicates worker error: {e}")

	def populate_duplicates_table(self):
		self.dup_tree.delete(*self.dup_tree.get_children())
		dup_count = 0
		for hv, items in self.dup_groups.items():
			if len(items) < 2:
				continue  # not duplicates

			dup_count += 1
			for it in items:
				self.dup_tree.insert(
					"",
					"end",
					values=(hv, it["size"], it["path"]),
					tags=("dup_group",)
				)

		if dup_count == 0:
			self.dup_status.configure(text="No duplicates found.", text_color="orange")
		else:
			self.dup_status.configure(text=f"Found {dup_count} duplicate hash groups.", text_color="green")

	def export_duplicates_txt(self):
		# Export only groups with more than one file
		groups = {h: items for h, items in self.dup_groups.items() if len(items) > 1}
		if not groups:
			self.dup_status.configure(text="No duplicates to export.", text_color="orange")
			return

		path = filedialog.asksaveasfilename(
			defaultextension=".txt",
			filetypes=[("Text Files", "*.txt"), ("All Files", "*")]
		)
		if not path:
			return

		try:
			with open(path, "w", encoding="utf-8") as f:
				for hv, items in groups.items():
					f.write(f"HASH: {hv}\n")
					for it in items:
						f.write(f"  {it['size']} bytes  {it['path']}\n")
					f.write("\n")
			self.dup_status.configure(text="Duplicates TXT exported.", text_color="green")
			self.log("INFO", f"Duplicates TXT exported: {path}")
		except Exception as e:
			self.dup_status.configure(text="TXT export failed.", text_color="red")
			self.log("ERROR", f"Duplicates TXT export failed: {e}")

	def export_duplicates_json(self):
		groups = {h: items for h, items in self.dup_groups.items() if len(items) > 1}
		if not groups:
			self.dup_status.configure(text="No duplicates to export.", text_color="orange")
			return

		path = filedialog.asksaveasfilename(
			defaultextension=".json",
			filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
		)
		if not path:
			return

		try:
			with open(path, "w", encoding="utf-8") as f:
				json.dump(groups, f, indent=2, ensure_ascii=False)
			self.dup_status.configure(text="Duplicates JSON exported.", text_color="green")
			self.log("INFO", f"Duplicates JSON exported: {path}")
		except Exception as e:
			self.dup_status.configure(text="JSON export failed.", text_color="red")
			self.log("ERROR", f"Duplicates JSON export failed: {e}")

	def delete_selected_duplicates(self):
		items = self.dup_tree.selection()
		if not items:
			self.dup_status.configure(text="No files selected.", text_color="orange")
			return

		paths = []
		for iid in items:
			vals = self.dup_tree.item(iid, "values")
			if len(vals) >= 3:
				path = vals[2]
				if path:
					paths.append((iid, path))

		if not paths:
			self.dup_status.configure(text="No valid file paths selected.", text_color="orange")
			return

		deleted = 0
		for iid, p in paths:
			try:
				if os.path.isfile(p):
					os.remove(p)
					deleted += 1
					self.dup_tree.delete(iid)
			except Exception as e:
				self.log("ERROR", f"Failed to delete duplicate file: {p} ({e})")

		self.dup_status.configure(text=f"Deleted {deleted} files.", text_color="green")
		self.log("INFO", f"Deleted {deleted} duplicate files.")

	def move_selected_duplicates(self):
		items = self.dup_tree.selection()
		if not items:
			self.dup_status.configure(text="No files selected.", text_color="orange")
			return

		dest = filedialog.askdirectory(title="Select destination for duplicates")
		if not dest:
			return

		moved = 0
		for iid in items:
			vals = self.dup_tree.item(iid, "values")
			if len(vals) < 3:
				continue
			path = vals[2]
			if not path or not os.path.isfile(path):
				continue

			try:
				fname = os.path.basename(path)
				target = os.path.join(dest, fname)

				# Ensure unique name if exists
				base, ext = os.path.splitext(fname)
				counter = 1
				while os.path.exists(target):
					target = os.path.join(dest, f"{base}_{counter}{ext}")
					counter += 1

				shutil.move(path, target)
				moved += 1
				self.dup_tree.set(iid, "path", target)  # update displayed path
			except Exception as e:
				self.log("ERROR", f"Failed to move duplicate file: {path} ({e})")

		self.dup_status.configure(text=f"Moved {moved} files.", text_color="green")
		self.log("INFO", f"Moved {moved} duplicate files.")

	def apply_settings(self):
		# Validate numeric inputs
		try:
			threshold = int(self.settings_threshold.get())
			retention = int(self.settings_log_retention.get())
		except ValueError:
			self.log("ERROR", "Invalid numeric values in settings. Please enter valid integers.")
			return

		# Update config dictionary
		self.cfg["language"] = self.lang_var.get()
		self.cfg["theme_mode"] = self.theme_var.get()
		self.cfg["smart_move_threshold"] = threshold
		self.cfg["log_retention_days"] = retention

		# Save to file
		save_config(self.cfg)

		# Apply theme
		if self.cfg["theme_mode"] == "auto":
			ctk.set_appearance_mode(get_auto_theme())
		else:
			ctk.set_appearance_mode(self.cfg["theme_mode"])

		# Language change requires restart
		if self.lang != self.cfg["language"]:
			self.log("INFO", "Settings saved. Please restart the application for language changes to take effect.")
		else:
			# Cleanup logs according to new retention
			cleanup_old_logs(self.cfg["log_retention_days"])
			self.log("INFO", "Settings saved and applied.")

	def refresh_logs(self):
		ensure_log_dir()
		self.logs_listbox.delete(0, tk.END)

		for file in sorted(os.listdir(LOG_DIR)):
			if file.endswith(".log"):
				self.logs_listbox.insert(tk.END, file)

	def load_selected_log(self, event=None):
		selection = self.logs_listbox.curselection()
		if not selection:
			return

		filename = self.logs_listbox.get(selection[0])
		path = os.path.join(LOG_DIR, filename)

		try:
			with open(path, "r", encoding="utf-8") as f:
				content = f.read()
		except Exception:
			content = "Error reading log file."

		self.logs_textbox.delete("1.0", "end")
		self.logs_textbox.insert("end", content)

	def delete_selected_log(self):
		selection = self.logs_listbox.curselection()
		if not selection:
			self.log("WARN", "No log file selected for deletion.")
			return

		filename = self.logs_listbox.get(selection[0])
		path = os.path.join(LOG_DIR, filename)

		try:
			os.remove(path)
			self.log("INFO", f"Deleted log file: {filename}")
		except Exception as e:
			self.log("ERROR", f"Failed to delete log: {e}")

		self.refresh_logs()
		self.logs_textbox.delete("1.0", "end")

	# ---------------------------------------------------------
	# Run App
	# ---------------------------------------------------------
if __name__ == "__main__":
	app = App()
	app.mainloop()
