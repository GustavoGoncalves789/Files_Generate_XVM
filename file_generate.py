import tkinter as tk
from tkinter import filedialog
import re
import os

def sanitize_filename(name):
    # Replace special characters with underscores
    return re.sub(r'[^\w]', '_', name)

def generate_section_files(file_path):
    log_area.delete(1.0, tk.END)  # Clear previous logs
    log_area.insert(tk.END, "Generating section files...\n")
    
    output_directory = os.path.join(os.path.dirname(file_path), "model")  # Get the directory of the input file
    
    # Create the 'model' directory if it does not exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        section_title = None
        section_content = []

        for line in lines:
            if line.strip():  # Non-empty line
                if line.startswith('\t'):  # Content line
                    section_content.append(line)
                else:  # Section title line
                    if section_title:
                        # Write content to file
                        with open(os.path.join(output_directory, f"{sanitize_filename(section_title.strip())}.xmv"), 'w') as section_file:
                            section_file.write(f"{section_title.strip()}\n")
                            section_file.writelines(section_content)
                        log_area.insert(tk.END, f"Generated {sanitize_filename(section_title.strip())}.xmv\n")
                    section_title = line.strip()
                    section_content = []

        # Write content for the last section
        if section_title and section_content:
            with open(os.path.join(output_directory, f"{sanitize_filename(section_title.strip())}.xmv"), 'w') as section_file:
                section_file.write(f"{section_title.strip()}\n")
                section_file.writelines(section_content)
            log_area.insert(tk.END, f"Generated {sanitize_filename(section_title.strip())}.xmv\n")
        
        # Log the path where files were generated
        log_area.insert(tk.END, f"Files were generated in path: {output_directory}\n")
        
        log_area.insert(tk.END, "Section files generation completed.\n")
        
        # Open the directory where the files are located
        os.startfile(output_directory)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("XMV files", "*.xmv")])
    if file_path:
        generate_section_files(file_path)

# Create tkinter window
root = tk.Tk()
root.title("Section File Generator")

# Styling
root.geometry("400x300")
root.configure(background="#f0f0f0")

# Browse button
browse_button = tk.Button(root, text="Browse", command=browse_file, bg="#4CAF50", fg="white", font=("Arial", 12))
browse_button.grid(row=0, column=0, padx=10, pady=10)

# Logging area
log_area = tk.Text(root, height=10, width=54, bg="#e0e0e0", bd=0, font=("Arial", 10))
log_area.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()
