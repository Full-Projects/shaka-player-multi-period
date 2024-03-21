# shaka-player-multi-period
I have `input.mp4` (duration: 30 seconds)
# Step 1:
```python
ffmpeg -i input.mp4 -c copy -map 0 -segment_time 10 -f segment input_%03d.mp4
```
output:
```
input_000.mp4
input_001.mp4
input_002.mp4
```

# Step 2:
```python
MP4Box -dash 10000 input_000.mp4:period=0 input_001.mp4:period=1 input_002.mp4:period=2 -out out.mpd
```

output:
```
input_000_dashinit.mp4
input_001_dashinit.mp4
input_002_dashinit.mp4
out.mpd
```
