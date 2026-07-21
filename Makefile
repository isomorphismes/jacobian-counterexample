PAPER_SOURCE := src/distinguished_root_map.tex
PAPER_NAME := one_map_three_descriptions
PAPER_OUTPUT_DIR := output/pdf
PAPER_BUILD_DIR := tmp/paper-build
PAPER_PDF := $(PAPER_OUTPUT_DIR)/$(PAPER_NAME).pdf
PAPER_LOG := $(PAPER_BUILD_DIR)/$(PAPER_NAME).log
DIALOGUE_SOURCE := src/six_questions_keller_map.tex
DIALOGUE_NAME := six_questions_keller_map
DIALOGUE_BUILD_DIR := tmp/pdfs/dialogue-paper-build
DIALOGUE_PDF := $(PAPER_OUTPUT_DIR)/$(DIALOGUE_NAME).pdf
DIALOGUE_LOG := $(DIALOGUE_BUILD_DIR)/$(DIALOGUE_NAME).log

.PHONY: verify sympy sage magma test book paper dialogue-paper clean

verify: sympy sage magma test

sympy:
	python3 artifacts/sympy/verify.py
	python3 artifacts/sympy/verify_plane_attack.py
	python3 artifacts/sympy/verify_resultant_route.py
	PYTHONDONTWRITEBYTECODE=1 python3 artifacts/sympy/verify_dialogue_reconstruction.py
	python3 research/n2/certify_pseudoplane_poisson.py
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

paper:
	@command -v pdflatex >/dev/null || { echo "pdflatex is required to build the paper"; exit 127; }
	@mkdir -p "$(PAPER_BUILD_DIR)" "$(PAPER_OUTPUT_DIR)"
	@pdflatex -interaction=nonstopmode -halt-on-error \
		-jobname="$(PAPER_NAME)" -output-directory="$(PAPER_BUILD_DIR)" \
		"$(PAPER_SOURCE)" >"$(PAPER_BUILD_DIR)/pass1.stdout" || \
		{ sed -n '1,240p' "$(PAPER_BUILD_DIR)/pass1.stdout"; exit 1; }
	@pdflatex -interaction=nonstopmode -halt-on-error \
		-jobname="$(PAPER_NAME)" -output-directory="$(PAPER_BUILD_DIR)" \
		"$(PAPER_SOURCE)" >"$(PAPER_BUILD_DIR)/pass2.stdout" || \
		{ sed -n '1,240p' "$(PAPER_BUILD_DIR)/pass2.stdout"; exit 1; }
	@issues="$$(grep -En 'LaTeX Warning|Package .* Warning|Overfull \\[hv]box' "$(PAPER_LOG)" || true)"; \
		if [ -n "$$issues" ]; then \
			echo "Paper build produced warnings or overfull boxes:"; \
			echo "$$issues"; \
			exit 1; \
		fi
	@cp "$(PAPER_BUILD_DIR)/$(PAPER_NAME).pdf" "$(PAPER_PDF)"
	@echo "Built $(PAPER_PDF)"

dialogue-paper:
	@command -v pdflatex >/dev/null || { echo "pdflatex is required to build the dialogue paper"; exit 127; }
	@mkdir -p "$(DIALOGUE_BUILD_DIR)" "$(PAPER_OUTPUT_DIR)"
	@pdflatex -interaction=nonstopmode -halt-on-error \
		-jobname="$(DIALOGUE_NAME)" -output-directory="$(DIALOGUE_BUILD_DIR)" \
		"$(DIALOGUE_SOURCE)" >"$(DIALOGUE_BUILD_DIR)/pass1.stdout" || \
		{ sed -n '1,240p' "$(DIALOGUE_BUILD_DIR)/pass1.stdout"; exit 1; }
	@pdflatex -interaction=nonstopmode -halt-on-error \
		-jobname="$(DIALOGUE_NAME)" -output-directory="$(DIALOGUE_BUILD_DIR)" \
		"$(DIALOGUE_SOURCE)" >"$(DIALOGUE_BUILD_DIR)/pass2.stdout" || \
		{ sed -n '1,240p' "$(DIALOGUE_BUILD_DIR)/pass2.stdout"; exit 1; }
	@issues="$$(grep -En 'LaTeX Warning|Package .* Warning|Overfull \\[hv]box' "$(DIALOGUE_LOG)" || true)"; \
		if [ -n "$$issues" ]; then \
			echo "Dialogue-paper build produced warnings or overfull boxes:"; \
			echo "$$issues"; \
			exit 1; \
		fi
	@cp "$(DIALOGUE_BUILD_DIR)/$(DIALOGUE_NAME).pdf" "$(DIALOGUE_PDF)"
	@echo "Built $(DIALOGUE_PDF)"

clean:
	jupyter-book clean knowledge
