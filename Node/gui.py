import customtkinter as ctk

class Window(ctk.CTk):
    def __init__(self, title: str, size: tuple[int, int], theme: str, accent: str, icon_bitmap, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme(accent)
        
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.iconbitmap(icon_bitmap)

    def run(self) -> None:
        self.mainloop()