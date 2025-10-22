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


```{admonition} Advantages
:class: tip

A local gateway automatically retrieves and verifies content from the most responsive peers, and still can provide access to the data if any particular server fails (no single point of failure).
This option also caches content locally, so accessing the same data multiple times won't require additional network transfers.
```

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

```{admonition} Disadvantages
:class: warning

The downside of using the ORCESTRA gateway are, that you rely on a single server, you won't have access to non-orcestra datasets on IPFS and you won't benefit from local caching.
```

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
```{admonition} Disadvantages
:class: warning

While the public gateway provides access to all of IPFS, it is operated voluntarily and doesn't provide any availability guarantees. You also won't benefit from local caching like you'd have when running a local node, and on some networks, the public IPFS gateways are blocked.
```

``````
```````

## Accessing data through Python

If you want to access the ORCESTRA data using Python, you will need to install the [`ipfsspec>=0.6.0`](http://pypi.org/project/ipfsspec/) package.
It is essential to install `ipfsspec` using pip, the version provided via `conda-forge` is outdated and **broken**.

You can check that your setup is complete by running the following python snippet, which will load the BAHAMAS Quick Look data for the ORCESTRA campaign:
```py
import xarray as xr

ds = xr.open_dataset("ipfs://bafybeiadmnra665v3yflqz7ekjq3sgzt2bpb2ytz4dsu34ggf3gxd2nn5m", engine="zarr")
```

## Adding data to IPFS

To add data to IPFS, you need to install and run a local IPFS client, e.g. [kubo](https://docs.ipfs.tech/install/command-line/).
The local client will usually start a local gateway and connect to it.
You can then add data to your local IPFS node using the `ipfs add` command.

The following options are recommended when adding data:
```sh
ipfs add --recursive --hidden --raw-leaves --chunker=size-1048576 --quieter </path/to/data>
```
This command will add trees recursively and will also include hidden files, which is important for Zarr v2, as crucial metadata is stored in hidden files (e.g. `.zarray`).
The `--raw-leaves` option tells IPFS to store data blocks on the lowest level in a raw format instead of wrapping them in more complex [IPLD](https://ipld.io) data types.
This doesn't have any direct effect on the user side, but allows for easier reuse of individual data blocks when handling the data on the backend.
The `--chunker=size-1048576` increases the maximum internal block size from the default of 256KB to 1MB (which is the maximum safely transferrable by IPFS). This also doesn't have a direct user-visible effect, but will improve performance.

The command returns a Content Identifier (CID) of your data, which you can then use to access and share the data.
