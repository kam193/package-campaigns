# Package Campaigns Collection

This is a collection of campaigns targeting package ecosystems, currently limited to PyPI.

Currently, data are sourced only from what I've seen in my analysing lab and are exported here periodically. The classification is mostly arbitrary and may not follow any strict criteria.

Published are information about campaigns as well as list of identified package names. This repository does not (and will not) contain the source code of mentioned packages.

## Repository Structure

* `pypi/` - automatically extracted data about packages from PyPI ecosystem.
  * `campaigns/<category>` - list of campaigns in a category, each one as JSON file
  * `packages/<category>/json/` - alternative structure with basic package info as JSON files.
 
## Campaign Categories

Currently, I publish following categories:

* _malicious_ - the campaign has clearly malicious intent, like infostealers;
* _spam_ - advertisements, spam packages etc.;
* _pentest_ - packages with high confidence of being created for a pentest;
* _probably_pentest_ - packages looking like typical pentest packages, but also anything that looks like testing, exploring pre-prepared kits & co, with clearly low-harm possibilities.

## Disclaimer
Data are presented as-is without any guarantee. Detection, classification, analyse & co. are done as a hobby activity, you use the information at your own risk. There are possible mistakes or highly opinionated classifications.
