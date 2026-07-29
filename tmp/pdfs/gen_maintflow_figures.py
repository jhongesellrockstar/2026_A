from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(r"C:\xampp\htdocs\tw_maintflow_simple\documentacion_final\figuras")
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#15324A"
BLUE = "#2F80ED"
TEAL = "#18A999"
LIGHT = "#F4F8FB"
GOLD = "#F2B134"
RED = "#D95D5D"
GRAY = "#5D6B78"


def canvas(title, subtitle="TW MaintFlow · Programación Web I"):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.text(0.6, 8.5, title, fontsize=24, fontweight="bold", color=NAVY, va="center")
    ax.text(0.6, 8.1, subtitle, fontsize=10.5, color=GRAY, va="center")
    ax.plot([0.6, 15.4], [7.82, 7.82], color=TEAL, linewidth=3)
    ax.text(15.4, 0.28, "Universidad Nacional del Callao · 2026", fontsize=9,
            color=GRAY, ha="right")
    return fig, ax


def box(ax, x, y, w, h, text, color=BLUE, text_color="white", size=13, subtitle=None):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                       linewidth=1.6, edgecolor=color, facecolor=color)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2+(0.15 if subtitle else 0), text, ha="center", va="center",
            color=text_color, fontsize=size, fontweight="bold")
    if subtitle:
        ax.text(x+w/2, y+h/2-0.28, subtitle, ha="center", va="center",
                color=text_color, fontsize=9.5)


def light_box(ax, x, y, w, h, text, color=BLUE, size=11):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.1",
                       linewidth=1.5, edgecolor=color, facecolor=LIGHT)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", color=NAVY,
            fontsize=size, fontweight="semibold", wrap=True)


def arrow(ax, a, b, color=GRAY, label=None, curve=0):
    p = FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16, linewidth=1.8,
                        color=color, connectionstyle=f"arc3,rad={curve}")
    ax.add_patch(p)
    if label:
        mx, my = (a[0]+b[0])/2, (a[1]+b[1])/2
        ax.text(mx, my+0.18, label, fontsize=9.2, color=color, ha="center",
                bbox=dict(facecolor="white", edgecolor="none", pad=1.5))


def save(fig, name):
    fig.savefig(OUT/name, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# 1. Arquitectura MVC
fig, ax = canvas("Arquitectura MVC de TW MaintFlow")
box(ax, 0.9, 4.9, 2.8, 1.25, "Navegador", TEAL, subtitle="GET / POST")
box(ax, 4.4, 4.9, 3.0, 1.25, "index.php + rutas.php", NAVY, subtitle="Punto de entrada")
box(ax, 8.1, 5.8, 2.8, 1.15, "Controladores", BLUE, subtitle="Validación y flujo")
box(ax, 8.1, 3.8, 2.8, 1.15, "Modelos", GOLD, text_color=NAVY, subtitle="SQL preparado")
box(ax, 12.0, 5.8, 2.8, 1.15, "Vistas", TEAL, subtitle="HTML + CSS + JS")
box(ax, 12.0, 3.8, 2.8, 1.15, "MariaDB", NAVY, subtitle="bd_tw_maintflow")
arrow(ax, (3.7, 5.52), (4.4, 5.52), label="petición")
arrow(ax, (7.4, 5.52), (8.1, 6.35))
arrow(ax, (9.5, 5.8), (9.5, 4.95), label="consulta")
arrow(ax, (10.9, 6.35), (12.0, 6.35), label="carga")
arrow(ax, (10.9, 4.35), (12.0, 4.35), label="mysqli")
arrow(ax, (13.4, 5.8), (13.4, 4.95), color=TEAL, label="datos")
arrow(ax, (12.0, 6.1), (3.7, 5.9), color=TEAL, label="respuesta HTML", curve=-0.18)
light_box(ax, 4.3, 1.45, 7.4, 1.25,
          "Separación de responsabilidades: el controlador coordina, el modelo accede a datos y la vista presenta.", TEAL, 12)
save(fig, "01_arquitectura_mvc.png")

# 2. Flujo petición
fig, ax = canvas("Flujo de una petición MVC")
steps = [
    (0.7, "1", "Usuario\nselecciona opción"), (3.2, "2", "index.php\nlee controlador/acción"),
    (5.7, "3", "rutas.php\nvalida la ruta"), (8.2, "4", "Controlador\nvalida sesión y rol"),
    (10.7, "5", "Modelo\nejecuta SQL"), (13.2, "6", "Vista\nrenderiza HTML")]
for x, n, t in steps:
    ax.text(x+0.9, 6.75, n, ha="center", va="center", fontsize=13, fontweight="bold",
            color="white", bbox=dict(boxstyle="circle", facecolor=TEAL, edgecolor=TEAL))
    light_box(ax, x, 4.65, 1.8, 1.5, t, TEAL if n in ("1", "6") else BLUE, 9.2)
for i in range(len(steps)-1):
    arrow(ax, (steps[i][0]+1.8, 5.4), (steps[i+1][0], 5.4))
light_box(ax, 3.0, 2.1, 10.0, 1.3,
          "Si la ruta no existe: 404 · Si el rol no tiene permiso: 403 · Si todo es válido: respuesta 200", NAVY, 12)
save(fig, "02_flujo_peticion_mvc.png")

# 3. Modelo relacional
fig, ax = canvas("Modelo relacional simplificado", "bd_tw_maintflow · 12 tablas")
nodes = {
    "roles": (0.7,6.2), "usuarios": (3.0,6.2), "tecnicos": (5.4,6.2),
    "clientes": (0.7,3.9), "sedes": (3.0,3.9), "equipos": (5.4,3.9),
    "estados_orden": (8.0,6.2), "ordenes_servicio": (8.0,3.9),
    "detalle_orden": (11.1,3.9), "repuestos": (13.4,6.2),
    "movimientos_repuesto": (12.6,1.6), "categorias_equipo": (5.0,1.6)
}
sizes = {k:(2.0,0.9) for k in nodes}; sizes["ordenes_servicio"]=(2.5,0.9); sizes["movimientos_repuesto"]=(2.8,0.9); sizes["categorias_equipo"]=(2.6,0.9)
for name,(x,y) in nodes.items():
    w,h=sizes[name]; light_box(ax,x,y,w,h,name,TEAL if name in ("ordenes_servicio","detalle_orden") else BLUE,9.5)
def center(name):
    x,y=nodes[name]; w,h=sizes[name]; return (x+w/2,y+h/2)
for a,b in [("roles","usuarios"),("usuarios","tecnicos"),("clientes","sedes"),("sedes","equipos"),
            ("categorias_equipo","equipos"),("equipos","ordenes_servicio"),("tecnicos","ordenes_servicio"),
            ("estados_orden","ordenes_servicio"),("ordenes_servicio","detalle_orden"),("repuestos","detalle_orden"),
            ("repuestos","movimientos_repuesto"),("usuarios","movimientos_repuesto")]:
    arrow(ax, center(a), center(b), color=GRAY)
ax.text(8.0,0.55,"Las flechas representan claves foráneas hacia registros relacionados.",fontsize=10.5,color=GRAY,ha="center")
save(fig, "03_modelo_relacional.png")

# 4. Login
fig, ax = canvas("Flujo de autenticación y sesión")
items=[("Formulario\nusuario + contraseña",0.7,5.0,TEAL),("AuthController::login",4.1,5.0,BLUE),
       ("Usuario::validar\npassword_verify",7.5,5.0,GOLD),("session_regenerate_id\n(true)",10.9,5.0,NAVY),
       ("Dashboard según rol",13.2,5.0,TEAL)]
for textv,x,y,c in items: box(ax,x,y,2.4 if x<13 else 2.2,1.3,textv,c,text_color=NAVY if c==GOLD else "white",size=11)
for i in range(len(items)-1):
    x=items[i][1]; w=2.4 if x<13 else 2.2; arrow(ax,(x+w,5.65),(items[i+1][1],5.65))
light_box(ax,4.0,2.1,3.4,1.1,"Credencial inválida\nmensaje de error",RED,11)
arrow(ax,(8.7,5.0),(5.7,3.2),RED,"no coincide",0.1)
light_box(ax,9.0,2.1,4.0,1.1,"logout() destruye la sesión\ny vuelve al acceso",NAVY,11)
save(fig, "04_flujo_login.png")

# 5. Orden
fig, ax = canvas("Flujo de una orden de servicio")
labels=[("Recepción crea\nla solicitud",0.6,5.0,TEAL),("Selecciona equipo,\nprioridad y tipo",3.5,5.0,BLUE),
        ("Asigna técnico",6.4,5.0,NAVY),("Técnico registra\ndiagnóstico",9.3,5.0,GOLD),
        ("Solución, actividades\ny repuestos",12.2,5.0,BLUE)]
for txt,x,y,c in labels: box(ax,x,y,2.3,1.35,txt,c,text_color=NAVY if c==GOLD else "white",size=10.5)
for i in range(len(labels)-1): arrow(ax,(labels[i][1]+2.3,5.67),(labels[i+1][1],5.67))
box(ax,6.0,2.0,4.0,1.25,"Cierre de orden",TEAL,subtitle="estado + fecha_cierre")
arrow(ax,(13.35,5.0),(10.0,3.25),TEAL,"finaliza",0.12)
light_box(ax,10.8,1.65,4.3,1.55,"Trigger descuenta stock\ny recalcula costo total\nal agregar un repuesto.",RED,10.2)
save(fig, "05_flujo_orden.png")

# 6. trigger
fig, ax = canvas("Flujo del trigger tr_detalle_stock")
box(ax,0.8,5.0,3.1,1.4,"INSERT en detalle_orden",BLUE,subtitle="actividad con repuesto")
light_box(ax,4.6,5.0,3.0,1.4,"¿id_repuesto no es NULL\ny cantidad > 0?",GOLD,11)
box(ax,8.4,5.0,3.0,1.4,"UPDATE repuestos",RED,subtitle="stock - cantidad")
box(ax,12.2,5.0,3.0,1.4,"UPDATE orden",TEAL,subtitle="recalcula costo_total")
arrow(ax,(3.9,5.7),(4.6,5.7)); arrow(ax,(7.6,5.7),(8.4,5.7),TEAL,"sí"); arrow(ax,(11.4,5.7),(12.2,5.7))
light_box(ax,4.9,2.2,2.4,1.1,"No modifica stock",GRAY,11)
arrow(ax,(6.1,5.0),(6.1,3.3),GRAY,"no")
light_box(ax,8.0,1.35,7.0,1.8,"Momento: AFTER INSERT · Tabla: detalle_orden\nUtilidad: consistencia automática del inventario",NAVY,11.0)
save(fig, "06_trigger_stock.png")

# 7. roles
fig, ax = canvas("Matriz de roles y permisos")
cols=["Clientes / sedes / equipos","Órdenes","Técnicos / repuestos","Usuarios / reportes"]
rows=[("Administrador",["CRUD","Todas","CRUD","Gestiona"]),("Recepción",["CRUD","Crea y asigna","Sin acceso","Sin acceso"]),("Técnico",["Sin acceso","Solo asignadas","Usa repuestos en orden","Sin acceso"])]
x0=4.1; colw=2.75
for j,c in enumerate(cols): box(ax,x0+j*colw,6.45,colw-0.12,0.95,c,NAVY,size=9.3)
for i,(role,vals) in enumerate(rows):
    y=5.05-i*1.45; box(ax,0.8,y,3.0,1.0,role,TEAL if i==0 else BLUE,size=12)
    for j,v in enumerate(vals):
        color=TEAL if v in ("CRUD","Todas","Gestiona","Crea y asigna","Solo asignadas","Usa repuestos en orden") else RED
        light_box(ax,x0+j*colw,y,colw-0.12,1.0,v,color,9.5)
light_box(ax,3.2,0.75,9.6,1.0,"exigir_roles() aplica la restricción y muestra error 403 cuando corresponde.",NAVY,11.5)
save(fig, "07_roles_permisos.png")

print(f"Figuras creadas en {OUT}")
