resume.pdf: resume.tex
	latexmk -xelatex -interaction=nonstopmode -halt-on-error resume.tex
	cp resume.pdf ../public/resume.pdf
	cp resume.pdf "Atharva Mohite Resume.pdf"

clean:
	latexmk -C
	rm -f "Atharva Mohite Resume.pdf"

.PHONY: clean
