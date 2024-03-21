I see, thank you for the clarification. Here's the revised version of your question:

**Title:**
"Buffering Goal Not Working with Multi-Period MPEG-DASH in Shaka Player"

**Body:**
I'm using the Shaka Player to play a multi-period MPEG-DASH video, but I'm encountering an issue with the buffering goal. I have an `input.mp4` file with a duration of 30 seconds, and I want to split it into segments of 10 seconds each.

Here are the steps I followed:

**Step 1:**
I used ffmpeg to split the video into segments:
```python
ffmpeg -i input.mp4 -c copy -map 0 -segment_time 10 -f segment input_%03d.mp4
```
This resulted in the following output files:
```
input_000.mp4
input_001.mp4
input_002.mp4
```

**Step 2:**
I used MP4Box to dash the segments into periods:
```python
MP4Box -dash 10000 input_000.mp4:period=0 input_001.mp4:period=1 input_002.mp4:period=2 -out out.mpd
```
This resulted in the following output files:
```
input_000_dashinit.mp4
input_001_dashinit.mp4
input_002_dashinit.mp4
out.mpd
```

I then attempted to play the `out.mpd` file using the Shaka Player in my HTML file. The player is configured with a `rebufferingGoal` and `bufferingGoal` of 10. However, the buffering goal does not seem to work with the multi-period MPEG-DASH video.

When I use the `https://storage.googleapis.com/shaka-demo-assets/angel-one/dash.mpd` URL, it works fine. But when I use my own `https://raw.githubusercontent.com/azoozs/shaka-player-multi-period/main/videos/out.mpd` URL, the buffering goal doesn't seem to work.

My question is: Why doesn't the `bufferingGoal: 10` setting work with a multi-period MPEG-DASH video?

Any help would be greatly appreciated. Thank you.
