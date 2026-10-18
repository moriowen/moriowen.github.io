resume.pdf: resume.tex
	latexmk -xelatex -interaction=nonstopmode -halt-on-error resume.tex
	cp resume.pdf ../public/resume.pdf

clean:
	latexmk -C

.PHONY: clean
