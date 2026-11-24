"""Fake 'remote' C2 listener — prints whatever the keylogger sends."""
import socket

HOST, PORT = "127.0.0.1", 9009

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[listener] listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        data = conn.recv(4096)
        print(f"[{addr}] {data!r}")
        conn.close()