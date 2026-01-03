	def populate_duplicates_table(self):
		self.dup_tree.delete(*self.dup_tree.get_children())

		dup_count = 0
		for hv, items in self.dup_groups.items():
			if len(items) < 2:
				continue  # not duplicates

			dup_count += 1
			# Optionally, you can insert a header row per group (commented out)
			# group_id = self.dup_tree.insert("", "end", values=(hv, "", "[DUPLICATE GROUP]"), tags=("dup_group",))

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
