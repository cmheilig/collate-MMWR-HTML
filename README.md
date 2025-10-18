# collate-MMWR-HTML
Code to extract and collate HTML of 56 full reports selected for review.

This repository contains Python code and auxiliary assets to do the following: 
1. Extract MMWR HTML from a zipped JSON object, [mmwr_art_en_html_json.zip](https://github.com/cmheilig/harvest-cdc-journals/blob/main/json-outputs/html/mmwr_art_en_html_json.zip), that contains HTML for approximately 13,000 [_MMWR_ weekly reports online](https://www.cdc.gov/mmwr/). See the [full repository](https://github.com/cmheilig/harvest-cdc-journals) for further details.
2. Extract HTML for the 56 selected full reports.
3. Extract and trim core HTML for each report by removing unneeded segments and inserting anchors to aid with on-page navigation.
4. Collate trimmed, revised core HTML—along with a preconstructed header, table of contents, and tail—into a single HTML file.


We created a resource for learners, [Data in the _MMWR_](https://bookdown.org/cmheilig/data-in-mmwr/): A purposive review with recommendations, as a collection of examples of closely reviewing public health reports. We reviewed 56 full reports published between January 2019 and May 2022, to identify specific practices regarding presentations of data, analytic methods and results, tables and graphics, and interpretation of results. Within that resource, we included [trimmed, collated version](https://bookdown.org/cmheilig/data-in-mmwr/mmwr-selectees-compiled.html) of those 56 reports for convenience. For example, one can easily search across all selected reports together. The 56 full reports selected for this review are listed in chronological order of publication, with links from the report identifier (e.g., mm6802a1) to the text of the report below, from "HTML" and "PDF1" to the HTML and PDF versions on the MMWR website, respectively, and from "PDF2" to a local copy of the PDF version, followed by the lead author, title, publication date, volume, issue, and pages.
