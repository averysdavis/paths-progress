# Life expectancy - Data package

This data package contains the data that powers the chart ["Life expectancy"](https://ourworldindata.org/grapher/life-expectancy-hmd-unwpp?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website. It was downloaded on October 4, 2026.

### Active Filters

A filtered subset of the full data was downloaded. The following filters were applied:

## CSV structure

Each row is an observation for an entity (usually a country or region) at a timepoint.

- "Entity" — the name of the entity, e.g. "United States".
- "Code" — our internal entity code. For most countries this is the [ISO alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) code, e.g. "USA"; historical and other non-standard entities get a custom code.
- "Year" or "Day" — the timepoint. Annual data has a "Year" column holding an integer year; otherwise a "Day" column holds a date string in the form "YYYY-MM-DD".
- The final column is the data column — the time series that powers the chart. Downloaded with the "full data" option it corresponds to the time series below; with "only selected data visible in the chart" it is transformed depending on the chart type, so the correspondence may be less direct.


## Metadata.json structure

The .metadata.json file contains metadata about the data package. The "charts" key contains information to recreate the chart, like the title, subtitle etc. The "columns" key contains information about each of the columns in the csv, like the unit, timespan covered, citation for the data etc.

## How we process data at Our World in Data

Our World in Data is almost never the original producer of the data - almost all of the data we use has been compiled by others. If you want to re-use data, it is your responsibility to ensure that you adhere to the sources' license and to credit them correctly. Please note that a single time series may have more than one source - e.g. when we stitch together data from different time periods by different producers or when we calculate per capita metrics using population data from a second source.

Preparing this data involves several processing steps. Depending on the data, this can include standardizing country names and world region definitions, converting units, calculating derived indicators such as per capita measures, as well as adding or adapting metadata such as the name or the description given to an indicator.
[Read about our data pipeline](https://docs.owid.io/projects/etl/).

## Detailed information about the data


### Life expectancy at birth – totals, period tables – HMD
Period life expectancy at birth among totals, in a given year.
Last updated: October 22, 2025  
Next expected update: October 2026  
Date range: 1751–2023  
Unit: years  
Source: Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data  

#### How to cite this data

Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data

#### What you should know about this data
- Period life expectancy is a metric that summarizes death rates across all age groups in one particular year.
- For a given year, it represents the average lifespan for a hypothetical group of people, if they experienced the same age-specific death rates throughout their whole lives as the age-specific death rates seen in that particular year.
- Prior to 1950, we use HMD (2025) data. From 1950 onwards, we use UN WPP (2024) data.


## Sources

These are the sources behind the data in this package. Each time series above names the ones it draws on in its citation.

### Human Mortality Database

The Human Mortality Database (HMD) is a research resource that provides detailed mortality and population data for national populations with high-quality vital statistics. It includes original calculations of death rates and life tables, as well as the underlying data — such as birth counts, death counts, and census-based population estimates — used to produce these metrics.

Its scope is limited to countries with virtually complete death registration and census coverage, mostly wealthy and industrialized nations. The database’s core mission is to document the historical rise in human longevity and support research into its causes and implications. HMD follows a rigorous, uniform methodology focused on transparency, reproducibility, and comparability, while acknowledging limitations such as age misreporting and data coverage issues.

Each country’s dataset is curated and quality-checked by dedicated researchers, ensuring reliability for demographic and public health analysis.

Producer: Human Mortality Database  
Published: 2025-09-25  
Retrieved on: 2025-10-22  
Retrieved from: https://www.mortality.org/Data/ZippedDataFiles  
License: CC BY 4.0 (https://www.mortality.org/Data/UserAgreement)  

Citation: HMD. Human Mortality Database. Max Planck Institute for Demographic Research (Germany), University of California, Berkeley (USA), and French Institute for Demographic Studies (France). Available at www.mortality.org.

See also the methods protocol:
Wilmoth, J. R., Andreev, K., Jdanov, D., Glei, D. A., Riffe, T., Boe, C., Bubenheim, M., Philipov, D., Shkolnikov, V., Vachon, P., Winant, C., & Barbieri, M. (2021). Methods protocol for the human mortality database (v6). [Available online](https://www.mortality.org/File/GetDocument/Public/Docs/MethodsProtocolV6.pdf) (needs log in to mortality.org).

### United Nations – World Population Prospects

The World Population Prospects 2024 is the 28th edition of the official estimates and projections of the global population published by the United Nations since 1951. The estimates are based on all available sources of data on population size and levels of fertility, mortality, and international migration for 237 countries or areas.

For each revision, any new, recent, and historical, information that has become available from population censuses, vital registration of births and deaths, and household surveys is considered to produce consistent time series of population estimates for each country or areas from 1950 to today

For the estimation period between 1950 and 2023, data from 1,910 censuses were considered in the present evaluation, which is 79 more than the 2022 revision. In some countries, population registers based on administrative data systems provide the necessary information. Population data from censuses or registers referring to 2019 or later were available for 114 countries or areas, representing 48 percent of the 237 countries or areas included in this analysis (and 54 percent of the world population). For 43 countries or areas, the most recent available population count was from the period 2014-2018, and for another 57 locations from the period 2009-2013. For the remaining 23 countries or areas, the most recent available census data were from before 2009, that is more than 15 years ago.

Producer: United Nations  
Published: 2024-07-11  
Retrieved on: 2024-12-02  
Retrieved from: https://population.un.org/wpp/downloads/  
License: CC BY 3.0 IGO (https://population.un.org/wpp/downloads/)  

Citation: United Nations, Department of Economic and Social Affairs, Population Division (2024). World Population Prospects 2024, Online Edition.

### United Nations – World Population Prospects

The World Population Prospects 2024 is the 28th edition of the official estimates and projections of the global population published by the United Nations since 1951. The estimates are based on all available sources of data on population size and levels of fertility, mortality, and international migration for 237 countries or areas.

For each revision, any new, recent, and historical, information that has become available from population censuses, vital registration of births and deaths, and household surveys is considered to produce consistent time series of population estimates for each country or areas from 1950 to today

For the estimation period between 1950 and 2023, data from 1,910 censuses were considered in the present evaluation, which is 79 more than the 2022 revision. In some countries, population registers based on administrative data systems provide the necessary information. Population data from censuses or registers referring to 2019 or later were available for 114 countries or areas, representing 48 percent of the 237 countries or areas included in this analysis (and 54 percent of the world population). For 43 countries or areas, the most recent available population count was from the period 2014-2018, and for another 57 locations from the period 2009-2013. For the remaining 23 countries or areas, the most recent available census data were from before 2009, that is more than 15 years ago.

Producer: United Nations  
Published: 2024-07-11  
Retrieved on: 2024-12-17  
Retrieved from: https://population.un.org/wpp/downloads/  
License: CC BY 3.0 IGO (https://population.un.org/wpp/downloads/)  

Citation: United Nations, Department of Economic and Social Affairs, Population Division (2024). World Population Prospects 2024, Online Edition.

    