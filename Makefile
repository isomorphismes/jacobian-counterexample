.PHONY: verify sympy sage magma test book clean

verify: sympy sage magma test

sympy:
	python3 artifacts/sympy/verify.py
	python3 artifacts/sympy/verify_plane_attack.py
	python3 research/n2/search_graph_sections.py --groebner

sage:
	DOT_SAGE=/tmp/jacobian-sage sage artifacts/sage/verify.sage
	DOT_SAGE=/tmp/jacobian-sage sage research/n2/low_degree_collision.sage

magma:
	cd artifacts/magma && MAGMA_STARTUP_FILE=/dev/null /Applications/Magma/magma run_all.m

test:
	pytest -q

book:
	jupyter-book build knowledge

clean:
	jupyter-book clean knowledge
