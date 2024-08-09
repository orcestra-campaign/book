<!-- This file was created automatically -->
# ATR-42

Flight-ID | Date | Takeoff | Landing | PI | Nickname
--- | --- | --- | --- | --- | ---
{% for k, v in flights.items() -%}
{% set c1 = v["refs"]|join(", ") -%}
{% set c2 = v["takeoff"].strftime("%d %B %Y") -%}
{% set c3 = v["takeoff"].strftime("%X") -%}
{% set c4 = v["landing"].strftime("%X") -%}
{% set c5 = v["pi"] -%}
{% set c6 = v["nickname"] -%}
{{ k }} ({{ c1 }}) | {{ c2 }} | {{ c3 }} | {{ c4 }} | {{ c5 }} | {{ c6 }}
{% endfor -%}
