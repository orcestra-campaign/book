# Lessons Learned

## Share Preliminary Data Early

Many teams provided *quick-look* visualizations rather than preliminary data.  
While useful for initial assessment, these quick looks often created challenges in data interoperability across the campaign.
To improve cross-team collaboration, teams should **share preliminary data as early as possible**, even if the data are not fully curated.

## Use a Monorepo for Joint Tool and Website Development

During the campaign, we organized our shared website in a Git repository and maintained a separate Python package in another repository.  
We found that when tools and documentation are developed side by side, using a **monorepo structure** simplifies coordination, development workflows, and maintenance.
