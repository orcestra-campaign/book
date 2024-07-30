<!-- This file was created automatically -->
# HALO

Flight-ID | Date | Takeoff | Landing | PI | Nickname | Categories
--- | --- | --- | --- | --- | --- | ---
{% for k, v in flights.items() -%}
{{ v["expr_refs"] }} | {{ v["expr_date"] }} | {{ v["expr_takeoff"] }} | {{ v["expr_landing"] }} | {{ v["pi"] }} | {{ v["nickname"] }} | {{ v["expr_categories"]|join(' ') }}
{% endfor -%}
