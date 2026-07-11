from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = Decimal

def q(value):
    return D(value).quantize(D("0.01"), rounding=ROUND_HALF_UP)

checks = []
def add(name, got, expected):
    got = q(got)
    expected = D(expected)
    checks.append((name, got, expected, got == expected))

add("Razón corriente", D("480000") / D("300000"), "1.60")
add("Prueba ácida", (D("480000") - D("180000")) / D("300000"), "1.00")
prom_cxc = (D("180000") + D("220000")) / D("2")
add("Promedio CxC", prom_cxc, "200000.00")
add("Rotación CxC", D("1200000") / prom_cxc, "6.00")
add("Periodo promedio de cobro", D("360") / D("6"), "60.00")
prom_inv = (D("140000") + D("160000")) / D("2")
add("Promedio inventario", prom_inv, "150000.00")
add("Rotación inventarios", D("900000") / prom_inv, "6.00")
add("Permanencia inventario", D("360") / D("6"), "60.00")
add("Endeudamiento", D("900000") / D("2000000") * D("100"), "45.00")
add("Deuda-patrimonio", D("900000") / D("1100000"), "0.82")
add("Margen neto", D("135000") / D("1500000") * D("100"), "9.00")
add("ROA", D("135000") / D("1500000") * D("100"), "9.00")
add("ROE", D("135000") / D("900000") * D("100"), "15.00")

activo_corriente = D("120000") + D("240000") + D("180000")
total_activo = activo_corriente + D("660000")
pasivo_total = D("300000") + D("270000")
total_py_p = pasivo_total + D("630000")
add("Integrador activo corriente", activo_corriente, "540000.00")
add("Integrador total activo", total_activo, "1200000.00")
add("Integrador pasivo total", pasivo_total, "570000.00")
add("Igualdad contable", total_py_p - total_activo, "0.00")
add("Integrador utilidad bruta", D("1500000") - D("975000"), "525000.00")
add("Integrador utilidad operativa", D("525000") - D("300000"), "225000.00")
add("Integrador UAI", D("225000") - D("45000"), "180000.00")
add("Integrador utilidad neta", D("180000") - D("53100"), "126900.00")
add("Integrador razón corriente", D("540000") / D("300000"), "1.80")
add("Integrador prueba ácida", (D("540000") - D("180000")) / D("300000"), "1.20")
add("Integrador endeudamiento", D("570000") / D("1200000") * D("100"), "47.50")
add("Integrador deuda-patrimonio", D("570000") / D("630000"), "0.90")
add("Integrador margen neto", D("126900") / D("1500000") * D("100"), "8.46")
add("Integrador ROA simple", D("126900") / D("1200000") * D("100"), "10.58")
add("Integrador ROE simple", D("126900") / D("630000") * D("100"), "20.14")

lines = ["VALIDACIÓN DE CÁLCULOS", ""]
failed = False
for name, got, expected, ok in checks:
    lines.append(f"{name}: calculado {got} | esperado {expected} | {'OK' if ok else 'ERROR'}")
    failed = failed or not ok

out = ROOT / "04_casos_practicos" / "VALIDACION_CALCULOS.txt"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(out.read_text(encoding="utf-8"))
raise SystemExit(1 if failed else 0)
