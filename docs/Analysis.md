# Analysis Tab

**The Analysis Tab shown with dark mode selected**


![Analysis Tab](./images/Analysis-dark.png)

## Content Table

[Applying Filters, Compare Hosts Example](#applying-filters-compare-hosts-example)
[Applying Filters, Compare Backend Example](#applying-filters-compare-backend-example)
[Export PDF](#export-to-pdf)
[Export Markdown](#export-to-markdown)


## Overview

The Analysis tab provides a graphical comparison of various LLM characteristics captured in the benchmark database. The primary metric or measure of performance is Tokens Per Second (**TPS**) although we can compare model size and model parameter count as well.

## Filters

A number of filters are provided allowing more accurate control over exactly what we are comparing. Creating a graph with no filters will ignore, the model, hosts, backend, test_type, when the benchmark was run, illama-bench version, and graph grouping.

When a database contains benchmark data from multiple Hosts, GPUs, and Backends the TPS number will be virtually meaningless with no filters applied to the graph data. Applying the appropriate filter is required to make accurate comparisons.

Clicking the *Filters* button opens the Filter Dialog Window

![Analysis Filter Window](./images/analysis-filters.png)

### Applying Filters, Compare Hosts Example

[Back to Content](#content-table)

**Please Note, before any benchmark runs the database will be empty and this is where we obtain the filter content. No filter content will be displayed**

There are two hosts in the database created and maintained while developing the localmind application, Fedora550 and Ryzen9x670. One is running Fedora Linux and the other Windows 11. The Linux host has an Intel Arc B580 GPU and the Windows host an Intel Arc Pro B70 GPU. Obviously we do not want to mix TPS results from these two sources without applying filters, typically we would select a host as a filter when we want to limit the scope of the analysis to a single or limited hosts.

For this example we want to compare the TPS of these two hosts for Gemma-4-E2B and E4B models. On the Fedora hosts I am only running the SYCL backend so I do not want to consider Vulkan backend runs on the Windows host. We only want to look at benchmark runs from the past week.

- Select the models

Select the *Model* radio button and then click the *Select* button and select the models of interest.

![Model Selection](./images/analysis-select-model.png)

The filter dialog now shows the selected models.

![Selected Models](./images/filters-selected-models.png)

- Select the SYCL backend benchmarks

Select the *Backend* radio button and then click the *Select* button and click the SYCL option, this retrieves only SYCL backend benchmarks.

![Select the Backend](./images/analysis-select-sycl.png)

- Select the *Time Range* radio button and click the *Select* button

Select the start date and the end date of the time range of interest, for this example we will use data from one week.

![Select Time Range](images/analysis-select-time-range.png)

- Select the grouping category

Click the *Group By* button and select *Model* then click *Ok*

![Select Group By](./images/analysis-group-by.png)

The Filters dialog now shows all configured filters.


![Host Compare Configured Filters](./images/analysis-filters-host-compare.png)

Click *Done* and then select the category as *Host*

Click the *Show Graph* button to apply the filters and show the graph

![Compare Hosts Graph](./images/compare-hosts.png)

This graph shows the TPS for the averaged Prompt test and Generation tests. Lets take a look at Generation and Prompt separately by applying the appropriate filter.

Click the *Filters* button and then the *Test Type* radio button and the *Select*. Select the **Prompt** test.

![Select the Prompt Test](./images/analysis-select-prompt.png)

Click *Ok* and then *Done*

Now Click *Show Graph* to compare the prompt tests on the two hosts. We still see the large disparity between the two hosts.

![Compare Hosts Graph](./images/compare-hosts-prompt.png)

**Now do the same for Generation**

- Open the FIlters dialog and select the generation test type.

![Select the Generation Test](./images/analysis-select-generation.png)

![Compare Hosts Graph](./images/compare-hosts-generation.png)

As you can see the performance is much closer on the Generation test. 

### Applying Filters, Compare Backend Example

[Back to Content](#content-table)


For this example we want to compare the two backends SYCL and Vulkan to each other on the Ryzen9x670 host.
Configure the filters
- Select the same gemma-4 models used in the previous example.
- Select host 
- Select the time range
- Set the group by parameter

![Compare Backend Filters](./images/analysis-compare-backend-filters.png)

- Click done and select the 'Backend' category
- Click the 'Show Graph' button

![Compare Backend Graph](./images/analysis-compare-backends-graph.png)

This graph shows the aggregate average of all TPS values from both the Generation and Prompt tests. We want to refine this to show only the generation test results. 

First we add the test type to the selected filters.

![Compare Backend Gen Tests](./images/analysis-compare-backends-graph-gen-filters.png)

- Click 'Done' and 'Show Graph'

Here we can see that we have mixed results. With the exception of the gemma-4-E4B-it-Q8_0 model, SYCL shows better performance.

![Compare Backend Graph](./images/analysis-compare-backends-graph2.png)

## Exporting Graph Results

Graph results can be exported to either a PDF document or a Markdown document. 

### Export to PDF

[Back to Content](#content-table)

- Click the Export button on the sidebar.
- Select PDF if not selected.
- Click the 'Open PDF after generation' to enable/disable PDF preview in system PDF viewer.

![Analysis Export PDF](./images/analysis-export-pdf.png)

- Click Ok
- Select the folder where the pdf file is to be saved. The default is in you user localmind folder.

![Analysis Export PDF Folder](./images/analysis-export-pdf-folder.png)

If the 'Open PDF after generation' option was selected you will see a preview of the exported PDF document.

![Analysis Export PDF Preview](./images/analysis-export-pdf-preview.png)

[Back to Content](#content-table)


### Export to Markdown

[Back to Content](#content-table)

- Click the Export button on the sidebar.
- Select Markdown.
- The 'Open PDF after generation' will dissappear, you always get a preview when Markdown is exported.

![Markdown Export Select](./images/analysis-export-markdown.png)

- Click Ok and select the name and location of the exported markdown.
- A markdown preview window will appear.

![Markdown Preview](./images/analysis-export-markdown-preview.png)

[Back to Content](#content-table)


