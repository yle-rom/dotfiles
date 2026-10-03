#!/usr/bin/env bash
# Run a preview bar NEXT TO your current one. Your real bar is never touched.
#   ./preview.sh phosphor        -> shows until you press Enter
#   ./preview.sh phosphor 8      -> shows for 8 seconds
#   ./preview.sh all             -> all four side by side until Enter
cd "$(dirname "$0")" || exit 1
names=("$@"); secs=""
[[ ${names[-1]} =~ ^[0-9]+$ ]] && { secs=${names[-1]}; unset 'names[-1]'; }
[[ ${names[0]} == all ]] && names=(phosphor islands nerv nerv2 hud)
[[ ${names[0]} == meters ]] && names=(meters/a-frame meters/b-gauge meters/c-segments meters/d-line)
[[ ${names[0]} == nerv3 ]] && names=(nerv2 nerv3/clean nerv3/outline nerv3/borderless)
[[ ${names[0]} == clock ]] && names=(clock/1-big clock/2-week clock/3-ruler clock/4-sideways clock/5-readout)
[[ ${names[0]} == fonts ]] && names=(clock/1-big clock/font-vt323 clock/font-sharetech clock/font-dseg7 clock/font-spacemono clock/font-plex)
pids=()
for n in "${names[@]}"; do
  [[ -f $n/style.css ]] || { echo "no variant: $n"; continue; }
  waybar -c "$n/config" -s "$n/style.css" >/dev/null 2>&1 & pids+=($!)
done
if [[ -n $secs ]]; then sleep "$secs"; else read -rp "Enter to close previews… "; fi
kill "${pids[@]}" 2>/dev/null
