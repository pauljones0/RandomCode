from tkinter import Tk, Label, Button, messagebox
from typing import Optional
from .light_control import LightSystem, LightController
from .config import LightConfig

class LightGUI:
    """GUI interface for light control system"""
    def __init__(self, light_system: LightSystem):
        self.controller = LightController(light_system)
        self.root: Optional[Tk] = None
        self.setup_gui()

    def setup_gui(self) -> None:
        """Initialize the GUI window and controls"""
        try:
            self.root = Tk()
            self.root.title("Light Control")
            self.root.geometry("300x200")
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

            # Create control buttons
            Button(self.root, text="Start", command=self.safe_start).pack(pady=10)
            Button(self.root, text="Stop", command=self.safe_stop).pack(pady=10)
            Button(self.root, text="Dim", command=self.safe_dim).pack(pady=10)
            Button(self.root, text="Max Brightness", 
                   command=self.safe_max_brightness).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Setup Error", f"Failed to setup GUI: {e}")
            raise

    def safe_start(self) -> None:
        """Safely execute start command with error handling"""
        try:
            self.controller.start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start: {e}")

    def safe_stop(self) -> None:
        """Safely execute stop command with error handling"""
        try:
            self.controller.stop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop: {e}")

    def safe_dim(self) -> None:
        """Safely execute dim command with error handling"""
        try:
            self.controller.dim_lights()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to dim lights: {e}")

    def safe_max_brightness(self) -> None:
        """Safely execute max brightness command with error handling"""
        try:
            self.controller.set_max_brightness()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set max brightness: {e}")

    def on_closing(self) -> None:
        """Handle window closing event"""
        self.cleanup()
        self.root.quit()

    def run(self) -> None:
        """Start the GUI event loop"""
        if self.root:
            self.root.mainloop()

    def cleanup(self) -> None:
        """Cleanup resources before closing"""
        try:
            if self.controller._running:
                self.controller.stop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop controller: {e}")
        finally:
            if self.root:
                self.root.destroy()