from flask import Flask, jsonify, request
from data import products

app = Flask(__name__)

# Homepage: welcome message for the catalog API
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Product Catalog API"}), 200


# GET /products: return all products, or filter with ?category=
@app.route("/products", methods=["GET"])
def get_products():
    category = request.args.get("category")
    if category:
        # Normalize query and stored category so filtering is case-insensitive
        filtered = [
            product
            for product in products
            if product["category"].lower() == category.lower()
        ]
        return jsonify(filtered), 200
    return jsonify(products), 200


# GET /products/<id>: return one product, or 404 if the ID does not exist
@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    product = next((item for item in products if item["id"] == id), None)
    if product is None:
        return jsonify({"error": f"Product with id {id} not found"}), 404
    return jsonify(product), 200


if __name__ == "__main__":
    app.run(debug=True)
