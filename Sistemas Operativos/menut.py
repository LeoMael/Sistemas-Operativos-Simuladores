import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import subprocess
import threading
import queue
import os
import psutil
import sys

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú de Proyectos")
        self.geometry("1200x600")
        self.configure(bg="#2c3e50")  # Fondo oscuro

        self.queue = queue.Queue()
        self.process_counts = {"python1": 0, "python2": 0, "cpp": 0}
        self.processes = {"python1": None, "python2": None, "cpp": None}

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="Selecciona un Proyecto", font=("Arial", 24, "bold"), bg="#2c3e50", fg="#f5f5f5")
        title.pack(pady=20)

        main_frame = tk.Frame(self, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left_frame = tk.Frame(main_frame, bg="#2c3e50")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        btn_frame = tk.Frame(left_frame, bg="#2c3e50")
        btn_frame.pack(fill=tk.Y)

        self.preview_image_label = tk.Label(main_frame, bg="#2c3e50")
        self.preview_image_label.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        btn_style = {"font": ("Arial", 12), "relief": "flat", "bd": 0, "fg": "#f5f5f5"}

        btn_python1 = tk.Button(btn_frame, text="Politicas y memoria", command=self.run_python_project1, bg="#3498db", **btn_style, width=40)
        btn_python1.grid(row=0, column=0, padx=5, pady=5)
        btn_python1.bind("<Enter>", lambda e: self.show_preview("ram.png"))
        btn_python1.bind("<Leave>", lambda e: self.hide_preview())

        btn_python2 = tk.Button(btn_frame, text="Gestion de disco", command=self.run_python_project2, bg="#3498db", **btn_style, width=40)
        btn_python2.grid(row=1, column=0, padx=5, pady=5)
        btn_python2.bind("<Enter>", lambda e: self.show_preview("gdisco.png"))
        btn_python2.bind("<Leave>", lambda e: self.hide_preview())

        btn_cpp = tk.Button(btn_frame, text="Abrir consola", command=self.run_cpp_project, bg="#e74c3c", **btn_style, width=40)
        btn_cpp.grid(row=2, column=0, padx=5, pady=5)
        btn_cpp.bind("<Enter>", lambda e: self.show_preview("consola.png"))
        btn_cpp.bind("<Leave>", lambda e: self.hide_preview())

        btn_exit = tk.Button(btn_frame, text="Salir", command=self.exit_app, bg="#95a5a6", **btn_style, width=35)
        btn_exit.grid(row=3, column=0, padx=5, pady=5)

        terminate_frame = tk.Frame(btn_frame, bg="#2c3e50")
        terminate_frame.grid(row=4, column=0, padx=5, pady=10)

        btn_terminate_python1 = tk.Button(terminate_frame, text="Cerrar PyM", command=lambda: self.terminate_process("python1"), bg="#e67e22", **btn_style, width=20)
        btn_terminate_python1.grid(row=0, column=0, padx=5, pady=5)

        btn_terminate_python2 = tk.Button(terminate_frame, text="Cerrar GD", command=lambda: self.terminate_process("python2"), bg="#e67e22", **btn_style, width=20)
        btn_terminate_python2.grid(row=1, column=0, padx=5, pady=5)

        btn_terminate_cpp = tk.Button(terminate_frame, text="Cerrar consola", command=lambda: self.terminate_process("cpp"), bg="#e67e22", **btn_style, width=20)
        btn_terminate_cpp.grid(row=2, column=0, padx=5, pady=5)

        btn_terminate_all = tk.Button(terminate_frame, text="Cerrar Todos", command=self.terminate_all_processes, bg="#c0392b", **btn_style, width=25)
        btn_terminate_all.grid(row=3, column=0, padx=5, pady=5)

        self.output_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, height=10, bg="#34495e", fg="#f5f5f5", font=("Arial", 12), width=40, relief="flat")
        self.output_text.pack(padx=5, pady=10)

    def show_preview(self, image_path):
        image = Image.open(image_path)
        image = image.resize((600, 450), Image.Resampling.LANCZOS)  # Tamaño ajustado
        self.photo = ImageTk.PhotoImage(image)
        self.preview_image_label.config(image=self.photo)

    def hide_preview(self):
        self.preview_image_label.config(image='')

    def run_python_project1(self):
        if self.process_counts["python1"] >= 1:
            self.queue.put("El proyecto en Python 1 ya está en ejecución.\n")
            self.show_output()
            return
        self.queue.put("Iniciando el proyecto en Python 1...\n")
        self.show_output()
        threading.Thread(target=self.execute_python_project, args=('simulacion_procesos.py', "python1"), daemon=True).start()

    def run_python_project2(self):
        if self.process_counts["python2"] >= 1:
            self.queue.put("El proyecto en Python 2 ya está en ejecución.\n")
            self.show_output()
            return
        self.queue.put("Iniciando el proyecto en Python 2...\n")
        self.show_output()
        threading.Thread(target=self.execute_python_project, args=('simulador_gd.py', "python2"), daemon=True).start()

    def execute_python_project(self, script_name, project_key):
        self.process_counts[project_key] += 1
        process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes[project_key] = process
        stdout, stderr = process.communicate()
        output = stdout.decode() + stderr.decode()
        self.queue.put(output)
        self.show_output()
        self.process_counts[project_key] -= 1
        self.processes[project_key] = None
        messagebox.showinfo("Información", f"Proyecto en Python '{script_name}' ejecutado.")

    def run_cpp_project(self):
        if self.process_counts["cpp"] >= 1:
            self.queue.put("El proyecto en C++ ya está en ejecución.\n")
            self.show_output()
            return
        self.queue.put("Iniciando el proyecto en C++...\n")
        self.show_output()
        threading.Thread(target=self.compile_and_run_cpp_project, daemon=True).start()

    def compile_and_run_cpp_project(self):
        self.process_counts["cpp"] += 1
        self.queue.put("Compilando el proyecto en C++...\n")
        self.show_output()

        executable_path = 'cpp_project_executable.exe'
        if os.path.exists(executable_path):
            try:
                self.terminate_executable(executable_path)
                os.remove(executable_path)
            except Exception as e:
                self.queue.put(f"No se pudo eliminar el archivo ejecutable anterior: {e}\n")
                self.show_output()
                self.process_counts["cpp"] -= 1
                return

        compile_command = 'g++ simulacion_de_directorios_tipo_arbol.cpp -o cpp_project_executable'
        compile_output = self.execute_command(compile_command)
        self.queue.put(compile_output)
        self.show_output()

        if "error" not in compile_output.lower():
            self.queue.put("\nCompilación exitosa. Ejecutando el proyecto en C++...\n")
            self.show_output()
            self.processes["cpp"] = subprocess.Popen('cpp_project_executable.exe', creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.processes["cpp"].wait()
            self.processes["cpp"] = None
        else:
            self.queue.put("Error en la compilación del proyecto en C++.\n")
            self.show_output()
        self.process_counts["cpp"] -= 1

    def terminate_process(self, project_key):
        if self.processes[project_key]:
            self.processes[project_key].terminate()
            self.processes[project_key].wait()
            self.queue.put(f"El proceso '{project_key}' ha sido terminado.\n")
            self.show_output()
            self.processes[project_key] = None
            self.process_counts[project_key] = 0
        else:
            self.queue.put(f"No hay proceso '{project_key}' en ejecución.\n")
            self.show_output()

    def terminate_all_processes(self):
        for key in self.processes:
            self.terminate_process(key)
        self.queue.put("Todos los procesos han sido terminados.\n")
        self.show_output()

    def terminate_executable(self, executable_path):
        for proc in psutil.process_iter():
            try:
                if proc.name() == os.path.basename(executable_path):
                    proc.terminate()
                    proc.wait()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def execute_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        return stdout.decode() + stderr.decode()

    def show_output(self):
        while not self.queue.empty():
            output = self.queue.get()
            self.output_text.insert(tk.END, output)
            self.output_text.see(tk.END)

    def exit_app(self):
        self.terminate_all_processes()
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.mainloop()
