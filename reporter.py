"""Generador de reportes en JSON y HTML."""
import json
import os
from datetime import datetime
from jinja2 import Template


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Auditoría - {{ titulo }}</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        .meta { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .meta strong { color: #2c3e50; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; background: white; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #3498db; color: white; }
        tr:hover { background: #f9f9f9; }
        .abierto { color: #27ae60; font-weight: bold; }
        .cerrado { color: #e74c3c; }
        .footer { margin-top: 40px; text-align: center; color: #7f8c8d; font-size: 0.9em; }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 3px; font-size: 0.85em; }
        .badge-info { background: #3498db; color: white; }
    </style>
</head>
<body>
    <h1>🛡️ {{ titulo }}</h1>
    <div class="meta">
        <p><strong>Fecha:</strong> {{ fecha }}</p>
        <p><strong>Objetivo:</strong> {{ objetivo }}</p>
        <p><strong>Tipo de auditoría:</strong> <span class="badge badge-info">{{ tipo }}</span></p>
    </div>

    <h2>📋 Resumen Ejecutivo</h2>
    <p>{{ resumen }}</p>

    <h2>🔍 Hallazgos Detallados</h2>
    <table>
        <thead>
            <tr><th>Elemento</th><th>Estado</th><th>Detalle</th></tr>
        </thead>
        <tbody>
            {% for item in hallazgos %}
            <tr>
                <td>{{ item.elemento }}</td>
                <td class="{{ 'abierto' if item.estado == 'ABIERTO' else 'cerrado' }}">{{ item.estado }}</td>
                <td>{{ item.detalle }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <h2>💡 Recomendaciones</h2>
    <ul>
        {% for rec in recomendaciones %}
        <li>{{ rec }}</li>
        {% endfor %}
    </ul>

    <div class="footer">
        <p>Generado por Ethical Hacking Toolkit v4.1 | Uso exclusivo para auditorías autorizadas</p>
    </div>
</body>
</html>
"""


class ReportGenerator:
    """Genera reportes profesionales de auditoría."""

    def __init__(self, reports_dir="reports"):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)

    def save_json(self, data, filename=None):
        """Guarda resultados en JSON."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.reports_dir, f"scan_{timestamp}.json")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        return filename

    def save_html(self, data, filename=None):
        """Genera reporte HTML profesional."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(
                self.reports_dir, f"audit_{timestamp}.html")

        template = Template(HTML_TEMPLATE)
        html = template.render(
            titulo=data.get("titulo", "Auditoría de Seguridad"),
            fecha=data.get("fecha", datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")),
            objetivo=data.get("objetivo", "N/A"),
            tipo=data.get("tipo", "General"),
            resumen=data.get("resumen", "Sin resumen disponible."),
            hallazgos=data.get("hallazgos", []),
            recomendaciones=data.get("recomendaciones", []),
        )

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)

        return filename

    def generar_reporte_escaneo(self, target, puertos_abiertos, total_escaneados):
        """Genera reporte estructurado de escaneo de puertos."""
        hallazgos = []
        for p in puertos_abiertos:
            hallazgos.append({
                "elemento": f"Puerto {p['puerto']}/tcp",
                "estado": "ABIERTO",
                "detalle": f"Servicio: {p.get('servicio', 'desconocido')}",
            })

        recomendaciones = [
            "Cerrar puertos innecesarios para reducir la superficie de ataque.",
            "Implementar firewall con reglas estrictas (allowlist).",
            "Monitorear tráfico en puertos abiertos con IDS/IPS.",
            "Mantener servicios actualizados a sus últimas versiones.",
        ]

        data = {
            "titulo": "Reporte de Escaneo de Puertos",
            "fecha": datetime.now().isoformat(),
            "objetivo": target,
            "tipo": "Escaneo TCP",
            "resumen": f"Se escanearon {total_escaneados} puertos. Se encontraron {len(puertos_abiertos)} puertos abiertos.",
            "hallazgos": hallazgos,
            "recomendaciones": recomendaciones,
            "datos_crudos": {
                "target": target,
                "puertos_abiertos": puertos_abiertos,
                "total_escaneados": total_escaneados,
            },
        }

        json_path = self.save_json(data)
        html_path = self.save_html(data)

        return {"json": json_path, "html": html_path}
