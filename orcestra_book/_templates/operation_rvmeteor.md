<!-- This file was created automatically -->
# RV METEOR

```{admonition} Background information
:class: seealso

[Check this out](../rvmeteor), if you like to know more about the platform and its instrumentation.
```

## Reporting

Report-ID | Date | Report author
--- | --- | ---
{% for k, v in reports.items() -%}
[](../reports/{{ k }}) | {{ v["date"] }} | {{ v["pi"] }}
{% endfor -%}
