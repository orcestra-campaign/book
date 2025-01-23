# Attribute Convention for ORCESTRA

## Goals

The goal of this convention is to define a minimal set of global attributes for datasets to provide the following functionalities:

* Automatically retrieve contact information for any dataset
* Create a summary table with all datasets and some key metadata

## Global attributes

Key | Value
--- | ---
`title` | Short phrase or sentence describing the dataset
`summary` | Paragraph describing the dataset
`creator_name` | Comma-separated list of names
`creator_email` | Comma-separated list of emails
`project` | Comma-separated list of projects (see below)
`platform` | Name of the platform that supported the sensor (see below)
`source` | Method of production of the original data (e.g. "radar", "radiometer", "CTD")
`history` | Audit trail for modifications to the original data
`license` | [SPDX-ID](https://spdx.org/licenses/)
`references` | Comma-separated list of URL/DOI to extended information <br/>Published or web-based references that describe the data or methods used to produce it.
`keywords` | Comma-separated list of keywords

Undefined attributes **should not** be set.

For additional metadata we encourage to follow [CF](https://cfconventions.org) and [ACDD](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3) conventions

## Valid `project` values

* `ORCESTRA`
* `BOW-TIE`
* `CELLO`
* `CLARINET`
* `MAESTRO`
* `PERCUSION`
* `PICCOLO`
* `SCORE`
* `STRINQS`

## Valid `platform` values

* `EarthCARE`
* `HALO`
* `ATR-42`
* `INCAS KingAir`
* `BCO`
* `CVAO`
* `RV METEOR`
