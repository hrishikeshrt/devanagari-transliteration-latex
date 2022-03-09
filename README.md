# Devanagari Transliteration in LaTeX

*Write in Devanagari to render as IAST, Harvard-Kyoto, Velthuis, SLP1, WX etc.*

Devanagari text can be transliterated in several [standard schemes](https://en.wikipedia.org/wiki/Devanagari_transliteration). Often, every user has a preference of scheme to type in (in my case, Devanagari). Similarly, one often faces a need to render it in different scheme in the PDF document (in my case, IAST).

I use the pipeline provided here as a simple solution for this problem.
The core component of it is the file `finalize.py` which contains the transliteration routine. However, for the sake of completeness, the entire setup is
made available here as an end-to-end solution.

## Minimal Example

* Write TeX content in `minimal.tex`
* Add the following lines in the preamble of the LaTeX file,
```latex

% This assumes your files are encoded as UTF8
\usepackage[utf8]{inputenc}

% Devanagari Related Packages
\usepackage{fontspec, xunicode, xltxtra}

% Define Fonts
\newfontfamily\textskt[Script=Devanagari]{Sanskrit 2003}
\newfontfamily\textiast[Script=Latin]{Sanskrit 2003}

% Commands for Devanagari Transliterations
\newcommand{\skt}[1]{{\textskt{#1}}}
\newcommand{\iast}[1]{{\textiast{#1}}}
\newcommand{\Iast}[1]{{\textiast{#1}}}
\newcommand{\IAST}[1]{{\textiast{#1}}}
```

* Use `\iast{}`, `\Iast{}` or `\IAST{}` tags to render Devanagari text in IAST format in lower case, title case and upper case respectively.
* Type the following command in the terminal,
```console
python3 finalize.py minimal.tex final.tex
```
* Proceed to compile the LaTeX file

## Full Setup

* TODO: Describe full setup

### Requirements

* XeLaTeX (unicode support) (included in [TeX Live](https://www.tug.org/texlive/))
* [Python3](https://www.python.org/downloads/) + [`indic-transliteration`](https://pypi.org/project/indic-transliteration/)

* [BibTeX](http://www.bibtex.org/) (optional) (bibliography support)
* [latexmk](https://mg.readthedocs.io/latexmk.html) (optional) (simpler TeX compilation)

### Instructions

* TODO: Give detailed instructions

## Devanagari Fonts

Nowadays, there are several good Devanagari fonts available. Google Fonts also provides a [wide variety of Devanagari fonts](https://fonts.google.com/?subset=devanagari).

Two of my personal favourites are,

* [Sanskrit 2003](https://omkarananda-ashram.org/Sanskrit/itranslator2003.htm#dls)
* [Noto Serif Devanagari](https://fonts.google.com/noto/specimen/Noto+Serif+Devanagari)

## Structure

```console

├── README.md
├── Makefile
├── finalize.py
├── papers.bib
├── fonts
│   └── Sanskrit2003.ttf
├── main.tex
└── sections
    └── content.tex
```