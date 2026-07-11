from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT=Path(r'C:\xampp\htdocs\tw_maintflow\documentacion_defensa\figuras')
OUT.mkdir(parents=True,exist_ok=True)
try: F=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',25); B=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',28); S=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
except: F=B=S=ImageFont.load_default()
BG='#f4f7f9'; NAVY='#08243a'; CYAN='#12a89e'; BLUE='#dcecf3'; INK='#16242e'; ORANGE='#f28c45'
def box(d,xy,text,fill=BLUE):
 d.rounded_rectangle(xy,18,fill=fill,outline=NAVY,width=2); x1,y1,x2,y2=xy
 lines=text.split('\n'); h=sum(d.textbbox((0,0),t,font=F)[3] for t in lines)+8*(len(lines)-1); y=(y1+y2-h)/2
 for t in lines:
  bb=d.textbbox((0,0),t,font=F); d.text(((x1+x2-bb[2])/2,y),t,font=F,fill=INK); y+=bb[3]+8
def arrow(d,a,b): d.line([a,b],fill=CYAN,width=5); x,y=b; d.polygon([(x,y),(x-14,y-9),(x-14,y+9)],fill=CYAN)
def canvas(title):
 im=Image.new('RGB',(1600,900),BG);d=ImageDraw.Draw(im);d.rectangle((0,0,1600,85),fill=NAVY);d.text((45,22),title,font=B,fill='white');return im,d
def linear(name,title,labels):
 im,d=canvas(title); n=len(labels); w=min(250,(1450-(n-1)*45)//n); total=n*w+(n-1)*45; x=(1600-total)//2
 for i,l in enumerate(labels):
  box(d,(x,340,x+w,540),l,'#ffffff' if i%2==0 else BLUE)
  if i<n-1: arrow(d,(x+w,440),(x+w+40,440))
  x+=w+45
 d.text((45,835),'TW MaintFlow - Programación Web I - UNAC 2026-A',font=S,fill=NAVY);im.save(OUT/name)
linear('01_arquitectura_general.png','Arquitectura general',['Navegador','Apache\npublic/index.php','Router y\ncontroladores','Modelos\nPDO','MariaDB'])
linear('02_flujo_mvc.png','Flujo MVC',['Ruta /clientes','Router','ClienteController\nindex()','CrudModel\nall()','Vista HTML'])
linear('03_componentes_mvc.png','Componentes MVC',['Vista\nHTML/CSS','Controlador\nvalidación y flujo','Modelo\nconsultas PDO'])
linear('05_flujo_login.png','Flujo de autenticación',['Formulario','AuthController','Usuario\nauthenticate()','password_verify','Sesión y rol'])
linear('06_flujo_orden_servicio.png','Ciclo de una orden',['Pendiente','Asignada','En proceso','En espera','Cerrada'])
linear('08_trigger_stock.png','Trigger de stock',['INSERT\ndetalle_orden','tr_detalle_stock','UPDATE\nrepuestos','Recalcular\ncosto total'])
im,d=canvas('Modelo entidad-relación simplificado')
nodes={'roles':(70,150),'usuarios':(360,150),'técnicos':(650,150),'órdenes':(940,150),'detalle':(1230,150),'clientes':(70,520),'sedes':(360,520),'equipos':(650,520),'repuestos':(1230,520),'estados':(940,520)}
for k,(x,y) in nodes.items():box(d,(x,y,x+220,y+120),k)
edges=[('roles','usuarios'),('usuarios','técnicos'),('técnicos','órdenes'),('órdenes','detalle'),('clientes','sedes'),('sedes','equipos'),('equipos','órdenes'),('estados','órdenes'),('repuestos','detalle')]
for a,b in edges:
 x1,y1=nodes[a];x2,y2=nodes[b];arrow(d,(x1+220,y1+60),(x2-8,y2+60))
im.save(OUT/'04_modelo_relacional.png')
im,d=canvas('Matriz de roles y permisos'); cols=['Módulo','Administrador','Recepción','Técnico'];rows=[('Clientes','CRUD','CRUD','Consulta'),('Equipos','CRUD','CRUD','Consulta'),('Órdenes','Total','Crear/consultar','Actualizar'),('Usuarios','Sí','No','No'),('Reportes','Sí','No','No')]
x=[80,520,850,1180]; y=150
for i,c in enumerate(cols): box(d,(x[i],y,x[i]+300,y+90),c,CYAN if i else ORANGE)
for r,row in enumerate(rows):
 for i,c in enumerate(row): box(d,(x[i],270+r*105,x[i]+300,350+r*105),c,'#ffffff')
im.save(OUT/'07_roles_permisos.png')
