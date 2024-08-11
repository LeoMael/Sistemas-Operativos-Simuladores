import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Funciones para los algoritmos de gestión de disco
def fcfs(requests, start):
    return requests

def sstf(requests, start):
    remaining_requests = sorted(requests, key=lambda x: abs(x - start))
    order = []
    current_position = start
    while remaining_requests:
        closest = min(remaining_requests, key=lambda x: abs(x - current_position))
        remaining_requests.remove(closest)
        order.append(closest)
        current_position = closest
    return order

def scan(requests, start, direction, disk_size):
    requests = [r for r in requests if r <= disk_size]
    requests.sort()
    if direction == 'up':
        up = [r for r in requests if r >= start]
        down = [r for r in requests if r < start]
        return up + [disk_size] + down[::-1]
    else:
        up = [r for r in requests if r < start]
        down = [r for r in requests if r >= start]
        return up + [0] + down[::-1]

def cscan(requests, start, disk_size):
    requests = [r for r in requests if r <= disk_size]
    requests.sort()
    up = [r for r in requests if r >= start]
    down = [r for r in requests if r < start]
    return up + [disk_size, 0] + down

def look(requests, start, direction):
    requests.sort()
    if direction == 'up':
        up = [r for r in requests if r >= start]
        down = [r for r in requests if r < start]
        return up + down[::-1]
    else:
        up = [r for r in requests if r <= start]
        down = [r for r in requests if r > start]
        return up[::-1] + down

def clook(requests, start):
    requests.sort()
    up = [r for r in requests if r >= start]
    down = [r for r in requests if r < start]
    return up + down

def calculate():
    try:
        requests = list(map(int, entry_requests.get().split(',')))
        start = int(entry_start.get())
        algo = var.get()
        use_disk_size = disk_size_var.get()
        
        if use_disk_size:
            disk_size = int(entry_disk_size.get())
            requests = [r for r in requests if r <= disk_size]  # Filtrar solicitudes fuera del rango
        else:
            disk_size = max(requests) if requests else start
        
        if algo == 'Comparar Todos':
            results = {
                'FCFS': fcfs(requests, start),
                'SSTF': sstf(requests, start),
                'SCAN': scan(requests, start, 'up', disk_size),
                'C-SCAN': cscan(requests, start, disk_size),
                'LOOK': look(requests, start, 'up'),
                'C-LOOK': clook(requests, start)
            }
            distances = {key: calculate_distance(start, val) for key, val in results.items()}
            plot_comparison(start, results, distances, disk_size)
            display_comparison(distances)
        else:
            if algo == 'FCFS':
                result = fcfs(requests, start)
            elif algo == 'SSTF':
                result = sstf(requests, start)
            elif algo == 'SCAN':
                result = scan(requests, start, 'up', disk_size)
            elif algo == 'C-SCAN':
                result = cscan(requests, start, disk_size)
            elif algo == 'LOOK':
                result = look(requests, start, 'up')
            elif algo == 'C-LOOK':
                result = clook(requests, start)
            else:
                result = []

            distances, total_distance, avg_distance = calculate_distance(start, result)
            plot_requests(start, result, algo, disk_size)
            display_table(start, result, distances, total_distance, avg_distance)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

def calculate_distance(start, result):
    total_distance = 0
    current_position = start
    distances = []

    for request in result:
        if current_position <= request:
            distance = abs(current_position - request)
        else:
            distance = 0
        distances.append((current_position, request, distance))
        total_distance += distance
        current_position = request

    avg_distance = total_distance / len(result) if result else 0
    return distances, total_distance, avg_distance

def plot_requests(start, result, algo, disk_size):
    for widget in frame_plot.winfo_children():
        widget.destroy()
    
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor('#2e2e2e')
    ax.set_facecolor('#2e2e2e')

    all_positions = [start] + result
    y = np.arange(len(all_positions))
    x = all_positions

    ax.plot(x, y, marker='o', label=algo)
    for i, txt in enumerate(x):
        ax.annotate(txt, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=12, color='#00ff00')

    ax.set_yticks(y)
    ax.set_yticklabels([str(i) for i in y], fontsize=12, color='#ffd700')
    ax.set_xticks(sorted(set(x)))
    ax.set_xticklabels([str(i) for i in sorted(set(x))], fontsize=12, color='#ffd700')
    
    ax.set_ylabel('Orden de servicio', fontsize=14, color='#00ffff')
    ax.set_xlabel('Posición en el disco', fontsize=14, color='#00ffff')
    ax.set_title(f'Gestión de Disco - {algo}', fontsize=16, color='#00ffff')
    
    if algo in ['SCAN', 'LOOK']:
        ax.axvline(x=disk_size, color='#ff6347', linestyle='--')
        ax.axvline(x=0, color='#ff6347', linestyle='--')
    elif algo in ['C-SCAN', 'C-LOOK']:
        ax.axvline(x=disk_size, color='#00ff00', linestyle='--')
        ax.axvline(x=0, color='#00ff00', linestyle='--')

    ax.invert_yaxis()  # Invertir el eje Y para que el orden de servicio esté en el lateral izquierdo

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def plot_comparison(start, results, distances, disk_size):
    for widget in frame_plot.winfo_children():
        widget.destroy()
    
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor('#2e2e2e')
    ax.set_facecolor('#2e2e2e')

    colors = ['#ff6347', '#4682b4', '#3cb371', '#ffa500', '#9370db', '#ff1493']
    for i, (algo, result) in enumerate(results.items()):
        all_positions = [start] + result
        y = np.arange(len(all_positions))
        x = all_positions

        ax.plot(x, y, marker='o', color=colors[i], label=algo)
        for j, txt in enumerate(x):
            ax.annotate(txt, (x[j], y[j]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=12, color='#00ff00')

    ax.set_yticks(np.arange(max(len(r) for r in results.values()) + 1))
    ax.set_yticklabels([str(i) for i in range(max(len(r) for r in results.values()) + 1)], fontsize=12, color='#ffd700')
    
    ax.set_xlabel('Posición en el disco', fontsize=14, color='#00ffff')
    ax.set_title('Comparación de Algoritmos de Gestión de Disco', fontsize=16, color='#00ffff')
    ax.legend(fontsize=12)

    ax.invert_yaxis()  # Invertir el eje Y para que el orden de servicio esté en el lateral izquierdo

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def display_table(start, result, distances, total_distance, avg_distance):
    for widget in frame_table.winfo_children():
        widget.destroy()
    
    columns = ('Desde', 'Hasta', 'Distancia')
    tree = ttk.Treeview(frame_table, columns=columns, show='headings', style="My.Treeview")
    tree.heading('Desde', text='Desde')
    tree.heading('Hasta', text='Hasta')
    tree.heading('Distancia', text='Distancia')

    for (start, end, distance) in distances:
        tree.insert('', tk.END, values=(start, end, distance))

    tree.insert('', tk.END, values=('Total', '', total_distance))
    tree.insert('', tk.END, values=('Promedio', '', avg_distance))
    
    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def display_comparison(distances):
    for widget in frame_table.winfo_children():
        widget.destroy()

    # Crear la tabla de comparación
    columns = ('Algoritmo', 'Total', 'Promedio')
    tree = ttk.Treeview(frame_table, columns=columns, show='headings', style="My.Treeview")
    tree.heading('Algoritmo', text='Algoritmo')
    tree.heading('Total', text='Total')
    tree.heading('Promedio', text='Promedio')

    for algo, (distances, total, avg) in distances.items():
        tree.insert('', tk.END, values=(algo, total, avg))
    
    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Crear la ventana principal con ThemedTk
root = ThemedTk(theme="equilux")
root.title("Gestión de Disco")

# Establecer un fondo oscuro para la ventana principal
root.configure(bg='#2e2e2e')

# Crear el marco para la entrada de datos
frame_input = ttk.Frame(root, padding="10 10 10 10", style="My.TFrame")
frame_input.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

# Establecer un fondo oscuro para el marco de entrada
frame_input.configure(style="My.TFrame")

# Etiqueta y campo para ingresar las solicitudes de disco
label_requests = ttk.Label(frame_input, text="Solicitudes de Disco (separadas por coma):", style="My.TLabel")
label_requests.grid(row=0, column=0, sticky=tk.W, pady=5)
entry_requests = ttk.Entry(frame_input, width=30, style="My.TEntry")
entry_requests.grid(row=0, column=1, pady=5)

# Etiqueta y campo para ingresar la posición inicial del cabezal
label_start = ttk.Label(frame_input, text="Posición Inicial del Cabezal:", style="My.TLabel")
label_start.grid(row=1, column=0, sticky=tk.W, pady=5)
entry_start = ttk.Entry(frame_input, width=30, style="My.TEntry")
entry_start.grid(row=1, column=1, pady=5)

# Checkbutton para seleccionar si se usa tamaño del disco
disk_size_var = tk.BooleanVar()
disk_size_check = ttk.Checkbutton(frame_input, text="Usar tamaño del disco", variable=disk_size_var, style="My.TCheckbutton")
disk_size_check.grid(row=2, columnspan=2, sticky=tk.W, pady=5)

# Etiqueta y campo para ingresar el tamaño del disco (opcional)
label_disk_size = ttk.Label(frame_input, text="Tamaño del Disco (opcional):", style="My.TLabel")
label_disk_size.grid(row=3, column=0, sticky=tk.W, pady=5)
entry_disk_size = ttk.Entry(frame_input, width=30, style="My.TEntry")
entry_disk_size.grid(row=3, column=1, pady=5)

# Radio buttons para seleccionar el algoritmo
var = tk.StringVar()
var.set('FCFS')

label_algo = ttk.Label(frame_input, text="Seleccione el Algoritmo:", style="My.TLabel")
label_algo.grid(row=4, columnspan=2, sticky=tk.W, pady=10)

radio_fcfs = ttk.Radiobutton(frame_input, text="FCFS", variable=var, value='FCFS', style="My.TRadiobutton")
radio_fcfs.grid(row=5, columnspan=2, sticky=tk.W)
radio_sstf = ttk.Radiobutton(frame_input, text="SSTF", variable=var, value='SSTF', style="My.TRadiobutton")
radio_sstf.grid(row=6, columnspan=2, sticky=tk.W)
radio_scan = ttk.Radiobutton(frame_input, text="SCAN", variable=var, value='SCAN', style="My.TRadiobutton")
radio_scan.grid(row=7, columnspan=2, sticky=tk.W)
radio_cscan = ttk.Radiobutton(frame_input, text="C-SCAN", variable=var, value='C-SCAN', style="My.TRadiobutton")
radio_cscan.grid(row=8, columnspan=2, sticky=tk.W)
radio_look = ttk.Radiobutton(frame_input, text="LOOK", variable=var, value='LOOK', style="My.TRadiobutton")
radio_look.grid(row=9, columnspan=2, sticky=tk.W)
radio_clook = ttk.Radiobutton(frame_input, text="C-LOOK", variable=var, value='C-LOOK', style="My.TRadiobutton")
radio_clook.grid(row=10, columnspan=2, sticky=tk.W)
radio_compare = ttk.Radiobutton(frame_input, text="Comparar Todos", variable=var, value='Comparar Todos', style="My.TRadiobutton")
radio_compare.grid(row=11, columnspan=2, sticky=tk.W)

# Botón para calcular el orden de servicio
button_calculate = ttk.Button(frame_input, text="Calcular", command=calculate, style="My.TButton")
button_calculate.grid(row=12, columnspan=2, pady=10)

# Crear el marco para el gráfico y la tabla
frame_plot_table = ttk.Frame(root, padding="10 10 10 10", style="My.TFrame")
frame_plot_table.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Crear el marco para el gráfico
frame_plot = ttk.Frame(frame_plot_table, padding="10 10 10 10", style="My.TFrame")
frame_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Crear el marco para la tabla
frame_table = ttk.Frame(frame_plot_table, padding="10 10 10 10", style="My.TFrame")
frame_table.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Establecer estilos personalizados para ttk
style = ttk.Style()
style.configure("My.TFrame", background="#2e2e2e")
style.configure("My.TLabel", background="#2e2e2e", foreground="#00ffff")
style.configure("My.TEntry", fieldbackground="#4a4a4a", foreground="#ffffff")
style.configure("My.TCheckbutton", background="#2e2e2e", foreground="#00ffff")
style.configure("My.TRadiobutton", background="#2e2e2e", foreground="#00ffff")
style.configure("My.TButton", background="#4a4a4a", foreground="#00ffff")
style.configure("My.Treeview", background="#2e2e2e", fieldbackground="#2e2e2e", foreground="#ffffff", rowheight=30, font=('Arial', 12))
style.map('My.Treeview', background=[('selected', '#00ffff')], foreground=[('selected', '#000000')])

# Ejecutar el bucle principal de Tkinter
root.mainloop()
