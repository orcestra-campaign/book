<!-- This file was created automatically -->
# ATR-42

```{admonition} How to plan an ATR flight
:class: info
For an introduction to the ATR flight planning, [click here](../plans/howto_atr)
```

```{admonition} Background information
:class: seealso

[Check this out](../atr42), if you like to know more about the platform and its instrumentation.
```

## Planning and Reporting

For an overview of all flight categories, [click here](flight_categories).

Flight-ID | Date | Takeoff | Landing | PI | Categories
--- | --- | --- | --- | --- | ---
{% for k, v in flights.items() -%}
{% set c1 = v["refs"]|join(", ") -%}
{% set c2 = v["takeoff"].strftime("%d %B %Y") -%}
{% set c3 = v["takeoff_local"]|lt_utc -%}
{% set c4 = v["landing_local"]|lt_utc -%}
{% set c5 = v["pi"] -%}
{{ k }} ({{ c1 }}) | {{ c2 }} | {{ c3 }} | {{ c4 }} | {{ c5 }} | {% for cat in v["categories"] %}{flight-cat}`{{cat}}` {% endfor %}
{% endfor -%}
