import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "incidents.db"

VALID_PRIORITIES = ["Low", "Medium", "High", "Critical"]
VALID_STATUSES = ["New", "In Progress", "Resolved", "Closed"]
UPDATABLE_FIELDS = ["title", "description", "priority", "status"]


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Low',
            status TEXT DEFAULT 'New',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def choice_error(field, value, allowed):
    if value not in allowed:
        return field + " must be one of: " + ", ".join(allowed)
    return None


@app.route("/incidents", methods=["POST"])
def create_incident():
    data = request.get_json()
    if not data or not str(data.get("title", "")).strip():
        return jsonify({"error": "title is required"}), 400

    priority = data.get("priority", "Low")
    error = choice_error("priority", priority, VALID_PRIORITIES)
    if error:
        return jsonify({"error": error}), 400

    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO incidents (title, description, priority) VALUES (?, ?, ?)",
        (data["title"].strip(), data.get("description", ""), priority),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": new_id, "message": "Incident created"}), 201


@app.route("/incidents", methods=["GET"])
def list_incidents():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM incidents").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/incidents/<int:incident_id>", methods=["GET"])
def get_incident(incident_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM incidents WHERE id = ?", (incident_id,)
    ).fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify(dict(row))


@app.route("/incidents/<int:incident_id>", methods=["PATCH"])
def update_incident(incident_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data sent"}), 400

    updates = {field: data[field] for field in UPDATABLE_FIELDS if field in data}
    if not updates:
        return jsonify({"error": "Nothing to update"}), 400

    if "title" in updates and not str(updates["title"]).strip():
        return jsonify({"error": "title cannot be empty"}), 400
    if "priority" in updates:
        error = choice_error("priority", updates["priority"], VALID_PRIORITIES)
        if error:
            return jsonify({"error": error}), 400
    if "status" in updates:
        error = choice_error("status", updates["status"], VALID_STATUSES)
        if error:
            return jsonify({"error": error}), 400

    set_clause = ", ".join(field + " = ?" for field in updates)
    values = list(updates.values()) + [incident_id]

    conn = get_connection()
    cursor = conn.execute(
        "UPDATE incidents SET " + set_clause + " WHERE id = ?", values
    )
    conn.commit()
    changed = cursor.rowcount
    conn.close()

    if changed == 0:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify({"message": "Incident updated"})


@app.route("/incidents/<int:incident_id>", methods=["DELETE"])
def delete_incident(incident_id):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify({"message": "Incident deleted"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)