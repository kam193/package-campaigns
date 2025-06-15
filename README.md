# Package Campaigns Collection

This is a collection of (mostly) malicious campaigns targeting package ecosystems, currently limited to PyPI.

Data are sourced only from what I've seen in my analysing lab and are exported here periodically. The classification is mostly arbitrary and may not follow any strict criteria.

Published are information about campaigns as well as list of identified package names. This repository does not (and will not) contain the source code of mentioned packages.

**Web representation: [bad-packages.kam193.eu](https://bad-packages.kam193.eu/)**

## Repository Structure

* `pypi/` - automatically extracted data about packages from PyPI ecosystem.
  * `campaigns/<category>` - list of campaigns in a category, each one as JSON file
  * `packages/<category>/json/` - alternative structure with basic package info as JSON files.

## Campaign Categories

Currently, I publish following categories:

* _malicious_ - the campaign has clearly malicious intent, like infostealers;
* _spam_ - advertisements, spam packages etc.;
* _pentest_ - packages with high confidence of being created for a pentest (actually used rarerly, with the _probably_pentest_ taking most of pentesting packages);
* _probably_pentest_ - packages looking like typical pentest packages, but also anything that looks like testing, exploring pre-prepared kits, **research** & co, with clearly low-harm possibilities;
* _highly_suspicious_ - packages that are likely malicious, but due to the obfuscation level, lack of time or clear indicators it's hard to say what exactly they do; the highest risk of false positives.
* _high_risk_hacking_tools_ - packages that are very likely to be used to build or as part of a malware, in most cases. They are **not** malicious on their own, but are quite a good indicator of someting
  suspicious.

In my opinion, you should not have any of those packages in your environment.

## Disclaimer
Data are presented as-is without any guarantee. Detection, classification, analyse & co. are done as a hobby activity, you use the information at your own risk. There are possible mistakes or highly opinionated classifications.

## License

You're free to use data exposed here as long as you attribute the source. 
