import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from controllers import HospitalController

class DashboardView(tk.Tk):
    def __init__(self, medico_info):
        super().__init__()
        self.title("Sistema de Interoperabilidad Hospitalaria")
        self.geometry("1080x650")
        self.minsize(1000, 620)

        self.controller = HospitalController()
        self.medico = medico_info
        self.paciente_actual = None
        self.atencion_actual_id = None
        self.logo_img = None

        self._configurar_estilos()
        self._crear_encabezado()
        self._crear_tabs()

    def _ruta_recurso(self, ruta_relativa):
        if hasattr(sys, "_MEIPASS"):
            base = sys._MEIPASS
        else:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return os.path.join(base, ruta_relativa)

    def _cargar_logo(self, ancho_aproximado=76):
        ruta_logo = self._ruta_recurso(os.path.join("assets", "logo", "Logo.png"))
        if not os.path.exists(ruta_logo):
            print(f"Advertencia: no se encontro el logo en {ruta_logo}")
            return None
        try:
            imagen = tk.PhotoImage(file=ruta_logo)
            if imagen.width() > ancho_aproximado:
                factor = max(1, imagen.width() // ancho_aproximado)
                imagen = imagen.subsample(factor, factor)
            return imagen
        except Exception as error:
            print(f"Advertencia: no se pudo cargar el logo: {error}")
            return None

    def _configurar_estilos(self):
        self.configure(bg="#eef3f8")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Main.TFrame", background="#eef3f8")
        self.style.configure("Panel.TFrame", background="#ffffff")
        self.style.configure("Header.TFrame", background="#0f5f9f")
        self.style.configure("HeaderTitle.TLabel", background="#0f5f9f", foreground="#ffffff", font=("Segoe UI", 16, "bold"))
        self.style.configure("HeaderInfo.TLabel", background="#0f5f9f", foreground="#d8ecff", font=("Segoe UI", 10))
        self.style.configure("Section.TLabelframe", background="#ffffff", foreground="#183b56", padding=12)
        self.style.configure("Section.TLabelframe.Label", background="#ffffff", foreground="#183b56", font=("Segoe UI", 10, "bold"))
        self.style.configure("Field.TLabel", background="#ffffff", foreground="#1f2d3d", font=("Segoe UI", 10))
        self.style.configure("Status.TLabel", background="#ffffff", foreground="#637381", font=("Segoe UI", 10, "italic"))
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=7, background="#0f5f9f", foreground="#ffffff")
        self.style.map("Primary.TButton", background=[("active", "#0b5cad")], foreground=[("active", "#ffffff")])
        self.style.configure("TNotebook", background="#eef3f8", borderwidth=0)
        self.style.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=(16, 8))
        self.style.configure("Treeview", font=("Segoe UI", 9), rowheight=28, background="#ffffff", fieldbackground="#ffffff")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#dbe9f6", foreground="#183b56")

    def _crear_encabezado(self):
        header = ttk.Frame(self, style="Header.TFrame", padding=18)
        header.pack(fill=tk.X, side=tk.TOP)
        header.columnconfigure(1, weight=1)

        self.logo_img = self._cargar_logo(76)
        if self.logo_img:
            ttk.Label(header, image=self.logo_img, background="#0f5f9f").grid(row=0, column=0, rowspan=2, sticky=tk.W, padx=(0, 14))

        titulo = "Sistema de Interoperabilidad Hospitalaria"
        ttk.Label(header, text=titulo, style="HeaderTitle.TLabel").grid(row=0, column=1, sticky=tk.W)

        texto_medico = f"Medico: {self.medico['nombre']}    |    Sede: {self.medico['nombre_est']}"
        ttk.Label(header, text=texto_medico, style="HeaderInfo.TLabel").grid(row=1, column=1, sticky=tk.W, pady=(6, 0))

    def _crear_tabs(self):
        contenedor = ttk.Frame(self, style="Main.TFrame", padding=14)
        contenedor.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(contenedor)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = ttk.Frame(self.notebook, style="Panel.TFrame", padding=14)
        self.tab2 = ttk.Frame(self.notebook, style="Panel.TFrame", padding=14)
        self.tab3 = ttk.Frame(self.notebook, style="Panel.TFrame", padding=14)
        self.tab4 = ttk.Frame(self.notebook, style="Panel.TFrame", padding=14)

        self.notebook.add(self.tab1, text="Busqueda e historia clinica")
        self.notebook.add(self.tab2, text="Registro de atencion")
        self.notebook.add(self.tab3, text="Derivacion por DNI")
        self.notebook.add(self.tab4, text="Registro de paciente")

        self._disenar_tab1()
        self._disenar_tab2()
        self._disenar_tab3()
        self._disenar_tab4()

    def _disenar_tab1(self):
        f_busqueda = ttk.LabelFrame(self.tab1, text="Busqueda de paciente por DNI", style="Section.TLabelframe")
        f_busqueda.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(f_busqueda, text="DNI:", style="Field.TLabel").grid(row=0, column=0, sticky=tk.W, padx=(0, 8))
        self.txt_buscar_dni = ttk.Entry(f_busqueda, width=18)
        self.txt_buscar_dni.grid(row=0, column=1, sticky=tk.W, padx=(0, 8))
        ttk.Button(f_busqueda, text="Buscar historial", style="Primary.TButton", command=self._buscar_paciente).grid(row=0, column=2, sticky=tk.W)

        self.lbl_paciente_info = ttk.Label(self.tab1, text="Paciente no seleccionado", style="Status.TLabel")
        self.lbl_paciente_info.pack(anchor=tk.W, pady=(0, 10))

        f_tree = ttk.LabelFrame(self.tab1, text="Historia clinica unificada", style="Section.TLabelframe")
        f_tree.pack(fill=tk.BOTH, expand=True)

        columnas = ("fecha", "establecimiento", "distrito", "medico", "motivo", "diagnostico", "tratamiento")
        self.tree = ttk.Treeview(f_tree, columns=columnas, show="headings")

        encabezados = {
            "fecha": "Fecha/Hora",
            "establecimiento": "Establecimiento",
            "distrito": "Distrito",
            "medico": "Medico tratante",
            "motivo": "Motivo",
            "diagnostico": "Diagnostico",
            "tratamiento": "Tratamiento"
        }

        anchos = {
            "fecha": 130,
            "establecimiento": 170,
            "distrito": 110,
            "medico": 150,
            "motivo": 150,
            "diagnostico": 150,
            "tratamiento": 170
        }

        for col in columnas:
            self.tree.heading(col, text=encabezados[col])
            self.tree.column(col, width=anchos[col], anchor=tk.CENTER)

        scroll_y = ttk.Scrollbar(f_tree, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(f_tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        scroll_y.grid(row=0, column=1, sticky=tk.NS)
        scroll_x.grid(row=1, column=0, sticky=tk.EW)
        f_tree.rowconfigure(0, weight=1)
        f_tree.columnconfigure(0, weight=1)

    def _disenar_tab2(self):
        f_form = ttk.LabelFrame(self.tab2, text="Nueva atencion medica", style="Section.TLabelframe")
        f_form.pack(fill=tk.BOTH, expand=True)
        f_form.columnconfigure(1, weight=1)

        ttk.Label(f_form, text="Tipo de atencion:", style="Field.TLabel").grid(row=0, column=0, sticky=tk.W, pady=8, padx=(0, 12))
        self.combo_tipo_atencion = ttk.Combobox(f_form, values=["Consulta", "Emergencia", "Hospitalizacion"], state="readonly", width=28)
        self.combo_tipo_atencion.grid(row=0, column=1, sticky=tk.W, pady=8)
        self.combo_tipo_atencion.current(0)

        ttk.Label(f_form, text="Motivo:", style="Field.TLabel").grid(row=1, column=0, sticky=tk.NW, pady=8, padx=(0, 12))
        self.txt_motivo = tk.Text(f_form, height=4, bg="#ffffff", fg="#1f2d3d", relief=tk.SOLID, borderwidth=1, font=("Segoe UI", 10))
        self.txt_motivo.grid(row=1, column=1, sticky=tk.EW, pady=8)

        ttk.Label(f_form, text="Diagnostico:", style="Field.TLabel").grid(row=2, column=0, sticky=tk.NW, pady=8, padx=(0, 12))
        self.txt_diagnostico = tk.Text(f_form, height=4, bg="#ffffff", fg="#1f2d3d", relief=tk.SOLID, borderwidth=1, font=("Segoe UI", 10))
        self.txt_diagnostico.grid(row=2, column=1, sticky=tk.EW, pady=8)

        ttk.Label(f_form, text="Tratamiento:", style="Field.TLabel").grid(row=3, column=0, sticky=tk.NW, pady=8, padx=(0, 12))
        self.txt_tratamiento = tk.Text(f_form, height=4, bg="#ffffff", fg="#1f2d3d", relief=tk.SOLID, borderwidth=1, font=("Segoe UI", 10))
        self.txt_tratamiento.grid(row=3, column=1, sticky=tk.EW, pady=8)

        ttk.Button(f_form, text="Guardar registro clinico", style="Primary.TButton", command=self._guardar_atencion).grid(row=4, column=1, sticky=tk.E, pady=14)

    def _disenar_tab3(self):
        f_derivacion = ttk.LabelFrame(self.tab3, text="Derivacion interhospitalaria por DNI", style="Section.TLabelframe")
        f_derivacion.pack(fill=tk.BOTH, expand=True)
        f_derivacion.columnconfigure(1, weight=1)

        ttk.Label(f_derivacion, text="DNI del paciente:", style="Field.TLabel").grid(row=0, column=0, sticky=tk.W, pady=8, padx=(0, 12))
        self.txt_dni_derivacion = ttk.Entry(f_derivacion, width=18)
        self.txt_dni_derivacion.grid(row=0, column=1, sticky=tk.W, pady=8)

        ttk.Label(f_derivacion, text="Establecimiento destino:", style="Field.TLabel").grid(row=1, column=0, sticky=tk.W, pady=8, padx=(0, 12))
        self.combo_destino = ttk.Combobox(f_derivacion, state="readonly")
        self.combo_destino.grid(row=1, column=1, sticky=tk.EW, pady=8)

        lista_est = self.controller.obtener_establecimientos()
        self.lista_est_destino = [est for est in lista_est if est[0] != self.medico["id_est"]]
        self.combo_destino["values"] = [est[1] for est in self.lista_est_destino]

        ttk.Label(f_derivacion, text="Motivo o especialidad:", style="Field.TLabel").grid(row=2, column=0, sticky=tk.NW, pady=8, padx=(0, 12))
        self.txt_motivo_derivacion = tk.Text(f_derivacion, height=6, bg="#ffffff", fg="#1f2d3d", relief=tk.SOLID, borderwidth=1, font=("Segoe UI", 10))
        self.txt_motivo_derivacion.grid(row=2, column=1, sticky=tk.EW, pady=8)

        ttk.Label(f_derivacion, text="Estado:", style="Field.TLabel").grid(row=3, column=0, sticky=tk.W, pady=8, padx=(0, 12))
        self.combo_estado_derivacion = ttk.Combobox(f_derivacion, values=["Pendiente", "Aceptada", "Observada"], state="readonly", width=20)
        self.combo_estado_derivacion.grid(row=3, column=1, sticky=tk.W, pady=8)
        self.combo_estado_derivacion.current(0)

        nota = "Puede derivar por DNI. Si viene de una atencion recien registrada, el sistema conserva esa relacion."
        ttk.Label(f_derivacion, text=nota, style="Status.TLabel").grid(row=4, column=1, sticky=tk.W, pady=(0, 10))

        ttk.Button(f_derivacion, text="Derivar paciente", style="Primary.TButton", command=self._guardar_derivacion).grid(row=5, column=1, sticky=tk.E, pady=12)

    def _disenar_tab4(self):
        f_paciente = ttk.LabelFrame(self.tab4, text="Registro de paciente nuevo", style="Section.TLabelframe")
        f_paciente.pack(fill=tk.BOTH, expand=True)
        f_paciente.columnconfigure(1, weight=1)
        f_paciente.columnconfigure(3, weight=1)

        ttk.Label(f_paciente, text="DNI:", style="Field.TLabel").grid(row=0, column=0, sticky=tk.W, pady=8, padx=(0, 12))
        self.txt_pac_dni = ttk.Entry(f_paciente, width=20)
        self.txt_pac_dni.grid(row=0, column=1, sticky=tk.W, pady=8)

        ttk.Label(f_paciente, text="Telefono:", style="Field.TLabel").grid(row=0, column=2, sticky=tk.W, pady=8, padx=(20, 12))
        self.txt_pac_telefono = ttk.Entry(f_paciente, width=20)
        self.txt_pac_telefono.grid(row=0, column=3, sticky=tk.W, pady=8)

        ttk.Label(f_paciente, text="Nombres:", style="Field.TLabel").grid(row=1, column=0, sticky=tk.W, pady=8, padx=(0, 12))
        self.txt_pac_nombres = ttk.Entry(f_paciente)
        self.txt_pac_nombres.grid(row=1, column=1, columnspan=3, sticky=tk.EW, pady=8)

        ttk.Label(f_paciente, text="Apellidos:", style="Field.TLabel").grid(row=2, column=0, sticky=tk.W, pady=8, padx=(0, 12))
        self.txt_pac_apellidos = ttk.Entry(f_paciente)
        self.txt_pac_apellidos.grid(row=2, column=1, columnspan=3, sticky=tk.EW, pady=8)

        ttk.Label(f_paciente, text="Fecha nacimiento:", style="Field.TLabel").grid(row=3, column=0, sticky=tk.W, pady=8, padx=(0, 12))
        self.txt_pac_fecha = ttk.Entry(f_paciente, width=20)
        self.txt_pac_fecha.grid(row=3, column=1, sticky=tk.W, pady=8)
        self.txt_pac_fecha.insert(0, "1990-01-01")

        ttk.Label(f_paciente, text="Sexo:", style="Field.TLabel").grid(row=3, column=2, sticky=tk.W, pady=8, padx=(20, 12))
        self.combo_pac_sexo = ttk.Combobox(f_paciente, values=["M", "F"], state="readonly", width=8)
        self.combo_pac_sexo.grid(row=3, column=3, sticky=tk.W, pady=8)

        ttk.Label(f_paciente, text="Direccion:", style="Field.TLabel").grid(row=4, column=0, sticky=tk.W, pady=8, padx=(0, 12))
        self.txt_pac_direccion = ttk.Entry(f_paciente)
        self.txt_pac_direccion.grid(row=4, column=1, columnspan=3, sticky=tk.EW, pady=8)

        ttk.Label(f_paciente, text="Seguro:", style="Field.TLabel").grid(row=5, column=0, sticky=tk.W, pady=8, padx=(0, 12))
        self.combo_pac_seguro = ttk.Combobox(f_paciente, values=["SIS", "EsSalud", "Privado", "Ninguno"], state="readonly", width=18)
        self.combo_pac_seguro.grid(row=5, column=1, sticky=tk.W, pady=8)
        self.combo_pac_seguro.current(0)

        datos_prueba = "Dato de prueba: DNI 11223344 | Luis Alberto Rojas Medina | 987654321"
        ttk.Label(f_paciente, text=datos_prueba, style="Status.TLabel").grid(row=6, column=1, columnspan=3, sticky=tk.W, pady=(8, 4))

        ttk.Button(f_paciente, text="Registrar paciente", style="Primary.TButton", command=self._registrar_paciente).grid(row=7, column=3, sticky=tk.E, pady=14)

    def _registrar_paciente(self):
        dni = self.txt_pac_dni.get().strip()
        nombres = self.txt_pac_nombres.get().strip()
        apellidos = self.txt_pac_apellidos.get().strip()
        telefono = self.txt_pac_telefono.get().strip()
        fecha = self.txt_pac_fecha.get().strip()
        sexo = self.combo_pac_sexo.get().strip()
        direccion = self.txt_pac_direccion.get().strip()
        seguro = self.combo_pac_seguro.get().strip()

        if not dni or not dni.isdigit() or len(dni) != 8:
            messagebox.showwarning("DNI no valido", "Ingrese un DNI numerico de 8 digitos.")
            return
        if not nombres:
            messagebox.showwarning("Nombres requeridos", "Ingrese los nombres del paciente.")
            return
        if not apellidos:
            messagebox.showwarning("Apellidos requeridos", "Ingrese los apellidos del paciente.")
            return
        if self.controller.existe_paciente_por_dni(dni):
            messagebox.showerror("DNI duplicado", "Ya existe un paciente registrado con ese DNI.")
            return

        exito, mensaje = self.controller.registrar_paciente(dni, nombres, apellidos, telefono, fecha, sexo, direccion, seguro)
        if exito:
            messagebox.showinfo("Paciente registrado", mensaje)
            self.txt_pac_dni.delete(0, tk.END)
            self.txt_pac_nombres.delete(0, tk.END)
            self.txt_pac_apellidos.delete(0, tk.END)
            self.txt_pac_telefono.delete(0, tk.END)
            self.txt_pac_direccion.delete(0, tk.END)
        else:
            messagebox.showerror("Error de registro", mensaje)

    def _buscar_paciente(self):
        dni = self.txt_buscar_dni.get().strip()
        if not dni:
            messagebox.showwarning("DNI requerido", "Escriba un numero de DNI para buscar el historial.")
            return

        paciente, atenciones = self.controller.buscar_historial_por_dni(dni)

        for item in self.tree.get_children():
            self.tree.delete(item)

        if paciente:
            self.paciente_actual = {
                "id_paciente": paciente[0],
                "dni": paciente[1],
                "nombre": f"{paciente[2]} {paciente[3]}",
                "seguro": paciente[4],
                "id_historia": paciente[5]
            }
            texto = f"Paciente: {self.paciente_actual['nombre']} | DNI: {self.paciente_actual['dni']} | Seguro: {self.paciente_actual['seguro']}"
            self.lbl_paciente_info.config(text=texto, foreground="#1b7f45")
            for at in atenciones:
                self.tree.insert("", tk.END, values=(at[1], at[2], at[3], at[4], at[5], at[6], at[7]))
        else:
            self.paciente_actual = None
            self.lbl_paciente_info.config(text="Paciente no encontrado en el sistema.", foreground="#b42318")

    def _guardar_atencion(self):
        if not self.paciente_actual:
            messagebox.showerror("Paciente requerido", "Primero busque y seleccione un paciente.")
            return

        motivo = self.txt_motivo.get("1.0", tk.END).strip()
        diagnostico = self.txt_diagnostico.get("1.0", tk.END).strip()
        tratamiento = self.txt_tratamiento.get("1.0", tk.END).strip()
        tipo_atencion = self.combo_tipo_atencion.get()

        if not motivo or not diagnostico:
            messagebox.showwarning("Datos incompletos", "Ingrese como minimo el motivo y el diagnostico.")
            return

        id_atencion = self.controller.registrar_atencion_completa(
            self.paciente_actual["id_historia"],
            self.medico["id"],
            self.medico["id_est"],
            motivo, diagnostico, tratamiento, tipo_atencion
        )

        if id_atencion:
            self.atencion_actual_id = id_atencion
            messagebox.showinfo("Atencion registrada", "La atencion fue guardada correctamente.")
            self._buscar_paciente()
            self.txt_motivo.delete("1.0", tk.END)
            self.txt_diagnostico.delete("1.0", tk.END)
            self.txt_tratamiento.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error de registro", "No se pudo guardar la atencion en la base de datos.")

    def _guardar_derivacion(self):
        idx = self.combo_destino.current()
        motivo_dev = self.txt_motivo_derivacion.get("1.0", tk.END).strip()
        dni = self.txt_dni_derivacion.get().strip()
        estado = self.combo_estado_derivacion.get().strip() or "Pendiente"

        if idx == -1 or not motivo_dev:
            messagebox.showwarning("Datos incompletos", "Seleccione el establecimiento destino e ingrese el motivo.")
            return

        id_est_destino = self.lista_est_destino[idx][0]

        if dni:
            if not dni.isdigit() or len(dni) != 8:
                messagebox.showwarning("DNI no valido", "Ingrese un DNI numerico de 8 digitos.")
                return
            exito, mensaje = self.controller.registrar_derivacion_por_dni(dni, id_est_destino, motivo_dev, self.medico["id"], estado)
            if exito:
                messagebox.showinfo("Derivacion registrada", mensaje)
                self.txt_motivo_derivacion.delete("1.0", tk.END)
                self.txt_dni_derivacion.delete(0, tk.END)
            else:
                messagebox.showerror("Error de derivacion", mensaje)
            return

        if not self.atencion_actual_id:
            messagebox.showerror("DNI requerido", "Ingrese el DNI del paciente o registre una atencion en esta sesion.")
            return

        exito = self.controller.registrar_derivacion(self.atencion_actual_id, id_est_destino, motivo_dev)
        if exito:
            messagebox.showinfo("Derivacion registrada", "La derivacion fue registrada correctamente.")
            self.txt_motivo_derivacion.delete("1.0", tk.END)
            self.atencion_actual_id = None
        else:
            messagebox.showerror("Error de derivacion", "No se pudo registrar la derivacion.")
