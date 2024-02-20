import tkinter as tk
from tkinter import scrolledtext, messagebox, Checkbutton, IntVar, Entry, Label, Frame, Button, filedialog, simpledialog
from bs4 import BeautifulSoup
import requests
import csv
import json
import re

def scrape():
    url = url_entry.get()
    content = ""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape according to selected options
        if headline_var.get():
            content += "Headlines:\n" + '\n'.join([headline.text for headline in soup.find_all(['h1', 'h2', 'h3'])]) + "\n\n"
        
        if paragraph_var.get():
            content += "Paragraphs:\n" + '\n\n'.join([p.text for p in soup.find_all('p')]) + "\n\n"
        
        if link_var.get():
            content += "Links:\n" + '\n'.join([a['href'] for a in soup.find_all('a', href=True)]) + "\n\n"
        
        if image_var.get():
            content += "Images:\n" + '\n'.join([img['src'] for img in soup.find_all('img', src=True)]) + "\n\n"
        
        # Custom Tag/Element Extraction
        custom_tag = custom_tag_entry.get()
        if custom_tag:
            elements = soup.find_all(custom_tag)
            custom_content = '\n\n'.join([str(element) for element in elements])
            content += f"Custom {custom_tag} Elements:\n" + custom_content + "\n\n"
        
        result_area.delete(1.0, tk.END)
        result_area.insert(tk.INSERT, content)

    except Exception as e:
        messagebox.showerror("Error", "Failed to scrape the URL. Error: " + str(e))

def save_data():
    file_type = file_type_var.get()
    data = result_area.get(1.0, tk.END)
    if not data.strip():
        messagebox.showwarning("Warning", "No data to save!")
        return
    
    file_name = filedialog.asksaveasfilename(defaultextension=f".{file_type}",
                                             filetypes=[(f"{file_type.upper()} files", f"*.{file_type}")])
    
    if not file_name:
        return  # User cancelled save
    
    try:
        if file_type == 'csv':
            with open(file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Content'])
                writer.writerow([data])

        elif file_type == 'json':
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump({"content": data}, file, ensure_ascii=False, indent=4)
        elif file_type == 'txt':
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(data)
        messagebox.showinfo("Success", f"Data successfully saved as {file_name}!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file. Error: {e}")
