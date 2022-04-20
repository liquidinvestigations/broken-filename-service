import base64
import logging
from pathlib import Path
from flask import Flask, abort, send_file, request

log = logging.getLogger(__name__)

app = Flask(__name__)

MAX_REQUEST_SIZE = 100 * 1024  # 100 KB
DATA_PATH = Path('/data')


@app.route('/get-object', methods=['POST'])
def get_object():
    cl = request.content_length
    if cl is not None and cl > MAX_REQUEST_SIZE:
        log.error('req size too large!')
        abort(413)
    base64_path = request.get_json()['path_base64']
    filepath = base64.b64decode(base64_path).decode('utf8', errors="surrogateescape")
    return send_file(DATA_PATH / filepath)


@app.route('/health', methods=['GET'])
def health():
    log.info('GET /config 200')
    return {'status': 'ok'}, 200


if __name__ == "__main__":
    app.run()
