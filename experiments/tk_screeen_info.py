import tkinter as tk
from tkinter import font
from tkinter import scrolledtext

# Create an instance of Tkinter
root = tk.Tk()

# Withdraw the root window as we don't need to display it
root.withdraw()

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Create a ScrolledText widget
scrolled_text = scrolledtext.ScrolledText(root, width=40, height=10)

# Get the default font
default_font = font.nametofont("TkDefaultFont")
# Create a test string (you can adjust the length based on what you need)
test_string = "Tournament"

# Measure the width and height of the test string using the default font
text_width = default_font.measure(test_string)
text_height = default_font.metrics("linespace")

# Close the Tkinter root instance
root.quit()

# Print the results
print(f"Screen width: {screen_width} pixels")
print(f"Screen height: {screen_height} pixels")

print(f"Default font family: {default_font.actual()['family']}")
print(f"Default font size: {default_font.actual()['size']}")
print(f"Default font weight: {default_font.actual()['weight']}")

print(f"Default text width for '{test_string}': {text_width} pixels")
print(f"Default text height: {text_height} pixels")