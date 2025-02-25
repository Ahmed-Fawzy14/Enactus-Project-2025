import os
import requests
import tkinter as tk
from tkinter import filedialog, Label, Entry, Button, Radiobutton, IntVar, messagebox
from PIL import Image, ImageTk
from openai import OpenAI
import threading

client = OpenAI(api_key=" ")

# Directory to save images
IMAGE_DIR = "source"
os.makedirs(IMAGE_DIR, exist_ok=True)

class ImageGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Image Generator")
        self.root.geometry("700x800")

        # User Input
        self.label = Label(root, text="Enter your prompt:")
        self.label.pack()

        self.entry = Entry(root, width=50)
        self.entry.pack()

        # Buttons
        self.generate_button = Button(root, text="Generate", command=self.start_generate)
        self.generate_button.pack()

        self.variations_button = Button(root, text="Variations", command=self.generate_variation, state=tk.DISABLED)
        self.variations_button.pack()

        # Image Display
        self.image_label1 = Label(root)
        self.image_label1.pack()
        self.image_label2 = Label(root)
        self.image_label2.pack()

        # Radio buttons to select image for variations
        self.selected_image = IntVar()
        self.radio1 = Radiobutton(root, text="Select Image 1", variable=self.selected_image, value=1, state=tk.DISABLED)
        self.radio2 = Radiobutton(root, text="Select Image 2", variable=self.selected_image, value=2, state=tk.DISABLED)
        self.radio1.pack()
        self.radio2.pack()

        # Loading indicator
        self.loading_label = Label(root, text="", fg="blue")
        self.loading_label.pack()

        self.last_generated_images = []  # Store last generated image paths

    def start_generate(self):
        threading.Thread(target=self.generate_images, daemon=True).start()

    def generate_images(self):
        prompt = self.entry.get()
        if not prompt:
            messagebox.showerror("Error", "Please enter a prompt.")
            return
        
        self.loading_label.config(text="Generating images...")
        self.root.update()

        try:
            urls = [generate_New_Image(prompt) for _ in range(2)]
            file_paths = [os.path.join(IMAGE_DIR, f"generated_image_{i+1}.jpg") for i in range(2)]

            for i, url in enumerate(urls):
                download_image(url, file_paths[i])

            self.last_generated_images = file_paths
            self.display_images(file_paths)
            self.variations_button.config(state=tk.NORMAL)
            self.radio1.config(state=tk.NORMAL)
            self.radio2.config(state=tk.NORMAL)
            self.loading_label.config(text="Success: Images generated!")
        except Exception as e:
            messagebox.showerror("Error", f"Image generation failed: {e}")
            self.loading_label.config(text="Failed to generate images.")

    def generate_variation(self):
        if not self.last_generated_images:
            messagebox.showerror("Error", "No images generated yet.")
            return
        
        selected = self.selected_image.get()
        if selected not in [1, 2]:
            messagebox.showerror("Error", "Please select an image for variation.")
            return
        
        self.loading_label.config(text="Generating variation...")
        self.root.update()

        try:
            variation_url = variations(self.last_generated_images[selected - 1])[0]
            download_image(variation_url, self.last_generated_images[selected - 1])
            self.display_image(self.last_generated_images[selected - 1], selected)
            self.loading_label.config(text="Success: Variation generated!")
        except Exception as e:
            messagebox.showerror("Error", f"Variation generation failed: {e}")
            self.loading_label.config(text="Failed to generate variation.")

    def display_images(self, image_paths):
        self.display_image(image_paths[0], 1)
        self.display_image(image_paths[1], 2)

    def display_image(self, image_path, image_number):
        img = Image.open(image_path).resize((400, 400))
        img = ImageTk.PhotoImage(img)
        if image_number == 1:
            self.image_label1.config(image=img)
            self.image_label1.image = img
        else:
            self.image_label2.config(image=img)
            self.image_label2.image = img

def generate_New_Image(user_prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=user_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url


def variations(image_png):
    response = client.images.create_variation(
        model="dall-e-2",
        image=open(image_png, "rb"),
        n=1,
        size="1024x1024"
    )
    return [response.data[0].url]


def download_image(image_url, filename):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageGeneratorApp(root)
    root.mainloop()