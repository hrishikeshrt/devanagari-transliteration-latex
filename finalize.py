#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaTeX Finalization
------------------

- Transliteration
- Comment Removal
- Whitespace Cleaning
    - Trailing Whitespaces
    - Multiple Blank Lines

@author: Hrishikesh Terdalkar
"""

import os
import re
import argparse
from typing import Callable, List
from indic_transliteration.sanscript import transliterate
from indic_transliteration import sanscript

###############################################################################


def transliterate_between(
    text: str,
    from_scheme: str,
    to_scheme: str,
    start_pattern: str,
    end_pattern: str,
    post_hook: Callable[[str], str] or None = None,
) -> str:
    """Transliterate the text appearing between two patterns

    Only the text appearing between patterns `start_pattern` and `end_pattern`
    it transliterated.
    `start_pattern` and `end_pattern` can appear multiple times in the full
    text, and for every occurrence, the text between them is transliterated.

    `from_scheme` and `to_scheme` should be compatible with scheme names from
    `indic-transliteration`

    Parameters
    ----------
    text : str
        Full text
    from_scheme : str
        Input transliteration scheme
    to_scheme : str
        Output transliteration scheme
    start_pattern : regexp
        Pattern describing the start tag
    end_pattern : regexp
        Pattern describing the end tag
    post_hook : Callable[[str], str], optional
        Function to be applied on the text within tags after transliteration
        The default is `lambda x: x`.

    Returns
    -------
    str
        Text after replacements
    """

    if from_scheme == to_scheme:
        return text

    if post_hook is None:
        post_hook = lambda x: x

    def transliterate_match(matchobj):
        target = matchobj.group(1)
        replacement = transliterate(target, from_scheme, to_scheme)
        replacement = post_hook(replacement)
        return f"{start_pattern}{replacement}{end_pattern}"

    pattern = "%s(.*?)%s" % (re.escape(start_pattern), re.escape(end_pattern))
    return re.sub(pattern, transliterate_match, text, flags=re.DOTALL)


###############################################################################
# Generic LaTeX Transliteration


def latex_transliteration(
    input_text: str,
    from_scheme: str,
    to_scheme: str
) -> str:
    """Transliterate parts of the LaTeX input enclosed in scheme tags

    A scheme tag is of the form `\\to_scheme_lowercase{}` and is used
    when the desired output is in `to_scheme`.

    i.e.,
    - Tags for IAST scheme are enclosed in \\iast{} tags
    - Tags for ITrans scheme are enclosed in \\itrans{} tags
    - Tags for VH scheme are enclosed in \\vh{} tags
    - ...

    Parameters
    ----------
    input_text : str
        Input text
    from_scheme : str
        Transliteration scheme of the text written within the input tags
    to_scheme : str
        Transliteration scheme to which the text within tags should be
        transliterated

    Returns
    -------
    str
        Text after replacement of text within the scheme tags
    """
    start_tag_pattern = f"\\{to_scheme.lower()}"
    end_tag_pattern = "}"
    return transliterate_between(
        input_text,
        from_scheme=from_scheme,
        to_scheme=to_scheme,
        start_pattern=start_tag_pattern,
        end_pattern=end_tag_pattern
    )

###############################################################################
# Apply Chain of Transliterations


def apply_transliteration_chain(
    input_text: str,
    transliteration_chain: List[List]
):
    intermediate_text = input_text
    for transliteration_config in transliteration_chain:
        intermediate_text = transliterate_between(
            intermediate_text,
            **transliteration_config
        )
    return intermediate_text


###############################################################################
# Example: Devanagari to IAST Chain

DEVANAGARI_TO_IAST_TRANSFORMATIONS = [
    {
        "from_scheme": sanscript.DEVANAGARI,
        "to_scheme": sanscript.IAST,
        "start_pattern": "\\iast{",
        "end_pattern": "}"
    },
    {
        "from_scheme": sanscript.DEVANAGARI,
        "to_scheme": sanscript.IAST,
        "start_pattern": "\\Iast{",
        "end_pattern": "}",
        "post_hook": lambda x: x.title()
    },
    {
        "from_scheme": sanscript.DEVANAGARI,
        "to_scheme": sanscript.IAST,
        "start_pattern": "\\IAST{",
        "end_pattern": "}",
        "post_hook": lambda x: x.upper()
    }
]

def devanagari_to_iast(input_text: str) -> str:
    """Transliterate parts of the input enclosed in
    \\iast{}, \\Iast{} or \\IAST{} tags from Devanagari to IAST

    Text in \\Iast{} tags also undergoes a `.title()` post-hook.
    Text in \\IAST{} tags also undergoes a `.upper()` post-hook.

    Parameters
    ----------
    input_text : str
        Input text

    Returns
    -------
    str
        Text after replacement of text within the IAST tags
    """

    return apply_transliteration_chain(
        input_text,
        DEVANAGARI_TO_IAST_TRANSFORMATIONS
    )

###############################################################################
# Example: Bengali to ISO/ITRANS/IAST Chain


BENGALI_TRANSFORMATIONS = [
    {
        "from_scheme": sanscript.BENGALI,
        "to_scheme": sanscript.ISO,
        "start_pattern": "\\textiso{",
        "end_pattern": "}"
    },
    {
        "from_scheme": sanscript.BENGALI,
        "to_scheme": sanscript.ISO,
        "start_pattern": "\\Iso{",
        "end_pattern": "}",
        "post_hook": lambda x: x.title()
    },
    {
        "from_scheme": sanscript.BENGALI,
        "to_scheme": sanscript.ISO,
        "start_pattern": "\\ISO{",
        "end_pattern": "}",
        "post_hook": lambda x: x.upper()
    },
    {
        "from_scheme": sanscript.BENGALI,
        "to_scheme": sanscript.ITRANS,
        "start_pattern": "\\textitrans{",
        "end_pattern": "}"
    },
    {
        "from_scheme": sanscript.BENGALI,
        "to_scheme": sanscript.IAST,
        "start_pattern": "\\textiast{",
        "end_pattern": "}"
    },
    {
        "from_scheme": sanscript.BENGALI,
        "to_scheme": sanscript.IAST,
        "start_pattern": "\\Iast{",
        "end_pattern": "}",
        "post_hook": lambda x: x.title()
    },
    {
        "from_scheme": sanscript.BENGALI,
        "to_scheme": sanscript.IAST,
        "start_pattern": "\\IAST{",
        "end_pattern": "}",
        "post_hook": lambda x: x.upper()
    }
]

def bengali_to_multiple(input_text: str) -> str:
    """Transliterate parts of the input enclosed in
    \\textiast{}, \\Iast{} or \\IAST{} tags from Bengali to IAST
    \\textiso{}, \\Iso{} or \\ISO{} tags from Bengali to ISO
    \\textitrans{} tags from Bengali to ITRANS

    Text in \\Iast{} and \\Iso{} tags also undergoes a `.title()` post-hook.
    Text in \\IAST{} tags \\ISO{} also undergoes a `.upper()` post-hook.

    Parameters
    ----------
    input_text : str
        Input text

    Returns
    -------
    str
        Text after replacement of text within the IAST tags
    """

    return apply_transliteration_chain(
        input_text,
        BENGALI_TRANSFORMATIONS
    )

###############################################################################


def remove_comments(input_text: str) -> str:
    """Remove LaTeX Comments"""
    start = "\\begin{comment}"
    end = "\\end{comment}"
    pattern = "%s(.*?)%s" % (re.escape(start), re.escape(end))
    return re.sub(pattern, '', input_text, flags=re.DOTALL)

###############################################################################


def clean_whitespaces(input_text: str) -> str:
    """Remove trailing whitespaces and consective blank lines

    Parameters
    ----------
    input_text : str
        Input text

    Returns
    -------
    str
        Output text after whitespace cleaning
    """
    _text = re.sub(r"[\t\r ]+?\n", "\n", input_text)
    _text = re.sub("\n\n+", "\n\n", _text, flags=re.DOTALL)
    return _text


###############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LaTeX IAST Parser')
    parser.add_argument('infile', help='Name of the Input LaTeX file')
    parser.add_argument('outfile', help='Name of the Output LaTeX file')

    args = vars(parser.parse_args())
    infile = args['infile']
    outfile = args['outfile']

    if not os.path.isfile(infile):
        raise FileNotFoundError(f"{infile} does not exist.")

    with open(infile, 'r') as f:
        input_text = f.read()

    # ----------------------------------------------------------------------- #
    # Sample LaTeX Finalization Pipeline

    _text = input_text

    _text = devanagari_to_iast(_text)         # Transliteration
    _text = remove_comments(_text)            # Comment Removal
    _text = clean_whitespaces(_text)          # Whitespace Cleaning

    output_text = _text

    # ----------------------------------------------------------------------- #

    with open(outfile, 'w') as f:
        f.write(output_text)
