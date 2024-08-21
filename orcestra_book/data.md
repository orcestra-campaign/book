# Data



## Naming scheme for aircraft measurements

The naming scheme `<aircraft>-<year><month><day><letter>` (i.e. _HALO-20240810a_) shall serve as a clean and future-proof way to identify flights. The `<letter>` in the end of the scheme will distinguish between cases, when several flights will take place in one day.

For quicklook data the terminus `QL_<aircraft>-<year><month><day><letter>_<instrument>_<Version: Vxx>` is recommended.


## Tools

Some tools and data scripts:
* [AERIS](https://observations.ipsl.fr/aeris/maestro/#/map) - Flight track planning tool shaped for MAESTRO
* [MISVA](https://misva.aeris-data.fr/en/homepage/) - Monitoring and forecast of IntraSeasonal Variability over Africa 
* [TOOCAN](https://toocan.ipsl.fr/) - Tracking and characterizing mesoscale convective systems
* [ERA5 example data script](hera5.md)
* [pyorcestra](https://github.com/orcestra-campaign/pyorcestra) - A python package created for ORCESTRA purposes
