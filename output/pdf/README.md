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

[marked_root_binary_cubic.pdf](marked_root_binary_cubic.pdf) is retained as
historical version 1. It records the earlier coordinate-free audit, but it is
not the current paper and does not supersede the canonical synthesis above.
That frozen historical artifact predates the recording of Lou's X handle; the
canonical paper carries the corrected attribution and profile link.
