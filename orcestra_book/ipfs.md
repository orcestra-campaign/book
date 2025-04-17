# IPFS

The ORCESTRA data is stored via the InterPlanetary File System [(IPFS)](https://docs.ipfs.tech/concepts/what-is-ipfs/).
IPFS is a modular suite of protocols for organizing and transferring data, designed from the ground up with the principles of content addressing and peer-to-peer networking.
Because IPFS is open-source, there are multiple implementations of IPFS.
While IPFS has more than one use case, its main use case is for publishing data (files, directories, websites, etc.) in a decentralised fashion.
[(*Source*)](https://docs.ipfs.tech/concepts/what-is-ipfs/#defining-ipfs)

## IPFS@ORCESTRA

The latest version of the dataset is available via:

Subsystem | Name/Path
--- | ---
[IPNS](https://docs.ipfs.tech/concepts/ipns/) | `/ipns/latest.orcestra-campaign.org`
HTTP gateway | https://latest.orcestra-campaign.org

You can find an overview presentation about the usage of IPFS during ORCESTRA [here](https://orcestra-campaign.github.io/ipfs_intro/#/title-slide).

## Accessing data with IPFS

To obtain data from the IPFS network, you need access to an [IPFS Gateway](https://docs.ipfs.tech/concepts/ipfs-gateway).

::::{grid} 1 1 2 2
:::{grid-item-card} Local machine
We recommend that you use your own local gateway for faster access and local caching.
The simplest solution is to install [IPFS Desktop](https://docs.ipfs.tech/install/ipfs-desktop/), which provides a graphical user interface and runs a [Kubo daemon](https://docs.ipfs.tech/install/command-line/) in the background.

If you are **unable** to install software on your machine (e.g. work laptop), you can configure IPFS to use the public HTTPS gateway by setting:
```
export IPFS_GATEWAY=https://ipfs.io
```
:::

:::{grid-item-card} High-performance Computer
You should check, whether your HPC centre provides an IPFS gateway (e.g. whether `IPFS_GATEWAY` is set).

If this is **not** the case, you can configure IPFS to use the public HTTPS gateway by setting:
```
export IPFS_GATEWAY=https://ipfs.io
```
:::
::::

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
