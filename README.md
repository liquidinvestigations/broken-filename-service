# File reader HTTP service for non-UTF8, non-ASCII, binary encoded filenames

Minio is great! But it doesn't accept objects with non-UTF8 filenames. More
importantly, if objects with non-UTF8 filenames already exist, they cannot be
downloaded from the service (but they can be listed).

This service is used to overcome that limitation; in case one encounters a
non-UTF8 filename, they can encode the binary path as `base64` and send it to:

    curl -X POST http://localhost:5000/get-object \
     -H 'Content-Type: application/json' \
     -d '{"path_base64":"aaaaZZZ"}'


The file outputs will be returned.


## Routes

- `POST /get-object` -- Download object with base64-encoded filename.
- `POST /get-stat`   -- Run os.stat() on the object with base64-encoded filename. Returns dict with "size", "ctime", "mtime".
- `GET  /health`     -- Returns `{"status": "ok"}`.
