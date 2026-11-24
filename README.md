# CMPT280-project

This is a keylogger that:
  1) Logs keystrokes to a hidden file (/tmp/.sys_update_cache/keys.log).
  2) Simulates exfiltration by sending each key to a localhost listener
     (127.0.0.1:9009).


SETUP
--------
Build and start the container:
      docker compose up -d

    First build installs xvfb, xdotool, python3-tk, python3-dev, pynput.
    Takes about 3 minutes.

    Verify:
      docker compose ps        (victim machine should be "running")

Enter the container:
      docker exec -it victim-machine bash


RUNNING THE DEMO
-------------------
Open THREE terminals inside the container:
      docker exec -it victim-machine bash     (repeat 3 times)

Terminal A - start the "remote" listener:
      cd /app
      python listener.py

    Expected:
      [listener] listening on 127.0.0.1:9009

Terminal B - start the keylogger:
      cd /app
      python keylogger.py &

Terminal C - simulate typing:
      export DISPLAY=:99
      xdotool type "username=alice"
      xdotool key Return
      xdotool type "password=hunter2"
      xdotool key Return

Observe results:
  - Terminal A shows each keystroke as it arrives over TCP.
  - Terminal C — the hidden log:
      cat /tmp/.sys_update_cache/keys.log
      # username=alice[ENTER]password=hunter2[ENTER]

Stop cleanly:
      export DISPLAY=:99 && xdotool key Escape     (stops keylogger)
      Ctrl+C in Terminal A                         (stops listener)


CLEANUP
----------
      docker compose down -v


TROUBLESHOOTING
------------------
  ImportError: pynput            -> docker compose build --no-cache
  Listener shows nothing         -> confirm DISPLAY=:99 in Terminal C and that xdotool type ran
  Address already in use on 9009 -> pkill -f listener.py, then restart
  Keylogger won't stop           -> pkill -f keylogger.py
