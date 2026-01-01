#!/usr/bin/env python3
"""
Domain Finder Tool
A GUI application to search for specific domains in text files within a selected folder.
"""

import os
import re
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from pathlib import Path


class DomainFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Domain Finder Tool")
        self.root.geometry("800x600")
        
        # Configure style
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Folder selection
        ttk.Label(main_frame, text="Select Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.folder_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.folder_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=5)
        
        # Domain input
        ttk.Label(main_frame, text="Domain to Search:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.domain_input = tk.StringVar()
        domain_entry = ttk.Entry(main_frame, textvariable=self.domain_input, width=50)
        domain_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        domain_entry.bind('<Return>', lambda e: self.search_domain())
        
        # Search button
        ttk.Button(main_frame, text="Search", command=self.search_domain).grid(row=1, column=2, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Results area
        ttk.Label(main_frame, text="Results:").grid(row=3, column=0, sticky=(tk.W, tk.N), pady=5)
        
        # Results text with scrollbar
        self.results_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=80, height=25)
        self.results_text.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Export button
        self.export_btn = ttk.Button(main_frame, text="Export Results", command=self.export_results, state='disabled')
        self.export_btn.grid(row=5, column=2, pady=5)
        
        # Store results for export
        self.current_results = []
        
    def browse_folder(self):
        """Open folder selection dialog"""
        folder = filedialog.askdirectory(title="Select Folder to Search")
        if folder:
            self.folder_path.set(folder)
            
    def search_domain(self):
        """Search for domain in all .txt files in the selected folder"""
        folder = self.folder_path.get()
        domain = self.domain_input.get().strip()
        
        # Validation
        if not folder:
            messagebox.showwarning("No Folder", "Please select a folder to search.")
            return
            
        if not domain:
            messagebox.showwarning("No Domain", "Please enter a domain to search for.")
            return
            
        if not os.path.isdir(folder):
            messagebox.showerror("Invalid Folder", "The selected folder does not exist.")
            return
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.current_results = []
        
        # Start progress bar
        self.progress.start()
        self.status_var.set("Searching...")
        self.root.update()
        
        # Perform search
        try:
            results = self.find_domain_in_files(folder, domain)
            self.display_results(results, domain, folder)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.progress.stop()
            
    def find_domain_in_files(self, folder_path, domain):
        """Search for domain in all .txt files"""
        results = []
        txt_files = list(Path(folder_path).rglob("*.txt"))
        
        # Escape special regex characters in domain
        escaped_domain = re.escape(domain)
        # Create pattern that matches the domain (case-insensitive)
        pattern = re.compile(escaped_domain, re.IGNORECASE)
        
        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, 1):
                    if pattern.search(line):
                        results.append({
                            'file': str(file_path),
                            'line_number': line_num,
                            'line_content': line.strip()
                        })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                
        return results
        
    def display_results(self, results, domain, folder):
        """Display search results in the text area"""
        self.current_results = results
        
        if not results:
            self.results_text.insert(tk.END, f"No matches found for '{domain}' in {folder}\n")
            self.status_var.set("Search completed - No matches found")
            self.export_btn.config(state='disabled')
            return
        
        # Summary
        file_count = len(set(r['file'] for r in results))
        self.results_text.insert(tk.END, f"Found {len(results)} match(es) for '{domain}' in {file_count} file(s)\n")
        self.results_text.insert(tk.END, "=" * 80 + "\n\n")
        
        # Group results by file
        current_file = None
        for result in results:
            if result['file'] != current_file:
                current_file = result['file']
                rel_path = os.path.relpath(current_file, folder)
                self.results_text.insert(tk.END, f"\n📁 File: {rel_path}\n")
                self.results_text.insert(tk.END, "-" * 80 + "\n")
            
            self.results_text.insert(tk.END, f"  Line {result['line_number']}: {result['line_content']}\n")
        
        self.status_var.set(f"Search completed - {len(results)} match(es) found in {file_count} file(s)")
        self.export_btn.config(state='normal')
        
    def export_results(self):
        """Export results to a text file"""
        if not self.current_results:
            messagebox.showinfo("No Results", "No results to export.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Results"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.results_text.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Results exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")


def main():
    root = tk.Tk()
    app = DomainFinderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
