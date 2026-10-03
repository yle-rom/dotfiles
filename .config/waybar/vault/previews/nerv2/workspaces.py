#!/usr/bin/env python3
"""One workspace button for waybar: kanji + a dot per open window.
Usage: workspaces.py <id>. Listens to Hyprland's event socket, prints JSON lines."""
import json, os, socket, sys

WS = int(sys.argv[1])
# Evangelion units: 初号機 (Unit-01), 弐号機, 参号機, 四号機 ...
KANJI = {1: "初", 2: "弐", 3: "参", 4: "四", 5: "伍", 6: "六", 7: "七", 8: "八", 9: "九", 10: "十"}
MAX_DOTS = 4
HYPR = f"{os.environ['XDG_RUNTIME_DIR']}/hypr/{os.environ['HYPRLAND_INSTANCE_SIGNATURE']}"
TRIGGERS = (b"workspace", b"openwindow", b"closewindow", b"movewindow",
            b"focusedmon", b"createworkspace", b"destroyworkspace")


def query(cmd):
    with socket.socket(socket.AF_UNIX) as s:
        s.connect(f"{HYPR}/.socket.sock")
        s.sendall(f"j/{cmd}".encode())
        data = b""
        while chunk := s.recv(65536):
            data += chunk
    return json.loads(data)


def render():
    windows = next((w["windows"] for w in query("workspaces") if w["id"] == WS), 0)
    active = query("activeworkspace")["id"] == WS
    dots = "•" * min(windows, MAX_DOTS) + ("+" if windows > MAX_DOTS else "")
    cls = "active" if active else "occupied" if windows else "empty"
    text = f"{KANJI.get(WS, WS)}\n<span size='7pt' rise='2pt'>{dots or ' '}</span>"
    tip = f"Workspace {WS} · {windows} window{'s' * (windows != 1)}"
    print(json.dumps({"text": text, "class": cls, "tooltip": tip}), flush=True)


render()
with socket.socket(socket.AF_UNIX) as ev:
    ev.connect(f"{HYPR}/.socket2.sock")
    buf = b""
    while chunk := ev.recv(4096):
        buf += chunk
        *lines, buf = buf.split(b"\n")
        if any(l.startswith(TRIGGERS) for l in lines):
            render()
