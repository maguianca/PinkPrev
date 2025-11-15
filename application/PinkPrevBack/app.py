from flask import Flask, request, jsonify
from flask_cors import CORS
from matplotlib import pyplot as plt
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)


@app.route('/api/mamogram', methods=['POST'])
def test_mamogram():
    file = request.files.get('file')
    side = request.form.get('side')
    view = request.form.get('view')

    if not file or not side or not view:
        return jsonify({"error": "Missing data"}), 400

    return jsonify({
        "message": "Mamogram received",
        "side": side,
        "view": view
    }), 200


if __name__ == '__main__':
    app.run()
