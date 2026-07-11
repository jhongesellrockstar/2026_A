from pathlib import Path
try:
    import matplotlib.pyplot as plt
except Exception as exc:
    print(f"Matplotlib no disponible: {exc}")
    raise SystemExit(0)

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "10_salida" / "graficos"
out.mkdir(parents=True, exist_ok=True)

labels = ["Razón corriente", "Prueba ácida", "Endeudamiento", "Margen neto", "ROE"]
values = [1.80, 1.20, 47.50, 8.46, 20.14]
colors = ["#4FC3F7", "#4FC3F7", "#F59E0B", "#8B5CF6", "#1E3A8A"]
plt.figure(figsize=(9, 4.5))
plt.bar(labels, values, color=colors)
plt.xticks(rotation=20, ha="right")
plt.title("Indicadores del caso integrador")
plt.tight_layout()
plt.savefig(out / "ratios_integrador.png", dpi=180)
print(out / "ratios_integrador.png")
