(IPFS)=
# IPFS

The ORCESTRA data is made accessible via the InterPlanetary File System ([IPFS](https://docs.ipfs.tech/concepts/what-is-ipfs/)).
IPFS is a modular suite of protocols for identifying, transferring and accessing data, designed from the ground up with the principles of content addressing and peer-to-peer networking.
Because IPFS is open-source, there are multiple implementations of IPFS.
While IPFS has more than one use case, its main use case is for publishing data (files, directories, websites, etc.) in a decentralised fashion.
See also [what is IPFS?](https://docs.ipfs.tech/concepts/what-is-ipfs/).

## IPFS@ORCESTRA

We run the [**ORCESTRA Data Browser**](https://browser.orcestra-campaign.org) for finding ORCESTRA datasets on IPFS.

```{admonition} Historic note
:class: tip

We started using IPFS during the field campaign to share data locally in an efficient way.
Initially, we used `ipns://latest.orcestra-campaign.org` to list the most recent version of each dataset (see also [explanatory slides presented in the field](https://orcestra-campaign.github.io/ipfs_intro/#/title-slide)).
For most datasets, we now graduated from this approach and access through the **browser should be preferred**.
```

## Accessing data with IPFS

To obtain data from the IPFS network, you need access to an [IPFS Gateway](https://docs.ipfs.tech/concepts/ipfs-gateway).
There are multiple options available.

```{margin} On Levante
On DKRZ's **Levante** supercomputer (and probably some other machines), `IPFS_GATEWAY` is pre-defined for you, so you **don't have to care** about a gateway yourself.
```

```````{tab-set}
``````{tab-item} Local gateway

By far, the **best option** is to run a local gateway on your machine yourself.
The easiest way to do so, is to install [IPFS Desktop](https://docs.ipfs.tech/install/ipfs-desktop/), which provides a graphical user interface and runs a [Kubo daemon](https://docs.ipfs.tech/install/command-line/) in the background.


* ✅ retrieves content from any peer (i.e. the fastest responding or nearby ones)
* ✅ no single point of failure
* ✅ local caching of content (using the same dataset twice is effectively a local access)
* ✅ best performance
* ✅ access to all of IPFS
* ✅ access to data you've created & pinned yourself
* ❌ additional software to install

``````
``````{tab-item} ORCESTRA gateway

Only if you are **unable** to install software on your machine (e.g. work laptop), you can configure IPFS to use the ORCESTRA gateway by setting the `IPFS_GATEWAY` environment variable to `https://ipfs.orcestra-campaign.org`:

`````{tab-set}
````{tab-item} bash
```bash
export IPFS_GATEWAY=https://ipfs.orcestra-campaign.org
```
````

````{tab-item} Python
```python
import os
os.environ["IPFS_GATEWAY"] = "https://ipfs.orcestra-campaign.org"
```
````
`````
* ✅ easy to set up
* ✅ server is operated by ORCESTRA community
* 🤔 only serves data from ORCESTRA pinlist (**not** all of IPFS)
* ❌ relies on a single server, which may be offline
* ❌ little local caching
* ❌ usually much slower than local gateway

``````
``````{tab-item} Public gateway

If the ORCESTRA gateway doesn't work for you, you may also use the public HTTPS gateway `https://ipfs.io` instead.

`````{tab-set}
````{tab-item} bash
```bash
export IPFS_GATEWAY=https://ipfs.io
```
````

````{tab-item} Python
```python
import os
os.environ["IPFS_GATEWAY"] = "https://ipfs.io"
```
````
`````

* ✅ easy to set up
* ✅ access to all of IPFS (if reachable from the public internet)
* ✅ redundant cluster of servers
* ❌ operated voluntarily with no guarantees on availability or performance
* ❌ little local caching
* ❌ blocked on some corporate networks
* ❌ usually much slower than local gateway

``````
```````

(access-python)=
### Accessing data through Python

If you want to access the ORCESTRA data using Python, you will need to install the [`ipfsspec>=0.6.0`](http://pypi.org/project/ipfsspec/) package.
It is essential to install `ipfsspec` using pip, the version provided via `conda-forge` is outdated and **broken**.

You can check that your setup is complete by running the following python snippet, which will load the BAHAMAS Quick Look data for the ORCESTRA campaign:
```py
import xarray as xr

ds = xr.open_dataset("ipfs://bafybeiadmnra665v3yflqz7ekjq3sgzt2bpb2ytz4dsu34ggf3gxd2nn5m", engine="zarr")
```

## Adding to the ORCESTRA data collection

Adding to the ORCESTRA data collection involves a few steps, each of which gradually provide more functionality, so depending on your use case, you may want to use only some of the steps.

1. We aim for [analysis-ready datasets](dc-analysis-ready) to improve accessibility. It's generally easier to cut datasets than to glue them, so it's best to provide large, concatenated datasets (e.g. not one per day etc...). The datasets should follow the [](attribute-convention) and should be written as [Zarr](https://zarr.dev/).
2. [Add the dataset to IPFS](add-to-ipfs). This will return a {term}`CID`, which can immediately be used to open the dataset (e.g. [in Python](access-python) or in the browser). It's a good idea to have a peek at the browser landing page at this stage to identify data or metadata issues, and cycle back to step 1 in case of problems.
3. [](increase-retrievability), such that more people get reliable access.
4. Add your {term}`CID` to the [ORCESTRA pin list](orcestra-pin-list): {term}`CID`s in the pin list will be automatically pinned on multiple participating IPFS nodes, and the datasets will be listed in the [](data-browser).

(add-to-ipfs)=
### Adding data to IPFS

```{margin} Kubo Deamon
Kubo can run in daemon mode (i.e. as an IPFS node in the background), this is also what IPFS Desktop does, so if you run a local gateway as written above, you probably are set up already.
If you don't run IPFS Desktop, you can start the daemon using `ipfs daemon`.
```

To add data to IPFS, you need to install and run a local IPFS client, e.g. [kubo](https://docs.ipfs.tech/install/command-line/).
Kubo provides a command line interface (e.g. `ipfs add`), which we use below to add content to the node running in the background.

The following options are recommended when adding data:
```sh
ipfs add --recursive --hidden --raw-leaves --chunker=size-1048576 --quieter </path/to/data>
```

This command will add trees recursively and will also include hidden files, which is important for Zarr v2, as crucial metadata is stored in hidden files (e.g. `.zarray`).
The `--raw-leaves` option tells IPFS to store data blocks on the lowest level in a raw format instead of wrapping them in more complex [IPLD](https://ipld.io) data types.
This doesn't have any direct effect on the user side, but allows for easier reuse of individual data blocks when handling the data on the backend.
The `--chunker=size-1048576` increases the maximum internal block size from the default of 256KB to 1MB (which is the maximum safely transferrable by IPFS). This also doesn't have a direct user-visible effect, but will improve performance.

The command returns a Content Identifier ({term}`CID`) of your data, which you can then use to access and share the data.

(increase-retrievability)=
### Increase CID retrievability

Once you have added new data to IPFS, the content may only be present on your local computer.
To add it to the ORCESTRA collection, others (including public ORCESTRA IPFS nodes) must be able to reliably access the content.
While in theory others could access the content from your computer, it might be behind a firewall, limiting access.
As we currently don't operate an ORCESTRA {term}`pinning service`, the current best option might be to create a {term}`CAR` and share this until the data is in the [ORCESTRA pin list](orcestra-pin-list).
Alternatively you can of course run a well-connected node yourself, or use a commercial {term}`pinning service`.

(orcestra-pin-list)=
### The ORCESTRA pin list

To further improve data availability and ensure redundancy, we [pin](https://docs.ipfs.tech/how-to/pin-files/) data on multiple nodes (for example, nodes operated at DKRZ).
For this to work, all participating nodes need to agree on the set of CIDs that should be stored.
We maintain this set in a **pin list** — a list of all datasets that the ORCESTRA community wants to keep available.

The pin list is maintained in the [`ipfs_tools`](https://github.com/orcestra-campaign/ipfs_tools) repository, where anyone can propose new CIDs via a pull request.
Several IPFS nodes automatically fetch the latest version of the pin list and pin the corresponding data, increasing both **redundancy** and **availability**.

CIDs which are listed in the pin list **and** follow the [](attribute-convention) will subsequently be listed in the [](data-browser).
