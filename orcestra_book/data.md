# Data

ORCESTRA encourages free use and access to its data (see [](data-policy)).
The primary starting point for exploring data is the [**ORCESTRA Data Browser**](https://browser.orcestra-campaign.org).
Data listed in the browser can be accessed through [](IPFS).
Some specific datasets may not (yet) be available in the data bowser, so if you still miss something, you might want to check [alternate locations](data-locations).

(data-browser)=
## Data Browser

The [**ORCESTRA Data Browser**](https://browser.orcestra-campaign.org) retrieves all information on-demand from the metadata in the datasets. In order for the data browser to correctly identify and parse relevant information, we have created the [](attribute-convention).

````{admonition} about IPFS
:class: tip

The primary data distribution method for ORCESTRA is {term}`IPFS`.
In short, any data is identified by a content identifier ({term}`CID`), which identifies (immutable) content in a verifiable way, but doesn't specify the data location.
IPFS adds a mechanism to locate and retrieve the date, based on only the CID.
This means, the following code is sufficient to locate, retrieve, verify and open a dataset based on the CID:
```python
xr.open_dataset("ipfs://bafybeiesyutuduzqwvu4ydn7ktihjljicywxeth6wtgd5zi4ynxzqngx4m", engine="zarr")
```
In this case, `bafy...4m` is the CID.
To learn more about setting up and using IPFS in the context of ORCESTRA, [continue here](IPFS).
````

(data-locations)=
## Data Locations

| Name & Link | Description |
| --- | --- |
| [**ORCESTRA Data Browser**](https://browser.orcestra-campaign.org) | Main entry point for ORCESTRA data. |
| [ipns://latest.orcestra-campaign.org](https://latest.orcestra-campaign.org/) | (*deprecated*) IPFS filesystem tree, established during the campaign. A loosely organized collection of files, is being replaced entirely be the [](data-browser). |
| [MAESTRO Catalog](https://maestro.aeris-data.fr/catalog/) | Datasets from [](maestro) sub-campaign. |
| [MAESTRO Thredds Catalog](https://thredds-x.ipsl.fr/thredds/catalog/MAESTRO/catalog.html) | Loosely organized collection of files from [](maestro) sub-campaign. Also includes several forecasts and satellite data. |
| [Marine Data](https://marine-data.de/expeditions/M203) | Additional data for [](bowtie). |
| [EarthCARE Data](https://earth.esa.int/eogateway/missions/earthcare/data) | [](earthcare) data is provided at [ESA](https://esa.int).
| [TCO Data](https://tcodata.mpimet.mpg.de/) | Datasets from the Barbados Cloud Observatory ([](bco)) (TCO Data offers long timeseries, ORCESTRA data can be retrieved using subsetting). |
| [Cloudnet Site Mindelo](https://cloudnet.fmi.fi/search/visualizations?site=mindelo) | Data from the CVAO Cloudnet site ([](clarinet) sub-campaign). |
| limited area [ICON simulations](lam.md) | _requires [Levante](https://docs.dkrz.de/doc/levante/index.html) access_ |
