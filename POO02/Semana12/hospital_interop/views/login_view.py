import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from controllers import HospitalController
from views import DashboardView

class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Acceso medico - Sistema de Interoperabilidad Hospitalaria")
        self.geometry("620x500")
        self.minsize(620, 500)
        self.resizable(False, False)

        self.controller = HospitalController()
        self.lista_est = []
        self.logo_img = None

        self._configurar_estilos()
        self._crear_componentes()

    def _ruta_recurso(self, ruta_relativa):
        if hasattr(sys, "_MEIPASS"):
            base = sys._MEIPASS
        else:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return os.path.join(base, ruta_relativa)

    def _cargar_logo(self, ancho_aproximado=120):
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
        self.style.configure("Card.TFrame", background="#ffffff", relief="flat")
        self.style.configure("Title.TLabel", background="#ffffff", foreground="#183b56", font=("Segoe UI", 18, "bold"))
        self.style.configure("Subtitle.TLabel", background="#ffffff", foreground="#3f5f7a", font=("Segoe UI", 11))
        self.style.configure("Field.TLabel", background="#ffffff", foreground="#1f2d3d", font=("Segoe UI", 10, "bold"))
        self.style.configure("Note.TLabel", background="#ffffff", foreground="#637381", font=("Segoe UI", 9))
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=8, background="#0f5f9f", foreground="#ffffff")
        self.style.map("Primary.TButton", background=[("active", "#0b5cad")], foreground=[("active", "#ffffff")])
        self.style.configure("TCombobox", padding=5)
        self.style.configure("TEntry", padding=5)

    def _crear_componentes(self):
        contenedor = ttk.Frame(self, style="Main.TFrame", padding=30)
        contenedor.pack(fill=tk.BOTH, expand=True)

        tarjeta = ttk.Frame(contenedor, style="Card.TFrame", padding=28)
        tarjeta.pack(fill=tk.BOTH, expand=True)

        barra = tk.Frame(tarjeta, bg="#0f5f9f", height=8)
        barra.pack(fill=tk.X, side=tk.TOP)

        self.logo_img = self._cargar_logo(120)
        if self.logo_img:
            ttk.Label(tarjeta, image=self.logo_img, background="#ffffff").pack(anchor=tk.W, pady=(18, 0))

        ttk.Label(tarjeta, text="Sistema de Interoperabilidad Hospitalaria", style="Title.TLabel").pack(anchor=tk.W, pady=(22, 4))
        ttk.Label(tarjeta, text="Acceso medico", style="Subtitle.TLabel").pack(anchor=tk.W, pady=(0, 22))

        formulario = ttk.Frame(tarjeta, style="Card.TFrame")
        formulario.pack(fill=tk.X)

        ttk.Label(formulario, text="Establecimiento", style="Field.TLabel").pack(anchor=tk.W, pady=(0, 4))
        self.combo_est = ttk.Combobox(formulario, state="readonly", height=8)
        self.combo_est.pack(fill=tk.X, pady=(0, 16))
        self._cargar_establecimientos()

        ttk.Label(formulario, text="CMP del medico", style="Field.TLabel").pack(anchor=tk.W, pady=(0, 4))
        self.txt_cmp = ttk.Entry(formulario)
        self.txt_cmp.pack(fill=tk.X, pady=(0, 18))

        btn_ingresar = ttk.Button(formulario, text="Iniciar sesion", style="Primary.TButton", command=self._procesar_login)
        btn_ingresar.pack(fill=tk.X, pady=(0, 16))

        ttk.Separator(tarjeta).pack(fill=tk.X, pady=10)

        nota = "CMP = Codigo del Colegio Medico del Peru."
        ttk.Label(tarjeta, text=nota, style="Note.TLabel").pack(anchor=tk.W)

        prueba = "Datos de prueba: Hospital Academico Lima Callao | CMP: 123456"
        ttk.Label(tarjeta, text=prueba, style="Note.TLabel").pack(anchor=tk.W, pady=(4, 0))

    def _cargar_establecimientos(self):
        self.lista_est = self.controller.obtener_establecimientos()
        self.combo_est["values"] = [est[1] for est in self.lista_est]

    def _procesar_login(self):
        idx = self.combo_est.current()
        cmp = self.txt_cmp.get().strip()

        if idx == -1 or not cmp:
            messagebox.showwarning("Campos incompletos", "Seleccione un establecimiento e ingrese el CMP.")
            return

        id_establecimiento = self.lista_est[idx][0]
        nombre_est = self.lista_est[idx][1]

        medico_data = self.controller.verificar_login_medico(cmp, id_establecimiento)

        if medico_data:
            medico_info = {
                "id": medico_data[0],
                "nombre": f"{medico_data[1]} {medico_data[2]}",
                "id_est": id_establecimiento,
                "nombre_est": nombre_est
            }
            self.destroy()
            app_dashboard = DashboardView(medico_info)
            app_dashboard.mainloop()
        else:
            messagebox.showerror("Credenciales no validas", "No se encontro un medico con ese CMP en el establecimiento seleccionado.")
