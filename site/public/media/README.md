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
duration     278.231380 seconds
video        H.264, 1920 x 1080, 30 fps, yuv420p
audio        AAC, 48 kHz, stereo
MP4 SHA-256  c7ecb99fc2000da11cb95311897135b840fac768571b4c22de6c198bfa2a1d95
VTT SHA-256  876328b40312f024703fe2d75c96dbd08b68b94499b205154bf61f8490cc0316
```

The MP4 is arranged for progressive web playback (`moov` before `mdat`).
The original animation source is MIT-licensed; the repository's original
visual composition, transcript, captions, and released narration artifact are
provided under CC BY 4.0. Third-party components retain their own licenses.
