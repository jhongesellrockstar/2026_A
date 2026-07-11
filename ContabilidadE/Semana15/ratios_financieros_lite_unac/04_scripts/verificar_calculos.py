from decimal import Decimal, ROUND_HALF_UP

D = Decimal

def q(x):
    return D(x).quantize(D("0.01"), rounding=ROUND_HALF_UP)

checks = []

def add(name, got, expected):
    got = q(got)
    exp = D(expected)
    checks.append((name, got, exp, got == exp))

add("Razón corriente", D("480000") / D("300000"), "1.60")
add("Prueba ácida", (D("480000") - D("180000")) / D("300000"), "1.00")
add("Rotación CxC", D("1200000") / D("200000"), "6.00")
add("Periodo cobro", D("360") / D("6"), "60.00")
add("Rotación inventarios", D("900000") / D("150000"), "6.00")
add("Permanencia inventarios", D("360") / D("6"), "60.00")
add("Endeudamiento", D("900000") / D("2000000") * D("100"), "45.00")
add("Deuda-patrimonio", D("900000") / D("1100000"), "0.82")
add("Margen neto", D("135000") / D("1500000") * D("100"), "9.00")
add("ROA", D("135000") / D("1500000") * D("100"), "9.00")
add("ROE", D("135000") / D("900000") * D("100"), "15.00")
add("Integrador razón corriente", D("540000") / D("300000"), "1.80")
add("Integrador prueba ácida", (D("540000") - D("180000")) / D("300000"), "1.20")
add("Integrador endeudamiento", D("570000") / D("1200000") * D("100"), "47.50")
add("Integrador margen neto", D("126900") / D("1500000") * D("100"), "8.46")
add("Integrador ROA simple", D("126900") / D("1200000") * D("100"), "10.58")
add("Integrador ROE simple", D("126900") / D("630000") * D("100"), "20.14")

failed = False
for name, got, exp, ok in checks:
    print(f"{name}: calculado {got} | esperado {exp} | {'OK' if ok else 'ERROR'}")
    failed = failed or not ok

raise SystemExit(1 if failed else 0)
