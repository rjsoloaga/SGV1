# webhook_listener.py

from flask import Flask, request, jsonify
import logging
from models.venta import actualizar_estado_venta
import json


app = Flask(__name__)


@app.route("/webhook-mp", methods=["POST"])
def webhook_mp():
    data = request.json
    print("✅ Notificación recibida:", json.dumps(data, indent=2))

    try:
        event_type = data.get("type")
        if event_type == "payment":
            payment_data = data.get("data", {}).get("object", {})
            venta_id = payment_data.get("external_reference")

            if not venta_id:
                print("❌ No se encontró venta asociada")
                return jsonify({"status": "no_venta_id"}), 400

            status_pago = payment_data.get("status")
            print(f"💰 Venta #{venta_id} - Estado del pago: {status_pago}")

            if status_pago == "approved":
                actualizar_estado_venta(venta_id, "pagado", "Mercado Pago")
            elif status_pago in ["pending", "in_process"]:
                actualizar_estado_venta(venta_id, "pendiente", "Mercado Pago")
            elif status_pago in ["rejected", "cancelled"]:
                actualizar_estado_venta(venta_id, "rechazado", "Mercado Pago")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"❌ Error al procesar webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


def iniciar_webhook_server():
    """Función que puedes usar desde otro archivo"""
    app.run(port=5000)


if __name__ == "__main__":
    iniciar_webhook_server()