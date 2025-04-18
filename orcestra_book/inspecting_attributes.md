---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Inspecting dataset attributes

The datasets collected during ORCESTRA follow a common [Attribute Convention](attribute_convention), which means that certain global attributes can be expected to be set.
These can be used by downstream applications to automatically retrieve metadata from a dataset.

The [ORCESTRA Data Browser](https://browser.orcestra-campaign.org), for example, retrieves all necessary information to render a landing page directly from the dataset.
But the global attributes can also be helpful for scientists to get a better overview of a dataset.

```{code-cell} ipython3
from pprint import pprint

import xarray as xr
```

In general, the `attrs` attribute allows access to the global attributes of a dataset.
Here, we print **all** the global attributes of the CTD measurements during the BOW-TIE subcampaign:

```{code-cell} ipython3
ds_ctd = xr.open_dataset("ipfs://bafybeihoghhgi655g7arw2ubtpudbq4c4hpwjlrwghcex3snu7f36imjgq", engine="zarr")
pprint(ds_ctd.attrs)
```

But we can also extract individual keys to extract information that is relevant to us.
This can be used to print standardised log messages when working with different datasets.

```{code-cell} ipython3
pprint(ds_ctd.attrs["title"])
pprint(ds_ctd.attrs["creator_name"])
```

