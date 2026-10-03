#!/usr/bin/env python3
"""Generate meter-style experiments on top of nerv2 (only the battery/volume parts differ)."""
import json, os

base = json.load(open("../nerv2/config"))
DIM = "<span alpha='35%'>{}</span>"

def bar(fill, empty, left="", right="", n=10, dim_empty=True):
    out = []
    for i in range(n + 1):
        e = empty * (n - i)
        out.append(left + fill * i + (DIM.format(e) if dim_empty and e else e) + right)
    return out

# vertical battery glyphs (md battery 10..100) + volume glyphs, used with the Mono font
BATT = ["󰁺", "󰁻", "󰁼", "󰁽", "󰁾", "󰁿", "󰂀", "󰂁", "󰂂", "󰁹"]
VOL = ["󰕿", "󰖀", "󰕾"]

VARIANTS = {
    # A: CSS frame instead of [ ], text labels instead of icons
    "a-frame": dict(bar=bar("█", "░"), muted=bar("█", "░")[0],
                    bat_icon=["BAT"], bat_chg="CHG", vol_icon=["VOL"], vol_muted="MUTE"),
    # B: gauge caps (├ ┤ turn into ┬ ┴ when rotated), vertical battery glyphs
    "b-gauge": dict(bar=bar("█", "░", "├", "┤"), muted=bar("█", "░", "├", "┤")[0],
                    bat_icon=BATT, bat_chg="󰂄", vol_icon=VOL, vol_muted="󰝟"),
    # C: LED segments, no caps
    "c-segments": dict(bar=bar("▮", "▮"), muted=bar("▮", "▮")[0],
                       bat_icon=BATT, bat_chg="󰂄", vol_icon=VOL, vol_muted="󰝟"),
    # D: thin line gauge with heavy caps (┣ ┫ -> ┳ ┻)
    "d-line": dict(bar=bar("━", "╌", "┣", "┫"), muted=bar("━", "╌", "┣", "┫")[0],
                   bat_icon=BATT, bat_chg="󰂄", vol_icon=VOL, vol_muted="󰝟"),
}

for name, v in VARIANTS.items():
    os.makedirs(name, exist_ok=True)
    c = json.loads(json.dumps(base))
    c["battery#bar"]["format-icons"] = v["bar"]
    c["pulseaudio#bar"]["format-icons"] = {"default": v["bar"]}
    c["pulseaudio#bar"]["format-muted"] = v["muted"]
    c["battery#icon"]["format-icons"] = v["bat_icon"]
    c["battery#icon"]["format-charging"] = v["bat_chg"]
    c["pulseaudio#icon"]["format-icons"] = {"default": v["vol_icon"]}
    c["pulseaudio#icon"]["format-muted"] = v["vol_muted"]
    for k in ["battery#icon", "battery#bar", "battery#percentage",
              "pulseaudio#icon", "pulseaudio#bar", "pulseaudio#percentage"]:
        c[k]["justify"] = "center"
    json.dump(c, open(f"{name}/config", "w"), indent=2, ensure_ascii=False)
