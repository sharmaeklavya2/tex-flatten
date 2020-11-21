INAME = main
ONAME = my-thms
QOPTS = -cnf-line "max_print_line = 10000" -halt-on-error
all:
	pdflatex -jobname=$(ONAME) $(INAME).tex
	bibtex $(ONAME).aux
	pdflatex -jobname=$(ONAME) $(INAME).tex
	pdflatex -jobname=$(ONAME) $(INAME).tex
clean:
	rm -f *.{aux,bbl,blg,log,out,toc}
quiet:
	pdflatex $(QOPTS) -jobname=$(ONAME) $(INAME).tex | tex-filter.py --citeref=1
	@echo
	bibtex $(ONAME).aux
	@echo
	pdflatex $(QOPTS) -jobname=$(ONAME) $(INAME).tex | tex-filter.py --citeref=1
	@echo
	pdflatex $(QOPTS) -jobname=$(ONAME) $(INAME).tex | tex-filter.py
