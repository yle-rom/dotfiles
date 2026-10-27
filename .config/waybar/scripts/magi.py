#!/usr/bin/env python3
"""MAGI vote, one module per computer. Usage: magi.py gpu|cpu|ram
  gpu  MELCHIOR-1   temp + load (nvidia-smi; skipped while the dGPU sleeps, so polling never wakes it)
  cpu  BALTHASAR-2  package temp + load
  ram  CASPER-3     used memory
Each prints only on change; class cool|warm|hot drives its own color."""
import glob, json, subprocess, sys, time

GPU_PCI = "/sys/bus/pci/devices/0000:01:00.0"


def emit(text, cls):
    print(json.dumps({"text": text, "class": cls}), flush=True)


def level(v, warm, hot):
    return "hot" if v >= hot else "warm" if v >= warm else "cool"


def worst(*levels):
    return max(levels, key=["cool", "warm", "hot"].index)


def gpu():
    if open(f"{GPU_PCI}/power/runtime_status").read().strip() != "active":
        return "SLEEP", "sleep"
    out = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu,utilization.gpu", "--format=csv,noheader,nounits"],
                         capture_output=True, text=True).stdout
    temp, load = (int(x) for x in out.split(","))
    return f"{temp}° {load:>2}%", worst(level(temp, 75, 85), level(load, 80, 95))


def cpu_temp_path():  # same lookup as sysmon.py: hwmon numbers change between boots
    for h in glob.glob("/sys/class/hwmon/hwmon*"):
        if open(f"{h}/name").read().strip() == "coretemp":
            for lab in glob.glob(f"{h}/temp*_label"):
                if open(lab).read().startswith("Package"):
                    return lab.replace("_label", "_input")


def cpu_times():
    v = [int(x) for x in open("/proc/stat").readline().split()[1:]]
    idle = v[3] + v[4]
    return sum(v) - idle, sum(v)


def cpu_reader():
    tpath, prev = cpu_temp_path(), cpu_times()

    def read():
        nonlocal prev
        busy, total = cpu_times()
        load = round(100 * (busy - prev[0]) / max(1, total - prev[1]))
        prev = (busy, total)
        temp = int(open(tpath).read()) // 1000 if tpath else 0
        return f"{temp}° {load:>2}%", worst(level(temp, 75, 90), level(load, 80, 95))
    return read


def ram():
    m = {l.split(":")[0]: int(l.split()[1]) for l in open("/proc/meminfo")}
    used = round(100 * (1 - m["MemAvailable"] / m["MemTotal"]))
    return f"{used:>2}%", level(used, 75, 90)


NAME = {"gpu": "MELCHIOR", "cpu": "BALTHASAR", "ram": "CASPER"}
VOTE = {"cool": "承認", "warm": "警告", "hot": "否決", "sleep": "休止"}   # approve, warning, reject, dormant
read = {"gpu": gpu, "cpu": cpu_reader(), "ram": ram}[sys.argv[1]]
last = None
while True:
    time.sleep(2)
    value, cls = read()
    text = f"{NAME[sys.argv[1]]} {VOTE[cls]}"
    if (text, cls) != last:
        emit(text, cls)
        last = (text, cls)
