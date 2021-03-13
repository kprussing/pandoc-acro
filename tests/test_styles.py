import random

import panflute


def test_first_style() -> None:
    """Check the first use style."""
    TEXT = "\n".join(["---",
                      "acronyms:",
                      "  mwe:",
                      "    short: short",
                      "    long: long",
                      "  options:",
                      "    first-style: {style}",
                      "...",
                      "+mwe",
                      "[+mwe]{{.full}}"
                      ])
    for style, output in (("long-short", "long (short)"),
                          ("short-long", "short (long)"),
                          ("long", "long"),
                          ("short", "short")
                          ):
        expected = f"{output} {output}"
        result = panflute.convert_text(TEXT.format(style=style),
                                       output_format="markdown",
                                       extra_args=["-F", "pandoc-acro"])
        assert len(result) == len(expected)
        assert result == expected


def test_single_style_no_single() -> None:
    """Check the single style is ignored without ``single``."""
    TEXT = "\n".join(["---",
                      "acronyms:",
                      "  mwe:",
                      "    short: short",
                      "    long: long",
                      "  options:",
                      "    single-style: {style}",
                      "...",
                      "+mwe",
                      ])
    expected = "long (short)"
    for style in ("long-short", "short-long", "long", "short"):
        result = panflute.convert_text(TEXT.format(style=style),
                                       output_format="markdown",
                                       extra_args=["-F", "pandoc-acro"])
        assert len(result) == len(expected)
        assert result == expected


def test_single_style_with_single() -> None:
    """Check the single use style."""
    TEXT = "\n".join(["---",
                      "acronyms:",
                      "  mwe:",
                      "    short: short",
                      "    long: long",
                      "  options:",
                      "    single-style: {style}",
                      "    single: true",
                      "...",
                      "+mwe",
                      ])
    for style, expected in (("long-short", "long (short)"),
                            ("short-long", "short (long)"),
                            ("long", "long"),
                            ("short", "short")
                            ):
        result = panflute.convert_text(TEXT.format(style=style),
                                       output_format="markdown",
                                       extra_args=["-F", "pandoc-acro"])
        assert len(result) == len(expected)
        assert result == expected


def test_single_style_with_count() -> None:
    """Check setting ``single`` to a number works."""
    TEXT = "\n".join(["---",
                      "acronyms:",
                      "  mwe:",
                      "    short: short",
                      "    long: long",
                      "  options:",
                      "    single-style: {style}",
                      "    single: {single}",
                      "...",
                      ])
    for _ in range(10):
        style, first = random.choice([("long-short", "long (short)"),
                                      ("short-long", "short (long)"),
                                      ("long", "long"),
                                      ("short", "short")
                                      ])
        single = random.choice(range(1, 6))
        uses = random.choice(range(1, 11))
        text = TEXT.format(style=style, single=single)
        result = panflute.convert_text(text + "\n" +
                                       " ".join(["+mwe"] * uses),
                                       output_format="markdown",
                                       extra_args=["-F", "pandoc-acro"])
        if uses > single:
            expected = " ".join(
                ["long (short)"] + ["short" for _ in range(1, uses)]
            )
        else:
            expected = " ".join([first for _ in range(uses)])

        assert len(result) == len(expected)
        assert result == expected
