# Attribute Convention for ORCESTRA

## Goals

The goal of this convention is to define a minimal set of global attributes for datasets to provide the following functionalities:

* Automatically retrieve contact information for any dataset
* Create a summary table with all datasets and some key metadata

For additional metadata not covered by this convention we recommend following the [CF](https://cfconventions.org) and [ACDD](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3) conventions.

## Global attributes

The following section lists a selection of required and recommended global attributes for datasets.
The required attributes are essential for the [ORCESTRA Data Browser](https://browser.orcestra-campaign.org) to render proper landing pages.

If an attribute is undefined, it is recommended not to set it instead of using empty strings.

### Required

Key | Value
--- | ---
`title` | Short phrase or sentence describing the dataset
`summary` | Paragraph describing the dataset
`creator_name` | Comma-separated list of names
`creator_email` | Comma-separated list of emails
`license` | [SPDX-ID](https://spdx.org/licenses/)

### Recommended

Key | Value
--- | ---
`project` | Comma-separated list of projects (see below)
`platform` | Name of the platform that supported the sensor (see below)
`source` | Method of production of the original data (e.g. "radar", "radiometer", "CTD")
`history` | Audit trail for modifications to the original data
`references` | Comma-separated list of URL/DOI to extended information <br/>Published or web-based references that describe the data or methods used to produce it.
`keywords` | Comma-separated list of keywords
`processing_level` | A textual description of the processing (or quality control) level of the data.
`institution` | Institution responsible for the dataset
`instrument` | Instrument used to measure the data (may be set in addition to `source`)
`creator_id` | Comma-separated list of identifiers (e.g. ORCID)
`Conventions` | A comma-separated list of the conventions that are followed by the dataset, e.g., 'ACDD-1.3, CF-1.12'.

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
* `INMG`
