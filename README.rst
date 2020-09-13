Pandoc ``acro`` Filter
======================

This filter provides a means to manage acronyms in Pandoc_ flavored
Markdown sources.  It aims to do for Pandoc what the |acro|_ package
does for LaTeX.  As such, it's initial goal is to translate marked
acronyms into the appropriate ``acro`` LaTeX macros.  It does this by
extracting acronym definitions in the metadata ``acronyms`` map and
looking for keys in the main text that begin with a ‘``+``’ such as
``+afaik``.  The keys can be normal string words or they can use the
`native span`_ syntax to override the local formatting.  For details,
see the `Usage`_ section below.

.. _Pandoc: https://pandoc.org
.. |acro| replace:: ``acro``
.. _acro: https://ctan.org/pkg/acro?lang=en
.. _`native span`: https://pandoc.org/MANUAL.html#extension-native_divs

Installation
------------

The simplest way to install and use this filter is to download the main
script and pass it to Pandoc as a filter, i.e.

.. code-block:: bash

    pandoc -F <path/to/download>/pandoc-acro.py input.md

Alternatively, the script can be installed using the standard Python
``setuptools`` with ``python setup.py install``.

Usage
-----

Acronym Definitions
^^^^^^^^^^^^^^^^^^^

To define an acronym, place it in the ``acronyms`` map in the metadata.
The syntax is designed to replicate that used by the LaTeX ``acro``
package.  Each acronym must define a ``long`` and ``short`` form.
Beyond the minimum, each acronym can define:

-   ``short-plural``: The plural ending of the short form.
    Defaults to ‘s’.
-   ``long-plural``: The plural ending of the long form.
    Defaults to ‘s’.

An example metadata block would be:

.. code-block:: yaml

    ---
    acronyms:
      afaik:
        short: AFAIK
        long: as far as I know
      lol:
        short: lol
        long: laugh out loud
        short-plural: es  # Contrived for example purposes
        long-plural: es   # Contrived for example purposes
    ...

Inline Usage
^^^^^^^^^^^^

The simplest usage in text is to prepend a key with ‘``+``’ such as
``+afaik``.  This will expand to the ``long`` form followed by the
``short`` inside parentheses on first usage and by the ``short`` form on
subsequent use.  The aim is to replicate the behavior of the ``acro``
package from LaTeX.  The default behavior can be overridden by placing
the key in a span and specifying the ``short``, ``long``, or ``full``
class.  To get the plural form, set the ``plural`` class in the span.
To be clear, the mapping is:

+-------------------------------+-------------------+-------------------------------+
| Markdown                      | LaTeX             | Expanded text                 |
+===============================+===================+===============================+
| ``+afaik``                    | ``\ac{afaik}``    | as far as I know (AFAIK)      |
| ``+afaik``                    | ``\ac{afaik}``    | AFAIK                         |
| ``[+afaik]{.short}``          | ``\acs{afaik}``   | AFAIK                         |
| ``[+afaik]{.short .plural}``  | ``\acsp{afaik}``  | AFAIKs                        |
| ``[+afaik]{.long}``           | ``\acl{afaik}``   | as far as I know              |
| ``[+afaik]{.long .plural}``   | ``\aclp{afaik}``  | as far as I knows             |
| ``[+afaik]{.full}``           | ``\acf{afaik}``   | as far as I know (AFAIK)      |
| ``[+afaik]{.full .plural}``   | ``\acfp{afaik}``  | as far as I knows (AFAIKs)    |
+-------------------------------+-------------------+-------------------------------+

Output Format Notes
-------------------

LaTeX
^^^^^

The acronyms definitions in the metadata are transformed to
``\DeclareAcronym`` commands and are added to the ``header-includes``
metadata field after ``\usepackage{acro}``.  These are entered as raw
LaTeX Inlines.  The running text markup is translated to the appropriate
``acro`` macro as described in the above table.

