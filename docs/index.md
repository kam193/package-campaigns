---
title: Start
---
# Malicious & suspicious packages

This is a collection of campaigns of malicious, suspicious and other unwanted or
risky packages, that target [Python Package Index](https://pypi.org) ecosystem
(more may come in the future).

Data are sourced (with rare exceptions) from what see in my analysing lab,
 and are exported here periodically. The classification is mostly arbitrary and
 may not follow any strict criteria.

All published packages have been manually checked. See some
[statistics for PyPI here](./pypi/index.md).

## Content

Packages are grouped in campaigns, which describe the activity. Usually,
there is no additional description on the package level. As sometimes the
behaviour changes over time, the campaign description may not describe exactly
the package behaviour.

The current focus is on packages that are created for malicious purposes, and
not on hacked versions of legitimate packages. You should generally assume all
versions to be affected. Except of older packages, I now try to list affected
versions. They are also automatically updates.

## Malicioussnes classification

Each campaing has assigned a category, which describe how "malicious" I
assessed the given campaign and how convinced I was about it. For instance,
packages that do just a basic installation check or collect basic information
(and have no other purpose, commonly used for dependency confusion checks)
will fall into _probably pentest_ category, indicating low harmfullness.
Note that such an activity is anyway forbidden by PyPI's [Acceptable Use Policy](https://policies.python.org/pypi.org/Acceptable-Use-Policy/).

For a definition of a _malicious package_, see [explanation in OpenSSF project](https://github.com/ossf/malicious-packages?tab=readme-ov-file#definition-of-a-malicious-package).

## Using data to secure your environment

You can secure your environment by using one of machine-readable
formats available in the [GitHub repository](https://github.com/kam193/package-campaigns):
the custom JSON or [OSV Schema](https://ossf.github.io/osv-schema/) to build
custom integration and leverage all provided data, including those with lower confidence,
like _highly suspisicous_ category.

Three categories (_malicious_, _probably pentest_ and _pentest_) are also
automatically ingested into [OpenSSF Malicious Packages](https://github.com/ossf/malicious-packages)
project, and from there into the main [OSV.dev](https://osv.dev/) database. You
can use one of their [official scanners](https://osv.dev/#use-vulnerability-scanner)
or [third party tools](https://google.github.io/osv.dev/third-party/) to easy
scan your dependencies. Note there is a delay between publishing data here
and injesting them into OSV.dev.

## Disclaimer

Data are presented as-is without any guarantee. Detection, classification,
analyse & co. are done as a hobby activity, you use the information at your own
risk. There are possible mistakes or highly opinionated classifications.
