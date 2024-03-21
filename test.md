Sure, I can help you with that. Here's how you can improve your question:

**Title:**
"Multi-Period MPEG-DASH Not Working with Shaka Player"

**Body:**
I'm using the Shaka Player to play a multi-period MPEG-DASH video, but I'm encountering an issue. I have an `input.mp4` file with a duration of 30 seconds, and I want to split it into segments of 10 seconds each.

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

I then attempted to play the `out.mpd` file using the Shaka Player in my HTML file. The player is configured with a `rebufferingGoal` and `bufferingGoal` of 10. However, the multi-period MPEG-DASH video does not seem to work with these settings.

When I use the `https://storage.googleapis.com/shaka-demo-assets/angel-one/dash.mpd` URL, it works fine. But when I use my own `https://raw.githubusercontent.com/azoozs/shaka-player-multi-period/main/videos/out.mpd` URL, it doesn't work.

My question is: Why don't the `rebufferingGoal: 10` and `bufferingGoal: 10` settings work with a multi-period MPEG-DASH video?

Any help would be greatly appreciated. Thank you.
