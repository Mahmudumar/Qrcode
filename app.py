import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import ImageTk, Image
import os

class QRGenerator:
    """A class to generate QR codes based on user input using Tkinter GUI."""

    def __init__(self, master:tk.Tk):
        """
        Initialize the QRGenerator.

        Args:
            master: The Tkinter root/master window.
        """
        self.master = master
        self.master.title("QR Code Generator")
        self.master.iconbitmap('logo.ico')
        

        self.layout()

    def layout(self):
        """
        Set up the layout of the GUI.
        """
        self.qrcode_frame = tk.Canvas(
            self.master, bg='#aaa', height=200, width=200)
        self.qrcode_frame.pack(pady=10)

        self.help_label = tk.Label(
            self.master, text='Enter the information to generate QR code for...')
        self.help_label.pack()

        self.input_text = tk.Text(self.master, height=3)
        self.input_text.pack()

        self.generate_btn = tk.Button(self.master, text='GENERATE QR code',
                                      height=3, bg='#aaf', command=self.generate)
        self.generate_btn.pack()
        self.save_btn = tk.Button(self.master, text='SAVE QR code',
                                      height=3, bg='#aaa', command=self.save,state='disabled')
        self.save_btn.pack()

    def generate(self):
        """
        Generate the QR code based on the input text and display it on the GUI canvas.
        """
        data = self.input_text.get(1.0, tk.END).strip()
        if not data:
            messagebox.showerror("Error", "Please enter some data.")
            return

        try:
            self.qr_code = qrcode.make(data)
            temp_file = "tmp_qrcode.png"
            self.qr_code.save(temp_file)
            
            original_image = Image.open(temp_file)
            resized_image = original_image.resize(
                (self.qrcode_frame.winfo_width(), self.qrcode_frame.winfo_height()))
            self.qrcode_image = ImageTk.PhotoImage(resized_image)

            self.qrcode_frame.create_image(
                0, 0, anchor=tk.NW, image=self.qrcode_image)
            self.save_btn['state']='normal'
            self.save_btn['bg']='#aaf'
            self.generate_btn['bg']='#aaa'

            # Clean up the temporary file
            os.remove(temp_file)

        except Exception as e:
            messagebox.showerror("Error", str(e))
    def save(self):
        file = filedialog.asksaveasfilename(filetypes=[("Image files", (".png", ".jpg")), ("All files", "")])
        if file:
            self.qr_code.save(file)
            messagebox.showinfo('File Saved', 'Your QR code has been saved successfully')
            self.input_text.delete(1.0, tk.END)
            # Delete the displayed QR code from the canvas
            self.qrcode_frame.delete("all")
        self.generate_btn['bg']='#aaf'
        self.save_btn['bg']='#aaa'
        self.save_btn['state']='disabled'





def main():
    """Main function to create and run the QR Generator application."""
    root = tk.Tk()
    app = QRGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
