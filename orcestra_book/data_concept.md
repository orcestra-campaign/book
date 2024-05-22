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

## Implementation

:::{caution}
This section is currently in exploratory stage. We aim to show options and their respective advantages and disatvantages. We should try to converge to a more concrete implementation plan until the start of the campaign.
:::
### Catalog

We aim to implement the **dataset list** from the requirements in form of a **data catalog**.
A data catalog in our sense is a somewhat formalized way of listing datasets and a method to access those datasets.
A catalog is machine readable and supports the goal of dataset accessibility.

::::{grid} 1 1 2 2

:::{grid-item-card} [Intake](https://intake.readthedocs.io)
Tool for reading data, from Python ecosystem.

* ✅ known and tested in EUREC4A and AC3
* ✅ easy to create
* ✅ compatible with any kind of data
* ❌ limited to Python
* ❌ unstable format (Intake 2 broke a lot of things)
* 🤔 has room for creative hacks
:::

:::{grid-item-card} [STAC](https://stacspec.org/)

SpatioTemporal Asset Catalogs, the STAC specification is a common language to describe geospatial information.

* ✅ stable format
* ✅ [integrations for multiple languages](https://stacspec.org/en/about/tools-resources/) exist
* ✅ can be used with Intake
* ✅ common set of earth observation related metadata is defined
* ❌ more complicated to create (but tools exist)
* ❌ can only be used for 
:::
::::

In any case, the catalog should be accessible though a well-known public URL, such that users always know where to start.
We suggest either `https://data.orcestra-campaign.org/catalog.yaml` or `https://data.orcestra-campaign.org/catalog.json`, depending on whether Intake or STAC will be chosen.

We may want to use Continuous Integration tools to automatically build the actual catalog based on simpler source input files. This might be particularly relevant if we opt for STAC catalogs, as they require providing spatial and temporal extend for every dataset. We might want to automatically extract this information from the actual datasets if they follow e.g. CF-Conventions, thus simplifying catalog creation and improving consistency.

### Storage and Access

While the Catalog provides a unified access method to all the datasets, mostly independent of the underlying storage and access methods, the particular choices in this section will have an influence on practical data accessibility and maintenance effort.
We can (and likely will have to) support multiple underlying storage and access methods.
This section tries to briefly cover the advantages and disadvantages of those methods.

::::{grid} 1 1 2 2
:::{grid-item-card} HTTP / Object Store
E.g. [Swift](https://docs.openstack.org/swift/train/api/object_api_v1_overview.html), [S3](https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html) or just a static HTTP server.

* ✅ HTTP as access protocol
* ✅ compatible with about everything
* ❌ prone to [link rot](https://en.wikipedia.org/wiki/Link_rot)
* ❌ single point of failure
* ❌ in general: no guarantees about data integrity or persistence
:::

:::{grid-item-card} DOI repo
This includes e.g. [Pangea](https://pangaea.de), [Aeris](https://www.aeris-data.fr), [Zenodo](https://zenodo.org), etc...

* ✅ DOI providers must state that they keep data available for a while
* ❌ providing all required information may be a burden
* ❌ DOI does not provide direct access to data thus we must fall back to direct HTTP links, effectively bypassing the DOI
* ❌ single point of failure
:::

:::{grid-item-card} NextCloud / OwnCloud
* ✅ easy to upload
* ✅ can be installed on-site at the campaign
* ❌ access performance may be sub-optimal
* ❌ single point of failure
* 🤔 easy way to create user accounts
:::

:::{grid-item-card} [IPFS](https://ipfs.tech)
* ✅ can be installed on-site at the campaign
* ✅ distributed, i.e. we can have multiple copies at different location (including local)
* ✅ very fast access if data is cached locally
* ✅ tracking data changes is easy due to the [Merkle Tree](https://en.wikipedia.org/wiki/Merkle_tree) structure
* ❌ requires setting up an [IPFS node](https://docs.ipfs.tech/install/ipfs-desktop/) on (or close to) the accessing machine for reasonable performance
:::

:::{grid-item-card} [OPeNDAP](https://www.opendap.org)
* ✅ minimizes data transfer
* ❌ very hard to cache
* ❌ very hard to track changes
* ❌ often poor performance due to high server load
* ❌ many problematic data types
:::
::::

### Tracking Progress
Some form of a second list of *to-be-created* datasets in advance is likely helpful to track progress (e.g. as for [(AC)<sup>3</sup> campaign](https://igmk.github.io/how_to_ac3airborne/datasets.html#p5))

### Good Datasets

The implementation builds on top of [HowTo EUREC4A](https://howto.eurec4a.eu/) and [(AC)<sup>3</sup> Airborne](https://igmk.github.io/how_to_ac3airborne/intro.html).

* few large datasets are better than many small datasets
  * daily datasets are nice during creation, but <br/> full-campaign datasets are easier afterwards
  * (large) datasets benefit from good chunking
* Some datatypes [are problematic](https://howto.eurec4a.eu/netcdf_datatypes.html), you **should not** use these datatypes.


### Special considerations on-site during the field campaign

It would be great if we can fill and access the data catalog already during the field campaign.
This might however require some special considerations, as we generally can't rely on a very fast internet connection.

* We may use links to local copies of the datasets in the catalog
* If using IPFS, things might work out automatically as IPFS would discover and access local copies.
