# Data Concept

We like to see ORCESTRA as **our common** field campaign.
All should be able to use the gathered data.
Together and for mutual benefit.

This page first focusses on the general **goals** we want to achieve, they should reflect general ideas of what we think a useful, practical datasystem should be capable of.
The next section details on **requirements** we derive from the goals, in order to find a good **implementation**, which is described in the third part.

## Goals

The purpose of these goals is to have a well-working environment for data dissemination (both during and post campaign) and to learn from what worked and what didn't work during the EUREC4A field campaign and other previous projects.
The goals are sorted in decreasing priority (i.e. 1 is the most important). We **aim for all of them**, but if we have to cut, we should cut at the end.

1. **a *single* list of existing datasets**<br/>
   We want a common data collection of our field campaign.
   Everyone interested in ORCESTRA should be able to find available datasets.
   For clarity and consistency, there must be exactly one list.
2. **the datasets in list are *accessible***<br/>
   Given someone found a dataset in the list, the dataset should be usable.
   That is, the information in the list must be sufficient for everyone to be able to open the dataset with common tools and little effort.
3. **datasets are *well-formed* and *analysis-ready***<br/>
   Useful datasets are typically written once and read often.
   The overall effort can be reduced if we spend a bit more time on creating the dataset if that facilitates the later use.
4. **incremental backups are possible**<br/>
   We expect that the ORCESTRA data collection is a valuable contribution to our scientific field.
   We should be able to have a backup of this collection.
   Realistically, the list will evolve over time, thus we will have to update any backups incrementally.
5. **datasets are on a shared, distributed system**<br/>
   We want the data system to be use in actual scientific work (not only for "data publication").
   Traditional systems are often too complicated or slow for day-to-day usage.
   A distributed system increases the availability and performance (e.g. due to local caches, redundant servers...), which renders the actual use of own published data convenient, fast and fun.


## Requirements

:::{admonition} About the wording
:class: tip
The use of the words **must**, **must not**, **should**, **should not** and **may** in bold case follows the definition of [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).
:::

### 1. a **single** list of existing datasets

There **must** be one definitive list of all ORCESTRA datasets.
There **must not** be more than one definitive list.
Any datasets which are not part of the list **must not** be called "an ORCESTRA dataset".

* likely not all datasets will be hosted on a single server (this didn't work at all in the past), thus the list **must** be kept somewhere independent of data storage location
    * list **must** be updated when data is added / changed / removed
* likely, the list will not be complete at one point in time
    * we **must** expect that the list changes over time
* in the past, we had problems answering the question of "what's all the campaign data".
  We aim to sidestep this problem by requiring every dataset which should be associated to ORCESTRA to be in this list. The effort to add datasets to the list should be kept low in order not to exclude anyone from making "ORCESTRA datasets".
---

### 2. the datasets in list are **accessible**

```
dataset = get(dataset_list, dataset_identifier)
```

☝️  any dataset can be opened directly by anyone

* The access **must** be testable (e.g. weekly CI).
* The dataset **should** be accessible without credentials.
* The dataset **should** be available publicly as soon as possible (ideally immediately after acquisition).
* The dataset **should** be available publicly not later than one year after the campaign finished. (**TODO:** this point might be better placed in the data policy, we really want something like a "must" here, but in this section this would technically mean that no data can be added after a year, which we also don't want)
* The dataset **must** be available as [`xarray.Dataset`](https://docs.xarray.dev/en/stable/user-guide/data-structures.html#dataset) (it **can** be available in different forms in addition).


:::{tip}
Many formats can be read as an xarray Dataset. This includes e.g. netCDF, zarr, GRIB, CSV, AMES FFI etc..., but it might require supplying an appropriate read routine.
:::

### 3. datasets are **well-formed** and **analysis-ready**

* You **should** stick to well-known formats (e.g. netCDF / zarr). The chosen format **must** be convertible to `xarray.Dataset`, see above.
* You **should** follow standard metadata schemes ([CF-Conventions](http://cfconventions.org/Data/cf-conventions/cf-conventions-1.11/cf-conventions.html))
* You **may** designate data processing levels to help users understand the quality of the provided data. If you provide processing levels, the levels **should** follow the [EOSDIS data processing levels](https://www.earthdata.nasa.gov/engage/open-data-services-and-software/data-information-policy/data-levels) scheme.
* You **should** work with your own **published** datasets.
* Datasets **should** be reviewed across teams.

### 4. incremental backups are possible

*(this section is currently in an early stage)*

* storage location has to provide a method to check if something changed
    * e.g. HTTP ETag, hash of content etc...
* how to handle updates / changes to a dataset?
    * ensure that dataset name changes on storage (e.g. version number, hash ...)
    * list / catalog may point to most recent version

### 5. datasets are on a shared, distributed system

*(this section is currently in an early stage)*

use a distributed storage protocol to make datasets accessible
e.g. [IPFS](https://ipfs.tech), [ONEDATA](https://onedata.org)

*maybe needs more support from computing centers*

### Closing remarks

* One **may** write a data paper to describe datasets that are part of the ORCESTRA data collection. The ORCESTRA data collection and a data paper may benefit mutually:
    * Preparing data for the ORCESTRA data collection may help writing a data paper.
    * Writing a data paper may help preparing data for the ORCESTRA data collection.
