# Additional methods to add to the App class for Hash Tree functionality

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
