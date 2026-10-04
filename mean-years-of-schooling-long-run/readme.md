# Average years of schooling - Data package

This data package contains the data that powers the chart ["Average years of schooling"](https://ourworldindata.org/grapher/mean-years-of-schooling-long-run?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website. It was downloaded on October 4, 2026.

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


### Average years of schooling
Average years of formal education for individuals aged 15-64.
Last updated: July 17, 2023  
Date range: 1870–2040  
Unit: years  
Source: Barro and Lee (2015); Lee and Lee (2016) – with major processing by Our World in Data  

#### How to cite this data

Barro and Lee (2015); Lee and Lee (2016) – with major processing by Our World in Data

#### What you should know about this data
- For the years leading up to 2015, the data are derived from historical estimates, providing a retrospective view of education levels. For the years 2015 and beyond, the projections are grounded in the historical data of 2010, which serve as the foundational benchmark. These forward-looking projections are then crafted by analyzing trends in school enrollment and changes in population structures. These trends are informed by forecasts from the United Nations, ensuring a global perspective and understanding of future educational developments.
- The method to estimate average years of schooling takes into account the age distribution in the population. This is important because access to education can vary significantly across generations. Older generations may have had fewer educational opportunities than younger ones, which affects the overall average education level.
- It also considers the typical duration required to complete each education level. For instance, primary education usually takes about 6 years, secondary education 4-6 years, and higher education may take even longer. Understanding the time investment required for different education levels is essential for accurate assessment.
- At its core, the method calculates the average years of schooling. This is achieved by determining the percentage of the population that has completed each education level and multiplying it by the duration of that level. The sum of these results gives a comprehensive view of both the extent of educational attainment and the time spent in education by the population.
- The method is dynamic, adapting to changes over time and across regions. For example, if a country increases the length of primary education, this change is included in subsequent calculations. This adaptability ensures that the average years of education remain relevant and accurate over time and across different educational systems.
- Note that the method does not take into account the quality of education. It only considers the number of years spent in education. This means that the average years of schooling may not reflect the actual skills and knowledge of the population.

#### Notes on our processing step for this indicator
Historical data up to the year 2010 has been sourced from 'Human Capital in the Long Run' by Lee and Lee (2016). This historical data was then combined with recent projections provided by Barro ane Lee (2015).

Regional aggregates were computed by Our World in Data through yearly population-weighted averages, where annual values are proportionally adjusted to emphasize the influence of larger populations.



## Sources

These are the sources behind the data in this package. Each time series above names the ones it draws on in its citation.

### Barro and Lee – Projections of Educational Attainment

Using the estimates on school enrollment and population structure, Barro and Lee have constructed projections of educational attainment for the population, disaggregated by gender and age group (15–24, 25–64, and 15–64) for 146 countries from 2015 to 2040 at five-year intervals.

They first use the 2010 data on educational attainment by age group as benchmark figures to project the educational attainment of the population by age group for the next three decades. They then estimate the distribution of educational attainment for the younger population, aged 15-24, at the five-year intervals from 2015 to 2040 and then forward-extrapolate the estimates to construct the distribution of educational attainment for the older population groups. For the population structure, they use existing U.N. projections. For the detailed explanation of the estimation method, see Barro and Lee (2015, chapter 3).

Producer: Barro and Lee  
Published: 2015  
Retrieved on: 2023-11-20  
Retrieved from: http://www.barrolee.com/  
License: 2021 by Robert J. Barro and Jong-Wha Lee. (https://barrolee.github.io/BarroLeeDataSet/OUPProj.html)  

Citation: Barro, Robert J. and Jong-Wha Lee, Education Matters: Global Schooling Gains from the 19th to the 21st Century (Oxford University Press, 2015)

### Lee and Lee – Human Capital in the Long Run

Datasets on estimated school enrollment ratios from 1820 to 2010 and estimated educational attainment for the total, female, and male populations from 1870 to 2010. The estimates are available in five-year intervals for 111 countries.

Datasets were last updated in 2021 September. The research provides insightful analysis on the progression and trends of educational attainment over a long historical period, offering a comprehensive understanding of educational developments globally.

Producer: Lee and Lee  
Published: 2016  
Retrieved on: 2023-11-20  
Retrieved from: https://barrolee.github.io/BarroLeeDataSet/DataLeeLee.html  
License: 2021 by Robert J. Barro and Jong-Wha Lee. (https://barrolee.github.io/BarroLeeDataSet/OUPProj.html)  

Citation: Lee, Jong-Wha and Hanol Lee, 2016, “Human Capital in the Long Run,” Journal of Development Economics, vol. 122, pp. 147-169.

    