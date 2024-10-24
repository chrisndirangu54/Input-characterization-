import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import json
import os

class MobileInputFieldExtractor:
    """
    A class for extracting input field information from mobile app UI images using Python and ADB.
    """
    def __init__(self):
        pass
    
    def extract_input_fields(self, app_image):
        """
        Extract input field information from the provided app image.
        
        Args:
        - app_image: Image of the mobile app UI
        
        Returns:
        - input_fields: Structured JSON containing input field attributes
        """
        # Check if ADB is installed
        if not self.check_adb_installed():
            raise EnvironmentError("ADB is not installed or configured properly.")
        
        # Check if app image exists
        if not os.path.exists(app_image):
            raise FileNotFoundError(f"App image '{app_image}' not found.")
        
        # Use ADB to capture app UI image
        self.capture_app_ui_image()
        
        # Perform image processing and field detection
        input_fields = self.detect_input_fields("app_ui.png")
        
        return input_fields
    
    def capture_app_ui_image(self):
        """
        Capture the mobile app UI image using ADB.
        """
        try:
            subprocess.run(["adb", "shell", "screencap", "/sdcard/app_ui.png"], check=True)
            subprocess.run(["adb", "pull", "/sdcard/app_ui.png", "app_ui.png"], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to capture app UI image: {e}")
    
    def detect_input_fields(self, image_path):
        """
        Detect input fields from the app UI image.
        
        Args:
        - image_path: Path to the app UI image
        
        Returns:
        - input_fields: Structured JSON containing input field attributes
        """
        # Placeholder for field detection logic
        input_fields = {
            "fields": [
                {"label": "Username", "type": "text", "validation": "required"},
                {"label": "Password", "type": "password", "validation": "required"},
                {"label": "DOB", "type": "date", "validation": "optional"}
            ]
        }
        
        return input_fields
    
    def save_output(self, input_fields, output_file):
        """
        Save the extracted input field information to a JSON file.
        
        Args:
        - input_fields: Structured JSON containing input field attributes
        - output_file: File path to save the output JSON
        """
        with open(output_file, "w") as f:
            json.dump(input_fields, f, indent=4)
        
    def check_adb_installed(self):
        """
        Check if ADB is installed and configured properly.
        
        Returns:
        - True if ADB is installed and configured, False otherwise
        """
        try:
            subprocess.run(["adb", "version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

class MobileInputFieldExtractorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mobile Input Field Extractor")
        self.root.geometry("400x200")
        
        self.extractor = MobileInputFieldExtractor()
        
        self.create_widgets()
    
    def create_widgets(self):
        self.label = tk.Label(self.root, text="Select App UI Image:")
        self.label.pack(pady=10)
        
        self.select_button = tk.Button(self.root, text="Select Image", command=self.select_image)
        self.select_button.pack()
        
        self.extract_button = tk.Button(self.root, text="Extract Input Fields", command=self.extract_fields)
        self.extract_button.pack(pady=10)
    
    def select_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Image Selected", f"Selected image: {self.image_path}")
        else:
            messagebox.showwarning("Warning", "No image selected.")
    
    def extract_fields(self):
        try:
            input_fields = self.extractor.extract_input_fields(self.image_path)
            output_file = "input_fields.json"
            self.extractor.save_output(input_fields, output_file)
            messagebox.showinfo("Extraction Successful", f"Input fields extracted successfully. Output saved to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MobileInputFieldExtractorUI(root)
    root.mainloop()
