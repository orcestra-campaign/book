<!-- This file was created automatically -->
# King Air

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
