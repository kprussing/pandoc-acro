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

To install, download the source and run ``python setup.py install`` from
the top of the source tree.  Then pass ``pandoc-acro`` as a filter to
Pandoc_ e.g.

.. code-block:: bash

    pandoc -F pandoc-acro input.md

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

The only reserved acronym is ``options`` which is reserved for passing
additional options to the ``\acsetup`` macro in LaTeX.  The options are
translated to the form ``key=value`` and are passed as a comma separated
option to ``\acsetup``.  The filter will try to sanity check the
options.  If it cannot convert the option to a string or boolean, the
option is skipped and a warning is issued.  If it is a known option used
by the filter, it checks for a valid value and issues a warning if it is
not valid but it still passes the option to ``\acsetup``.

Inline Usage
^^^^^^^^^^^^

The simplest usage in text is to prepend a key with ‘``+``’ such as
``+afaik``.  This will expand to the ``long`` form followed by the
``short`` inside parentheses on first usage and by the ``short`` form on
subsequent use.  The aim is to replicate the behavior of the ``acro``
package from LaTeX.  The default behavior can be overridden by placing
the key in a span and specifying the ``short``, ``long``, or ``full``
class.  To get the plural form, set the ``plural`` class in the span,
and to set the initial capitalization use ``caps``.  To be clear, the
mapping is:

+------------------------------------+-------------------+-------------------------------+
| Markdown                           | LaTeX             | Expanded text                 |
+====================================+===================+===============================+
| ``+afaik``                         | ``\ac{afaik}``    | as far as I know (AFAIK)      |
+------------------------------------+-------------------+-------------------------------+
| ``+afaik``                         | ``\ac{afaik}``    | AFAIK                         |
+------------------------------------+-------------------+-------------------------------+
| ``[+afaik]{.short}``               | ``\acs{afaik}``   | AFAIK                         |
+------------------------------------+-------------------+-------------------------------+
| ``[+afaik]{.short .plural}``       | ``\acsp{afaik}``  | AFAIKs                        |
+------------------------------------+-------------------+-------------------------------+
| ``[+afaik]{.long}``                | ``\acl{afaik}``   | as far as I know              |
+------------------------------------+-------------------+-------------------------------+
| ``[+afaik]{.long .plural}``        | ``\aclp{afaik}``  | as far as I knows             |
+------------------------------------+-------------------+-------------------------------+
| ``[+afaik]{.full}``                | ``\acf{afaik}``   | as far as I know (AFAIK)      |
+------------------------------------+-------------------+-------------------------------+
| ``[+afaik]{.full .plural}``        | ``\acfp{afaik}``  | as far as I knows (AFAIKs)    |
+------------------------------------+-------------------+-------------------------------+
| ``[+afaik]{.short .caps}``         | ``\Acs{afaik}``   | AFAIK                         |
+------------------------------------+-------------------+-------------------------------+
| ``[+afaik]{.short .plural .caps}`` | ``\Acsp{afaik}``  | AFAIKs                        |
+------------------------------------+-------------------+-------------------------------+
| ``[+afaik]{.long .caps}``          | ``\Acl{afaik}``   | As far as I know              |
+------------------------------------+-------------------+-------------------------------+
| ``[+afaik]{.long .plural .caps}``  | ``\Aclp{afaik}``  | As far as I knows             |
+------------------------------------+-------------------+-------------------------------+
| ``[+afaik]{.full .caps}``          | ``\Acf{afaik}``   | As far as I know (AFAIK)      |
+------------------------------------+-------------------+-------------------------------+
| ``[+afaik]{.full .plural .caps}``  | ``\Acfp{afaik}``  | As far as I knows (AFAIKs)    |
+------------------------------------+-------------------+-------------------------------+

Additionally, one can specify the acronym with ``*`` after the ``+``.
This sets the “starred” version of the LaTeX macro.  In the LaTeX
output, this places a ``*`` after the macro but before the opening
``{``.  Per the ``acro`` documentation, this indicates “don't count as
usage.”  Therefore, in the plain text output the rules are:

1.  Every usage respects the “full,” “short,” or “long” designation.
2.  Usages before the first one that “counts” are expanded to the full
    form by default.
3.  The first usage that “counts” is respected as the first usage and
    expanded as full by default.
4.  All usages after the first usage are expanded to the short form by
    default.

List of Acronyms
^^^^^^^^^^^^^^^^

A list of acronyms used can be generated by placing a div or header with
the id ``acronyms`` in the desired location

.. code-block::

    ::: {#acronyms}
    :::

or

.. code-block::

    last paragraph…

    # Acronyms

This syntax mimics that used by Pandoc to place the bibliography;
however, the list of acronyms is not printed by default.

In the LaTeX output, the div or header is replaced with
``\printacronyms`` with the following options:

-   ``name``: The text of the header (header version only).
-   ``sort``: The value of the ``sort`` attribute (``true`` or
    ``false``) indicating if the acronyms should be sorted.
-   ``level``: The desired section level for the title (plain text
    output for div version only).

In the plain text output, the div or header is replaced with a bulleted
list of acronyms in the ``description`` style of ``acro``.  For the
header style, the list is placed under a heading of the appropriate
level using the header’s text.  For the div style, the list is created
under a new level 1 header with the text “Acronyms.”  The list is sorted
(default) or not based on the ``sort`` attribute of the div or header.

Full and Single Use Forms
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``acro`` package accepts the ``first-style`` option which sets the
form of the first and full usages of an acronym.  The valid options are:
``long-short`` (default), ``short-long``, ``long`` , ``short``, and
``footnote``.  For the LaTeX output, this option is passed to
``\acsetup``.  For all other outputs, the filter respects the
selected style except for ``footnote`` which is not supported.

The default behavior is to typeset a single use of an acronym using the
first usage.  However, this can be changed using the ``single`` option.
Setting this to true typesets a single usage using the style passed to
the ``single-style`` option which accepts the same styles as
``first-style`` but defaults to ``long``.  The single option can also be
set to an integer which sets the number of non-starred times an acronym
must be used before it is considered a “single” use.  If the use goes
above this value, the first typesetting reverts to the usual method.
Setting ``single=true`` is equivalent to ``single=1``.

Output Format Notes
-------------------

LaTeX
^^^^^

The acronyms definitions in the metadata are transformed to
``\DeclareAcronym`` commands and are added to the ``header-includes``
metadata field after ``\usepackage{acro}`` and the ``\acsetup`` command.
These are entered as raw LaTeX Inlines.  The running text markup is
translated to the appropriate ``acro`` macro as described in the above
table.

