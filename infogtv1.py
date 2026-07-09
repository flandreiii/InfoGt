#!/usr/bin/env python3
"""
InfoGt GUI - Advanced Network Reconnaissance Tool with GUI
Author: flandreiii
Tested on: Parrot OS
Features: Multiple scan modes, proxychains4 support, real-time output
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
import socket
from datetime import datetime
from pathlib import Path
import os


class InfoGtGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("InfoGt - Network Reconnaissance Tool")
        self.root.geometry("1100x700")
        self.root.configure(bg="#1e1e1e")
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background="#1e1e1e")
        self.style.configure('TLabel', background="#1e1e1e", foreground="#00ff00")
        self.style.configure('TButton', background="#333333", foreground="#00ff00")
        self.style.configure('TEntry', fieldbackground="#222222", foreground="#00ff00")
        
        self.colors = {
            'green': '#00ff00',
            'red': '#ff0000',
            'yellow': '#ffff00',
            'blue': '#00aaff',
            'dark': '#1e1e1e',
            'darker': '#0a0a0a'
        }
        
        self.is_scanning = False
        self.scan_thread = None
        self.use_proxy = tk.BooleanVar(value=False)
        self.output_file = None
        
        self.setup_ui()

    def setup_ui(self):
        """Setup main UI"""
        # Banner
        banner_frame = tk.Frame(self.root, bg=self.colors['darker'], height=60)
        banner_frame.pack(fill=tk.X)
        banner_frame.pack_propagate(False)
        
        banner_label = tk.Label(
            banner_frame,
            text="╔═══════════════════════════════════╗\n║         InfoGt v1.0               ║\n║    Network Reconnaissance Tool    ║\n║        by flandreiii              ║\n╚═══════════════════════════════════╝",
            bg=self.colors['darker'],
            fg=self.colors['blue'],
            font=("Courier", 9),
            justify=tk.CENTER
        )
        banner_label.pack(pady=8)
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, bg=self.colors['dark'], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        left_panel.pack_propagate(False)
        
        # Target section
        target_label = tk.Label(
            left_panel,
            text="▸ TARGET",
            bg=self.colors['dark'],
            fg=self.colors['green'],
            font=("Courier", 10, "bold")
        )
        target_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.target_var = tk.StringVar()
        target_entry = ttk.Entry(left_panel, textvariable=self.target_var, width=35)
        target_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        target_entry.insert(0, "192.168.1.0/24")
        
        # Mode section
        mode_label = tk.Label(
            left_panel,
            text="▸ SCAN MODE",
            bg=self.colors['dark'],
            fg=self.colors['green'],
            font=("Courier", 10, "bold")
        )
        mode_label.pack(anchor=tk.W, pady=(15, 5))
        
        modes = [
            ("Quick Scan", "quick"),
            ("Standard Scan", "standard"),
            ("Aggressive Scan", "aggressive"),
            ("Stealth Scan", "stealth"),
            ("UDP Scan", "udp"),
            ("Vulnerability Scan", "vuln"),
            ("Ping Sweep", "ping"),
            ("Service Scan", "service")
        ]
        
        self.mode_var = tk.StringVar(value="quick")
        
        mode_frame = tk.Frame(left_panel, bg=self.colors['dark'])
        mode_frame.pack(fill=tk.X, padx=10, pady=(0, 15))
        
        for text, value in modes:
            rb = tk.Radiobutton(
                mode_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                bg=self.colors['dark'],
                fg=self.colors['green'],
                selectcolor=self.colors['darker'],
                activebackground=self.colors['dark'],
                activeforeground=self.colors['yellow']
            )
            rb.pack(anchor=tk.W, pady=2)
        
        # Options section
        options_label = tk.Label(
            left_panel,
            text="▸ OPTIONS",
            bg=self.colors['dark'],
            fg=self.colors['green'],
            font=("Courier", 10, "bold")
        )
        options_label.pack(anchor=tk.W, pady=(15, 5))
        
        proxy_check = tk.Checkbutton(
            left_panel,
            text="Use Proxychains4",
            variable=self.use_proxy,
            bg=self.colors['dark'],
            fg=self.colors['green'],
            selectcolor=self.colors['darker'],
            activebackground=self.colors['dark'],
            activeforeground=self.colors['yellow']
        )
        proxy_check.pack(anchor=tk.W, padx=10, pady=3)
        
        # Output file
        output_frame = tk.Frame(left_panel, bg=self.colors['dark'])
        output_frame.pack(fill=tk.X, padx=10, pady=(10, 15))
        
        output_label = tk.Label(
            output_frame,
            text="Save results to:",
            bg=self.colors['dark'],
            fg=self.colors['green'],
            font=("Courier", 9)
        )
        output_label.pack(side=tk.LEFT)
        
        browse_btn = tk.Button(
            output_frame,
            text="Browse",
            command=self.select_output_file,
            bg="#333333",
            fg=self.colors['green'],
            activebackground="#555555",
            activeforeground=self.colors['yellow'],
            relief=tk.FLAT,
            padx=5
        )
        browse_btn.pack(side=tk.RIGHT)
        
        self.output_label = tk.Label(
            left_panel,
            text="(none)",
            bg=self.colors['dark'],
            fg=self.colors['yellow'],
            font=("Courier", 8),
            wraplength=250
        )
        self.output_label.pack(anchor=tk.W, padx=10, pady=(0, 15))
        
        # Buttons
        scan_btn = tk.Button(
            left_panel,
            text="▶ START SCAN",
            command=self.start_scan,
            bg="#1a5f1a",
            fg=self.colors['green'],
            activebackground="#2a7f2a",
            activeforeground=self.colors['yellow'],
            relief=tk.FLAT,
            font=("Courier", 10, "bold"),
            padx=20,
            pady=8
        )
        scan_btn.pack(fill=tk.X, padx=10, pady=(20, 5))
        
        self.stop_btn = tk.Button(
            left_panel,
            text="⏹ STOP SCAN",
            command=self.stop_scan,
            bg="#5f1a1a",
            fg=self.colors['red'],
            activebackground="#7f2a2a",
            activeforeground=self.colors['yellow'],
            relief=tk.FLAT,
            font=("Courier", 10, "bold"),
            padx=20,
            pady=8,
            state=tk.DISABLED
        )
        self.stop_btn.pack(fill=tk.X, padx=10, pady=5)
        
        clear_btn = tk.Button(
            left_panel,
            text="⎌ CLEAR OUTPUT",
            command=self.clear_output,
            bg="#333333",
            fg=self.colors['blue'],
            activebackground="#555555",
            activeforeground=self.colors['yellow'],
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        clear_btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Status
        self.status_label = tk.Label(
            left_panel,
            text="Status: Ready",
            bg=self.colors['dark'],
            fg=self.colors['green'],
            font=("Courier", 9),
            wraplength=280
        )
        self.status_label.pack(anchor=tk.W, padx=10, pady=(20, 0), fill=tk.X)
        
        # Right panel - Output
        right_panel = tk.Frame(main_container, bg=self.colors['dark'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        output_label = tk.Label(
            right_panel,
            text="▸ SCAN OUTPUT",
            bg=self.colors['dark'],
            fg=self.colors['green'],
            font=("Courier", 10, "bold")
        )
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            right_panel,
            bg=self.colors['darker'],
            fg=self.colors['green'],
            insertbackground=self.colors['green'],
            wrap=tk.WORD,
            font=("Courier", 9)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for colored output
        self.output_text.tag_config("success", foreground=self.colors['green'])
        self.output_text.tag_config("error", foreground=self.colors['red'])
        self.output_text.tag_config("warning", foreground=self.colors['yellow'])
        self.output_text.tag_config("info", foreground=self.colors['blue'])

    def select_output_file(self):
        """Select output file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.output_file = filename
            self.output_label.config(text=Path(filename).name)

    def validate_target(self, target):
        """Validate target"""
        try:
            socket.inet_aton(target.split('/')[0])
            return True
        except socket.error:
            try:
                socket.gethostbyname(target)
                return True
            except socket.gaierror:
                return False

    def print_message(self, message, tag="info"):
        """Print message to output"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.output_text.see(tk.END)
        self.root.update()

    def start_scan(self):
        """Start scan in separate thread"""
        target = self.target_var.get().strip()
        
        if not target:
            messagebox.showerror("Error", "Please enter a target")
            return
        
        if not self.validate_target(target):
            messagebox.showerror("Error", "Invalid target IP or domain")
            return
        
        self.is_scanning = True
        self.scan_thread = threading.Thread(target=self.execute_scan, args=(target,))
        self.scan_thread.daemon = True
        self.scan_thread.start()

    def stop_scan(self):
        """Stop current scan"""
        if self.is_scanning:
            self.is_scanning = False
            self.print_message("Stopping scan...", "warning")

    def execute_scan(self, target):
        """Execute scan"""
        try:
            self.root.after(0, self.update_ui_scanning, True)
            
            mode = self.mode_var.get()
            use_proxy = self.use_proxy.get()
            
            self.print_message(f"[*] Target validated: {target}", "info")
            self.print_message(f"[*] Scan mode: {mode.upper()}", "info")
            
            if use_proxy:
                self.print_message(f"[*] Using Proxychains4", "info")
            
            self.print_message(f"[*] Starting scan at {datetime.now().strftime('%H:%M:%S')}", "info")
            self.print_message("=" * 60, "info")
            
            # Build command
            cmd_base = ["sudo", "nmap"]
            if use_proxy:
                cmd_base = ["sudo", "proxychains4"] + cmd_base
            
            scan_commands = {
                'quick': ["-F", "--open"],
                'standard': ["-p-", "-sV", "--open"],
                'aggressive': ["-p-", "-sV", "-O", "-sC", "--open"],
                'stealth': ["-p-", "-sS", "-T2", "--open"],
                'udp': ["-p-", "-sU", "--open", "-T2"],
                'vuln': ["-p-", "-sV", "-sC", "--script=vuln"],
                'ping': ["-sn"],
                'service': ["-p-", "-sV", "-sC", "--version-all"]
            }
            
            cmd = cmd_base + scan_commands[mode] + [target]
            
            # Execute
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            if self.output_file:
                output_file_obj = open(self.output_file, 'w')
            
            while True:
                if not self.is_scanning:
                    process.terminate()
                    break
                
                line = process.stdout.readline()
                if not line:
                    break
                
                line = line.rstrip()
                self.print_message(line, "info")
                
                if self.output_file:
                    output_file_obj.write(line + "\n")
            
            if self.output_file:
                output_file_obj.close()
            
            process.wait()
            
            self.print_message("=" * 60, "info")
            
            if process.returncode == 0:
                self.print_message(f"[+] Scan completed successfully at {datetime.now().strftime('%H:%M:%S')}", "success")
                if self.output_file:
                    self.print_message(f"[+] Results saved to: {self.output_file}", "success")
            else:
                self.print_message(f"[-] Scan finished with code {process.returncode}", "warning")
        
        except Exception as e:
            self.print_message(f"[-] Error: {str(e)}", "error")
        
        finally:
            self.root.after(0, self.update_ui_scanning, False)

    def update_ui_scanning(self, scanning):
        """Update UI during scan"""
        if scanning:
            self.status_label.config(text="Status: Scanning...", fg=self.colors['yellow'])
            self.stop_btn.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="Status: Ready", fg=self.colors['green'])
            self.stop_btn.config(state=tk.DISABLED)

    def clear_output(self):
        """Clear output text"""
        self.output_text.delete('1.0', tk.END)
        self.print_message("[*] Output cleared", "info")


def main():
    root = tk.Tk()
    app = InfoGtGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
