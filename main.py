import tkinter as tk
from tkinter import messagebox
import threading
import time
import pygetwindow as gw
import keyboard

class WindowListPopup:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        master.title("Selecionar Janela")
        master.geometry("300x200")

        self.window_listbox = tk.Listbox(master)
        self.window_listbox.pack(fill=tk.BOTH, expand=True)

        self.select_button = tk.Button(master, text="Selecionar", command=self.select_window)
        self.select_button.pack(pady=5)

    def populate_window_list(self):
        windows = gw.getAllTitles()
        for window in windows:
            self.window_listbox.insert(tk.END, window)

    def select_window(self):
        selected_index = self.window_listbox.curselection()
        if selected_index:
            selected_window = self.window_listbox.get(selected_index)
            self.app.select_entry.delete(0, tk.END)
            self.app.select_entry.insert(0, selected_window)
            self.master.destroy()


class MacroApp:
    def __init__(self, master):
        self.master = master
        master.title("Sistema de Macro")

        self.select_label = tk.Label(master, text="Selecionar janela/executável:")
        self.select_label.pack()

        self.select_entry = tk.Entry(master)
        self.select_entry.pack()

        self.select_entry.bind("<Button-1>", self.show_window_list)

        self.speed_label = tk.Label(master, text="Velocidade (segundos):")
        self.speed_label.pack()

        self.speed_entry = tk.Entry(master)
        self.speed_entry.pack()

        self.keys_label = tk.Label(master, text="Teclas a serem apertadas:")
        self.keys_label.pack()

        self.keys_entry = tk.Entry(master)
        self.keys_entry.pack()

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=5) 

        self.start_button = tk.Button(self.button_frame, text="Iniciar", command=self.start_macro)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Parar", command=self.stop_macro)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.stop_button['state'] = 'disabled'

        self.is_running = False
        self.selected_window = None
        self.macro_thread = None

    def show_window_list(self, event):
        window_list_popup = tk.Toplevel(self.master)
        window_list_popup.grab_set()
        window_list_popup.focus_set()
        window_list_popup.geometry("300x200")

        window_list_app = WindowListPopup(window_list_popup, self)
        window_list_app.populate_window_list()

    def start_macro(self):
        window_title = self.select_entry.get()
        speed = self.speed_entry.get()
        keys = self.keys_entry.get()

        if not window_title:
            messagebox.showerror("Erro", "Selecione uma janela.")
            return

        if not speed:
            messagebox.showerror("Erro", "Digite uma velocidade.")
            return

        if not keys:
            messagebox.showerror("Erro", "Digite as teclas a serem apertadas.")
            return

        try:
            speed = float(speed)
        except ValueError:
            messagebox.showerror("Erro", "A velocidade deve ser um número.")
            return

        target_window = gw.getWindowsWithTitle(window_title)
        if not target_window:
            messagebox.showerror("Erro", "Janela não encontrada.")
            return

        target_window = target_window[0]

        self.is_running = True
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'normal'

        self.macro_thread = threading.Thread(target=self.run_macro, args=(target_window, speed, keys))
        self.macro_thread.start()

    def stop_macro(self):
        self.is_running = False
        if self.macro_thread:
            self.macro_thread.join()
        self.start_button['state'] = 'normal'
        self.stop_button['state'] = 'disabled'

    def run_macro(self, target_window, speed, keys):
        while self.is_running:
            if target_window.isMinimized:  
                time.sleep(1)  
            else:
                target_window.activate()
                keys_list = keys.replace(' ', '').split(',')  
                for key in keys_list:
                    keyboard.press_and_release(key)
                    time.sleep(0.1)  

root = tk.Tk()
app = MacroApp(root)
root.mainloop()