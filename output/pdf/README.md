# Paper artifacts

The current canonical paper is
[One Map, Three Descriptions](one_map_three_descriptions.pdf). Its LaTeX source
is [src/distinguished_root_map.tex](../../src/distinguished_root_map.tex).
It gives the short, beginner-first synthesis of the Alpöge--Fable coordinate
presentation, the Jiang--GPT projective presentation, and the resultant
presentation of Aaron Lou (@aaron_lou), together with their exact
source--target equivalence.  The current revision also incorporates Daniel
Litt's ([@littmath](https://x.com/littmath))
[affine-line-bundle observation](https://x.com/littmath/status/2079347618417971212)
and [pencil gloss](https://x.com/littmath/status/2079353531430289734),
which he described as developed
[with substantial ChatGPT help](https://x.com/littmath/status/2079414119720165633).
Litt's later [comparison comment](https://x.com/littmath/status/2079475742401003816)
emphasizes that this is an explanation of the same construction, not a fourth
construction.  The explicit chart remains the global trivialization proof.

Rebuild the canonical PDF from the repository root with:

```sh
make paper
```

The target runs `pdflatex` twice, rejects LaTeX warnings and overfull boxes,
and writes the finished PDF to `output/pdf/one_map_three_descriptions.pdf`.

## Unified reconstruction dialogue

[Could One Have Found It This Way? A Six-Question Reconstruction of a
Three-Dimensional Keller Counterexample](six_questions_keller_map.pdf)
unifies the marked-cubic construction with the constrained coefficient
reconstruction developed on the why-this-counterexample branch.  It is a
synthetic, post-announcement dialogue rather than a historical transcript.
Each of its six exchanges separates what is chosen, what follows, and what is
still owed; the final coefficient solve receives neither a nonlinear
numerical coefficient nor a collision equation.

Its source is
[src/six_questions_keller_map.tex](../../src/six_questions_keller_map.tex),
and its independent exact replay is
[artifacts/sympy/verify_dialogue_reconstruction.py](../../artifacts/sympy/verify_dialogue_reconstruction.py).
Rebuild it with:

```sh
make dialogue-paper
```

The build target runs `pdflatex` twice, rejects LaTeX warnings and overfull
boxes, and writes `output/pdf/six_questions_keller_map.pdf`.

[marked_root_binary_cubic.pdf](marked_root_binary_cubic.pdf) is retained as
historical version 1. It records the earlier coordinate-free audit, but it is
not the current paper and does not supersede the canonical synthesis above.
That frozen historical artifact predates the recording of Lou's X handle; the
canonical paper carries the corrected attribution and profile link.
