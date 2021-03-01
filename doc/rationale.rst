:author: Keith F. Prussing
:date: 2021-02-07
:template: post.html

Rationale Behind the Filter
===========================

The obvious question is why make yet another acronym filter for Pandoc_
when we already have pandoc-acronyms_, pandoc-abbreviations_, and
pandoc-ac_?  Well for a start, I'm not really wild about their
interfaces.  Either the inline mark-up was too bulky for simple (i.e.
the most common) cases, the database format was unpleasant (JSON input
or not nested), or the output format was limited to either always
managing the expansion or only outputting LaTeX  In particular, my goal
was to cleanly translate a simple markup to LaTeX output using the
|acro|_ package, but I also wanted to actually have the expansion in
other source formats.

The YAML metadata provides a way to create a named database
(``acronyms``) with entries that contain key/value mappings just like
|acro|_'s ``\DeclareAcronym``.  Further, using ``+`` like pandoc-xnos_
makes the source clear to read and understand in the simple case, but
the native span allows one to customize the acronym expansion like
alternate macros ``\acs``, ``\acf``, ``\acl``, and friends.  The final
syntax winds up more verbose than the raw LaTeX version, but the
conversion to alternate output formats (like Word) becomes possible.
I'm not sure how often I'll really get to use this filter since I prefer
writing with the full power of LaTeX, but it might come in handy for
rough first drafts while I work with colleagues that need to work with
Word.

Another reason to do this was to play around with testing frameworks and
document generation.  I never really get time on a project to properly
set everything up (beyond a fairly standard ``setup.py``).  Since this
is primarily for myself, I get to spend time actually seeing how to get
Sphinx_ setup and to really play with nox_ to figure out how to
integrate linters, automatic regression testing, and other niceties into
my Python projects along with testing against multiple Python versions.
Maybe I'll even get to the point where it's stable enough to send to
PyPI_.  We'll see.

I hope the actual tool is useful.  But worst case scenario, I could
always fall back on the `Cranky Developer Manifesto`_ :-).

.. |acro| replace:: ``acro``
.. _acro: https://ctan.org/pkg/acro
.. _Cranky Developer Manifesto: https://dev.to/codemouse92/the-cranky-developer-manifesto--24km
.. _Pandoc: https://pandoc.org
.. _pandoc-ac: https://github.com/Enet4/pandoc-ac
.. _pandoc-acronyms: https://pypi.org/project/pandoc-acronyms/
.. _pandoc-abbreviations: https://github.com/scokobro/pandoc-abbreviations
.. _pandoc-xnos: https://github.com/tomduck/pandoc-xnos
.. _PyPI: https://pypi.org
.. _nox: xhttps://nox.thea.codes/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/index.html
