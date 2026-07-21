# Embedded explainer media

`marked-root-explainer.mp4` is the public 1920 x 1080, 30 fps H.264/AAC
render of `animations/jacobian_story.py`. It contains the complete 14-section
Manim explainer and an offline synthetic narration draft. The accompanying
`marked-root-explainer.en.vtt` file contains 104 ordered English caption cues
that losslessly partition the exact canonical narration; they are generated
from that text rather than speech recognition. Cues do not overlap, and the
last one ends before the film.

The draft voice is Piper `en_US-libritts-high`, speaker 0. It is synthetic,
is not presented as a recording by any credited mathematician, and should be
replaced by a clearly licensed human recording when one is accepted. Exact
model, corpus, software, and license attribution is recorded in the
repository-level `THIRD_PARTY_NOTICES.md`.

Release inspection values:

```text
duration     276.598698 seconds
video        H.264, 1920 x 1080, 30 fps, yuv420p
audio        AAC, 48 kHz, stereo
MP4 SHA-256  3758fb3a8944deda0b1f38c514133fa551b26c480e081ce7e55a31f58b15d925
VTT SHA-256  ec7f2bc253a9aa238f9566acd74e596a87297115ef1eed1378eee7125422a5f1
```

The MP4 is arranged for progressive web playback (`moov` before `mdat`).
The original animation source is MIT-licensed; the repository's original
visual composition, transcript, captions, and released narration artifact are
provided under CC BY 4.0. Third-party components retain their own licenses.
