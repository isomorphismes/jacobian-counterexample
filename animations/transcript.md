# One map, three descriptions

The marked-root map behind a noninjective Keller map

This is the canonical narration transcript. The three-dimensional scenes show the real slice `R^3` inside the complex map on `C^3`.

## Provenance

- **[Levent Alpöge](https://x.com/__alpoge__/status/2079028340955197566):** Public announcement of the explicit polynomial map; the post credits Akhil for the question and Fable for the work.
- **Fable:** Credited in Alpöge's announcement for work on the explicit construction.
- **[Andy Jiang (@davikrehalt)](https://x.com/davikrehalt/status/2079175065695035442):** Posted the projective symmetric-product marked-root description, explicitly presenting it in the post as GPT output.
- **GPT:** Credited by Jiang's post for the projective marked-root formulation.
- **[Aaron Lou (@aaron_lou)](https://aaronlou.com/jacobian_counterexample_derivation.pdf):** Gave the factorization-resultant derivation and a global affine chart.
- **Repository contributors:** Compilation, independent checking, exposition, animation, and landing page; no claim to the discoveries above.

## Narration

### Provenance

#### Three public descriptions

This map reached the public in three distinct forms. Levent Alpöge posted the explicit polynomial formula, crediting Akhil for the question and Fable for the work. Later, Andy Jiang, at davikrehalt, posted the projective marked-root description and explicitly presented it as GPT output. Aaron Lou then gave a resultant-based derivation and global affine chart. This repository compiles, explains, visualizes, and checks those contributions.

### The puzzle

#### Local invertibility can fail globally

The Jacobian condition is local: at every finite point, the derivative is invertible. Imagine a tiny neighborhood being moved without being pinched flat. The surprise is global. Different distant points can still acquire the same image if inverse branches disappear through infinity. That is the mechanism we will see.

### Levent and Fable

#### The explicit polynomial certificate

Alpöge's presentation begins with three explicit polynomials in x, y, and z. Exact symbolic expansion gives determinant minus two everywhere. The formula is the fastest certificate that the map is locally invertible, but by itself it gives little clue why these particular terms fit together.

#### Three points, one value

Now substitute these three source points. They are distinct, yet every one maps to negative one quarter, zero, zero. This already proves noninjectivity. The remaining descriptions explain the hidden object that each point is recording.

### The common idea

#### Mark one root, then forget the mark

A cubic has three projective roots when multiplicity is counted. Temporarily mark one root and leave the other two unordered. For a cubic with three distinct roots, there are exactly three possible markings. If we now forget the mark, those three choices become one cubic. Generic degree three is therefore built into the construction.

### Jiang and GPT

#### The projective marked-root map

Jiang's post packages this as a projective map. A point p and an unordered pair q, r are sent to the unordered triple p, q, r. In symbols, projective one-space times its second symmetric power maps to its third symmetric power. This is simply the operation: forget which root was distinguished.

#### Delete only bad marked roots

The forgetful map ramifies only when the marked root collides with one of the two residual roots. Delete exactly that ramification divisor. The unmarked roots may still collide with each other. After deletion, the differential is invertible everywhere that remains, so the restricted map is étale.

#### The affine-space miracle

Next choose a hyperplane tangent, but not osculating, to the small diagonal of triple roots. Its complement in projective three-space is affine three-space. Remarkably, the corresponding source complement is also affine three-space. Choosing coordinates on these two spaces turns the geometric forgetful map into Alpöge's polynomial map.

### Lou

#### A marked root is a factor

Lou's description replaces a marked root by a factorization of the binary cubic: a linear factor ell for the marked root, times a quadratic factor q for the other two. But the factorization has a redundant scale. Multiplying ell by s and q by s inverse leaves the cubic unchanged.

#### The resultant fixes the scale

The linear-quadratic resultant detects whether the marked root is simple. It is nonzero exactly when ell and q have no common root. Under the redundant scaling, the resultant is multiplied by s. Requiring resultant one therefore chooses one and only one representative on every simple-root scaling orbit. This is the resultant gauge.

### Equivalence

#### Three languages for one arrow

These are not competing maps. They are three coordinate systems for one arrow. Alpöge gives the direct formula and collision certificate. Jiang and GPT expose the marked-root geometry. Lou supplies the normalized factor space and global affine chart. Lou's coordinate map G equals an output reversal after F and a sign change in the source. That is left-right equivalence, not dynamical conjugacy.

### Visualization

#### Exact curves on the real slice

Complex three-space has six real dimensions, so here we visualize only its real slice. Three elementary source curves are mapped exactly: the x-axis becomes a target line, the y-axis becomes a parabola, and the z-axis becomes another target line. The same formulas drive both this animation and the browser artifact.

#### Two inverse branches escape

A more revealing target curve represents cubics with roots zero, s, and one minus s. Each possible marked root defines a different source curve, but all three map to the same target curve. As s approaches zero, two marked roots collide. Their two source branches run toward infinity, while the branch marking the remaining simple root stays finite. No finite critical point appears.

### Conclusion

#### The proof spine and its scope

The proof now has a short spine. Both chosen complements are affine three-space. Removing marked-root ramification makes the forgetful map étale. A general cubic has three simple roots, so the map has generic degree three and cannot be injective. Constant Jacobian, three-point fibers, and escape at infinity are three views of the same geometry. Adding identity coordinates extends the construction to higher dimensions, while dimension two remains a separate problem.

## Accessibility note

The narration states all mathematically essential motion. Root branches are distinguished by labels as well as color. The video captions are generated from this text and published as WebVTT.

## License

Narration text and original visual composition are CC BY 4.0; animation source code is MIT-licensed. Third-party materials retain their own terms.
