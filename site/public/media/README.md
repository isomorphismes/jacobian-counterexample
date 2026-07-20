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
duration     275.732031 seconds
video        H.264, 1920 x 1080, 30 fps, yuv420p
audio        AAC, 48 kHz, stereo
MP4 SHA-256  5c1c1a1be8f9fe53687aeeda71e434d79bd8b743f747157acebee7a38d28e318
VTT SHA-256  b0a684027cad8dabe70de85655ed4d86b0112bb5a3a38f3a0f5167a3d0d0f09c
```

The MP4 is arranged for progressive web playback (`moov` before `mdat`).
The original animation source is MIT-licensed; the repository's original
visual composition, transcript, captions, and released narration artifact are
provided under CC BY 4.0. Third-party components retain their own licenses.
