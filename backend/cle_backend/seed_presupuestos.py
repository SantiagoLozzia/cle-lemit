from database.models import Presupuesto, DetallePresupuesto, Solicitante, Servicio, Modulo
from datetime import date

modulo = Modulo.obtener_ultimo_modulo().valor
solicitantes = list(Solicitante.objects.all())
servicios = list(Servicio.objects.filter(arancel__gt=0))

def get_srv(nro, fallback_index):
    s = next((x for x in servicios if x.nro_servicio == nro), None)
    return s if s else servicios[fallback_index % len(servicios)]

presupuestos_data = [
    {"fecha": date(2025, 3, 10), "contacto": "Ing. Martínez", "area": "hormigones", "desc": 0, "estado": "aceptado", "obs": "Ensayos para obra vial RN 3", "items": [(10,3),(15,5),(22,2)]},
    {"fecha": date(2025, 4, 2),  "contacto": "Lic. Fernández", "area": "geologia", "desc": 5, "estado": "en_espera", "obs": "Estudio de suelo para licitación pública", "items": [(50,1),(55,2)]},
    {"fecha": date(2025, 5, 15), "contacto": "Arq. Gómez", "area": "patrimonio", "desc": 10, "estado": "aceptado", "obs": None, "items": [(100,4),(105,2),(110,1)]},
    {"fecha": date(2025, 6, 8),  "contacto": "Dr. Suárez", "area": "quimica", "desc": 0, "estado": "rechazado", "obs": "Presupuesto rechazado por costos elevados", "items": [(200,6),(205,3)]},
    {"fecha": date(2025, 7, 22), "contacto": "Ing. Rodríguez", "area": "metalurgia", "desc": 15, "estado": "aceptado", "obs": "Ensayos tracción y dureza serie A", "items": [(150,10),(155,5)]},
    {"fecha": date(2025, 8, 5),  "contacto": "Téc. López", "area": "tecnologia_vial", "desc": 0, "estado": "en_espera", "obs": "Carpetas asfálticas - Autopista Ezeiza", "items": [(70,2),(75,3),(80,1)]},
    {"fecha": date(2025, 9, 18), "contacto": "Ing. Peralta", "area": "ensayos_mecanicos", "desc": 5, "estado": "aceptado", "obs": None, "items": [(30,8),(35,4)]},
    {"fecha": date(2025, 10, 1), "contacto": "Lic. Torres", "area": "durabilidad", "desc": 20, "estado": "en_espera", "obs": "Campaña de durabilidad - hormigón portuario", "items": [(180,12),(185,6),(190,3)]},
    {"fecha": date(2025, 10, 10),"contacto": "Dr. Vega", "area": "estudios_especiales", "desc": 0, "estado": "aceptado", "obs": "Análisis especiales solicitados por IRAM", "items": [(250,2),(255,2)]},
    {"fecha": date(2025, 10, 15),"contacto": "Ing. Castillo", "area": "servicios_tecnologicos", "desc": 10, "estado": "en_espera", "obs": "Capacitación y ensayos combinados", "items": [(300,1),(305,3),(310,2)]},
]

for i, d in enumerate(presupuestos_data):
    sol = solicitantes[i % len(solicitantes)]
    items = [(get_srv(nro, i+j), cant) for j, (nro, cant) in enumerate(d["items"])]
    subtotal = sum(s.arancel * modulo * c for s, c in items)
    total = subtotal * (1 - d["desc"] / 100)
    p = Presupuesto.objects.create(
        fecha_presupuesto=d["fecha"],
        contacto=d["contacto"],
        area_tematica=d["area"],
        descuento=d["desc"],
        subtotal=subtotal,
        arancel_presupuesto=total,
        estado_presupuesto=d["estado"],
        observaciones=d["obs"],
        nro_solicitante=sol,
    )
    for s, c in items:
        DetallePresupuesto.objects.create(nro_presupuesto=p, nro_servicio=s, cant=c, subtotal=s.arancel * modulo * c)
    print(f"✓ #{p.nro_presupuesto} {sol.nombre_solicitante} | {d['area']} | ${total:,.0f}")

print("\nListo!")
