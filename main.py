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
