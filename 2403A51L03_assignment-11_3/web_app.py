from flask import Flask, jsonify, request, render_template

from contact_manager import ArrayContactManager, LinkedListContactManager

app = Flask(__name__)

# Create one instance of each implementation for the lifetime of the app
array_manager = ArrayContactManager()
linked_manager = LinkedListContactManager()


def get_manager(implementation: str):
    """
    Helper to choose the correct contact manager based on a string key.
    Defaults to array-based if an unknown key is provided.
    """
    implementation = (implementation or "").lower()
    if implementation == "linked":
        return linked_manager
    return array_manager


@app.route("/")
def index():
    """
    Render the main single-page app.
    """
    return render_template("index.html")


@app.route("/api/contacts", methods=["GET"])
def list_contacts():
    """
    List all contacts for the chosen implementation.
    Query parameter:
        implementation: "array" or "linked" (default: "array")
    """
    implementation = request.args.get("implementation", "array")
    manager = get_manager(implementation)
    contacts = manager.get_all_contacts()
    return jsonify({"implementation": implementation, "contacts": contacts})


@app.route("/api/contacts", methods=["POST"])
def add_or_update_contact():
    """
    Add a new contact or update an existing one.
    JSON body:
        {
          "implementation": "array" | "linked",
          "name": "...",
          "phone": "..."
        }
    """
    data = request.get_json(force=True) or {}
    implementation = data.get("implementation", "array")
    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()

    if not name or not phone:
        return jsonify({"error": "Both name and phone are required."}), 400

    manager = get_manager(implementation)
    manager.add_contact(name, phone)
    return jsonify({"message": "Contact added/updated successfully."}), 201


@app.route("/api/contacts/<string:name>", methods=["GET"])
def get_contact(name: str):
    """
    Search for a contact by name.
    Query parameter:
        implementation: "array" or "linked" (default: "array")
    """
    implementation = request.args.get("implementation", "array")
    manager = get_manager(implementation)
    contact = manager.search_contact(name)

    if contact is None:
        return jsonify({"error": "Contact not found."}), 404

    return jsonify({"name": contact.name, "phone": contact.phone})


@app.route("/api/contacts/<string:name>", methods=["DELETE"])
def delete_contact(name: str):
    """
    Delete a contact by name.
    Query parameter:
        implementation: "array" or "linked" (default: "array")
    """
    implementation = request.args.get("implementation", "array")
    manager = get_manager(implementation)
    deleted = manager.delete_contact(name)

    if not deleted:
        return jsonify({"error": "Contact not found."}), 404

    return jsonify({"message": "Contact deleted successfully."})


if __name__ == "__main__":
    # Run in debug mode for development; you can change host/port as needed.
    app.run(debug=True)

