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
`featureType` | Type of sampling geometry according to [CF conventions](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html#_features_and_feature_types)
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
* `MSG`

## Annotating datasets without native metadata

Our attribute convention is based on the use of global attributes.
However, not all data formats support metadata natively (e.g., CSV, PDF).
While we strongly recommend converting data to formats that support attributes, a fallback mechanism is provided for externally annotating data of any format.

Each directory containing a file named `dataset_meta.yaml` is considered a dataset.
This [YAML](https://yaml.org/spec/) file **must** include an `attributes` block that defines the dataset’s global attributes.
All attributes **must** comply with the ORCESTRA Attribute Convention.

The file **may** also include an optional `extent` block, used to provide information that would otherwise be derived from dataset coordinates.
Currently, the `extent` block supports the following keys:

Key | Type | Description
--- | --- | ---
`temporal` | [string] | Temporal extent in [ISO 8601 format](https://www.iso.org/iso-8601-date-and-time-format.html)
`spatial` | [float] | Geospatial extent defined by a [GeoJSON Bounding Box](https://datatracker.ietf.org/doc/html/rfc7946#section-5)

**Example:**

```yaml
attributes:
  title: BEACH dropsonde dataset (Level 3)
  summary: This dataset is the Level 3 BEACH dataset. It contains quality controlled
    dropsonde data from the ORCESTRA field campaign with a common altitude dimension.
  creator_name: Helene Gloeckner, Theresa Mieslinger, Nina Robbins
  creator_email: helene.gloeckner@mpimet.mpg.de, theresa.mieslinger@mpimet.mpg.de, nina.robbins@mpimet.mpg.de
  license: CC-BY-4.0
  featureType: trajectoryProfile
  history: Level 1 ASPEN processing with Aspen V4.0.4
  keywords: ORCESTRA, BEACH, Sounding, Dropsondes, Atmospheric Profiles
  platform: HALO
  project: ORCESTRA, PERCUSION, MAESTRO
  references: https://github.com/atmdrops/pydropsonde
  source: dropsondes
extent:
  temporal: ["2024-08-09T14:26:37", "2024-09-28T19:30:47"]
  spatial: [-59.45647812, 1.29273319, -19.62099838, 22.03603554]
```
