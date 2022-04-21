import base64
import logging
from pathlib import Path
from flask import Flask, abort, send_file, request

log = logging.getLogger(__name__)

app = Flask(__name__)

MAX_REQUEST_SIZE = 100 * 1024  # 100 KB
DATA_PATH = Path('/data')


@app.route('/get-list', methods=['POST'])
def get_list():
    cl = request.content_length
    if cl is not None and cl > MAX_REQUEST_SIZE:
        log.error('req size too large!')
        abort(413)
    base64_path = request.get_json()['path_base64']
    dirpath = base64.b64decode(base64_path).decode('utf8', errors="surrogateescape")

    return {'list': [
        {
            'is_dir': d.is_dir(),
            'name_bytes': base64.b64encode(
                d.name.encode('utf8', errors='surrogateescape'),
            ).decode(),
        }
        for d in (DATA_PATH / dirpath).iterdir()
    ]}, 200


@app.route('/get-stat', methods=['POST'])
def get_stat():
    cl = request.content_length
    if cl is not None and cl > MAX_REQUEST_SIZE:
        log.error('req size too large!')
        abort(413)
    base64_path = request.get_json()['path_base64']
    filepath = base64.b64decode(base64_path).decode('utf8', errors="surrogateescape")
    stat = (DATA_PATH / filepath).stat()
    return {
        'size': stat.st_size,
        'ctime': stat.st_ctime,
        'mtime': stat.st_mtime,
    }, 200


@app.route('/get-object', methods=['POST'])
def get_object():
    cl = request.content_length
    if cl is not None and cl > MAX_REQUEST_SIZE:
        log.error('req size too large!')
        abort(413)
    base64_path = request.get_json()['path_base64']
    filepath = base64.b64decode(base64_path).decode('utf8', errors="surrogateescape")
    filepath = DATA_PATH / filepath

    # generate etag
    stat = filepath.stat()
    mtime = int(stat.st_mtime)
    size = int(stat.st_size)
    base64_hash = hash(base64_path)
    etag = f'{mtime}-{size}-{base64_hash}'
    return send_file(filepath,
                     mimetype='application/octet-stream',
                     download_name='object',
                     etag=etag)


@app.route('/health', methods=['GET'])
def health():
    log.info('GET /config 200')
    return {'status': 'ok'}, 200


if __name__ == "__main__":
    app.run()
