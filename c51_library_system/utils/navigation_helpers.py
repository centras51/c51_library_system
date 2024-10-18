

class Navigator:
    def go_back_to_login(self, root):
        from main import LibraryApp
        for widget in root.winfo_children():
            widget.destroy()
        LibraryApp(root)