---
orphan: true
---

# Limited area model

A numerical campaign was performed in parallel to ORCESTRA, which consisted in daily hindcasts simulations of the Atlantic ITCZ.

These limited-area models (LAMs) were run with [ICON-MPI](https://gitlab.dkrz.de/icon/icon-mpim) at a horizontal resolution of 1.25km, and covered the (64W-8W,4S-24N)-area. Each daily run was initialized from the (day-1)-00h00 IFS analysis, and marched in times for 48h using the IFS forecast for lateral and surface boundary conditions. The first 24h are considered a transient time, as the solution adapts to the high-resolution mesh and non-hydrostatic solver. A concatenation of all second days is shown below, illustrating the complexity of the campaign:

<video width="700" controls="" poster="hhttps://swift.dkrz.de/v1/dkrz_f765c92765f44c068725c0d08cc1e6c5/LAM-ORCESTRA/pathways-rsut_ZoomLvl1-thumb.png">
  <source src="https://swift.dkrz.de/v1/dkrz_f765c92765f44c068725c0d08cc1e6c5/LAM-ORCESTRA/pathways-rsut_ZoomLvl1.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

Tracks of ATR-42, HALO and RV METEOR simulated with the Limited Area Model throughout the campaign (*by R. Fievet*).

Further, animations of key variables were constructed to showcase all runs. These are available at different "zoom-levels" 1, 2 and 3, corresponding to horizontal resolutions of 5.0, 2.5 and 1.25 kilometers, respectively. All animations can be found in this [publicly-accessible server](https://swiftbrowser.dkrz.de/public/dkrz_f765c92765f44c068725c0d08cc1e6c5/LAM-ORCESTRA/), and are presented below as well.

The whole dataset is stored on [Levante (DKRZ)](https://docs.dkrz.de/doc/levante/index.html) and accessible on demand. It comprises of high-sampling rate 2D and 3D snapshots of key variables.

## Daily simulations

```{list-videos}
```

<script>
    let today = new Date();
    // HACK: Simulations take a while... should be available with an 8-day offset
    let week = new Date(1979, 1, 9) - new Date(1979, 1, 1);

    document.querySelectorAll("#daily-simulations .reference.external").forEach(function(link) {
        let linkDate = new Date(link.innerText);
        // HACK: This should be replaced by properly checking an index of existing simulations
        if (linkDate > (today - week)) {
            link.parentNode.removeChild(link);
        }
    });
</script>
