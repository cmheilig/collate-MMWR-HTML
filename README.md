# Collate _MMWR_ HTML
Code to extract and collate HTML of 56 full reports selected for review.

This repository contains Python code and auxiliary assets to do the following: 
1. Extract MMWR HTML from a zipped JSON object, [mmwr_art_en_html_json.zip](https://github.com/cmheilig/harvest-cdc-journals/blob/main/json-outputs/html/mmwr_art_en_html_json.zip), that contains HTML for approximately 13,000 [_MMWR_ weekly reports online](https://www.cdc.gov/mmwr/). See the [full _CDC text corpora for learners_ repository](https://github.com/cmheilig/harvest-cdc-journals) for further details.
2. Extract HTML for the 56 selected full reports.
3. Extract and trim core HTML for each report by removing unneeded segments and inserting anchors to aid with on-page navigation.
4. Collate trimmed, revised core HTML—along with a preconstructed header, table of contents, and tail—into a single HTML file.

We created a resource for learners, [Data in the _MMWR_](https://bookdown.org/cmheilig/data-in-mmwr/): A purposive review with recommendations, as a collection of examples for closely reviewing public health reports. We reviewed 56 full reports published between January 2019 and May 2022 to identify specific practices regarding presentations of data, analytic methods and results, tables and graphics, and interpretation of results. Within that resource, we included [trimmed, collated version](https://bookdown.org/cmheilig/data-in-mmwr/mmwr-selectees-compiled.html) of those 56 reports for convenience. For example, one can easily search across all selected reports at once. The 56 full reports selected for this review are listed in chronological order of publication, with links from the report identifier to the text of the report and to HTML and PDF versions on the _MMWR_ website, along with lead author, title, publication date, volume, issue, and pages.

This repository contains the following:
- An annotated [Python script](https://github.com/cmheilig/collate-MMWR-HTML/blob/main/pycode/collate-selectee-html.py) to extract and collate full reports.
- A [collection of CSS and image files](https://github.com/cmheilig/collate-MMWR-HTML/tree/main/assets) that support rendering of the collated HTML. These assets are adapted from those used on the MMWR website and referenced in the `head` element of each published report.
- A fixed [HTML header](https://github.com/cmheilig/collate-MMWR-HTML/blob/main/html/mmwr-selectees-head.html), [table of contents](https://github.com/cmheilig/collate-MMWR-HTML/blob/main/html/mmwr-selectees-toc.html), and [tail](https://github.com/cmheilig/collate-MMWR-HTML/blob/main/html/mmwr-selectees-tail.html) in which to couch the trimmed, collated HTML from the selected reports, yielding a single, complete, internally coherent HTML file. The [collated HTML file](https://github.com/cmheilig/collate-MMWR-HTML/blob/main/html/mmwr-selectees-compiled.html) is also included.
