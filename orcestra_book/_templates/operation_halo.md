<!-- This file was created automatically -->
# HALO

```{admonition} How-to
:class: info

* [for mission PI and flight planning](../plans/howto)
* [for Documentation Scientist](../plans/doc-sci)
* {doc}`../flightplan_docs`
* {doc}`../plans/howto_groundsupport`
```

```{admonition} Background information
:class: seealso

[Check this out](../halo), if you like to know more about the platform and its instrumentation.
```

## Planning and Reporting

For an overview of all flight categories, [click here](flight_categories).

Flight-ID | Date | Takeoff | Landing | PI | Nickname | Categories
--- | --- | --- | --- | --- | --- | ---
{% for k, v in flights.items() -%}
{% set c1 = v["refs"]|join(", ") -%}
{% set c2 = v["takeoff"].strftime("%d %B %Y") -%}
{% set c3 = v["takeoff_local"]|lt_utc -%}
{% set c4 = v["landing_local"]|lt_utc -%}
{% set c5 = v["pi"] -%}
{% set c6 = v["nickname"] -%}
{{ k }} ({{ c1 }}) | {{ c2 }} | {{ c3 }} | {{ c4 }} | {{ c5 }} | {{ c6 }} | {% for cat in v["categories"] %}{flight-cat}`{{cat}}` {% endfor %}
{% endfor -%}
