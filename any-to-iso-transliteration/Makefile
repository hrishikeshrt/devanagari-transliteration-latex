all: .all

.all: main.tex sections/*.tex papers.bib
	latexpand main.tex > single.tex
	python3 finalize.py single.tex final.tex

	latexmk -pdflatex='xelatex %O %S' -pdf -ps- -dvi- final.tex

# rm -vf *.dvi *.pdf *.aux *.bbl *.synctex.gz *.out *.log *.blg *.bak *.fls *.fdb_latexmk 2> /dev/null
clear:
	latexmk -C
	rm single.tex
	rm final.tex

# rm -vf *.dvi *.aux *.bbl *.synctex.gz *.out *.log *.blg *.bak *.fls *.fdb_latexmk 2> /dev/null
clean:
	latexmk -c

