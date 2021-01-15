---
Title: COVID-19 Mortality and Disinformation - Part 4
Date: 2021-01-13 12:15
author: Kivan Polimis
Category: Tutorials
Status: draft
---

# Covid Mortality and Disinformation - (Part 4)

In the previous two posts we downloaded mortality data from the [National Center for Health Statistics](https://www.cdc.gov/nchs/about/50th_anniversary.htm) (NCHS) and population data from the Census from 1999 to 2020

load libraries
``` {.r}
library(here)
library(reshape2)
library(lubridate)
library(tidyverse)
```

``` {.r}
mortality_time_series_national = read_csv(here("output/mortality_time_series_national.csv"))
social_media_mortality_data = read_csv(here("data/social_media_mortality_data.csv"))
```

``` {.r}
names(mortality_time_series_national)
names(social_media_mortality_data)
```

``` {.r}
mortality_time_series_national$source = "CDC & Census"
social_media_mortality_data$source = "Social Media"
mortality_comparison_data_long = rbind(mortality_time_series_national, social_media_mortality_data)
```

``` {.r}
mortality_comparison_data_wide = reshape2::dcast(mortality_comparison_data_long, state_name + year + source ~ variable) %>%
  group_by(source) %>%
  arrange(source) %>%
  mutate(mortality_rate = round((all_deaths/pop_estimate)*100000),
         mortality_rate_lag = lag(mortality_rate, order_by = year),
         mortality_rate_roc = 100 * (mortality_rate - mortality_rate_lag)/mortality_rate_lag)
```

<div>
<img src="images/us_mortality_rate_plot.png" alt="Rate of Change: US Mortality Rate Change from 1999 to 2020">
</div>

<div>
<img src="images/us_mortality_rate_roc_plot.png" alt="Rate of Change: US Mortality Rate Change from 1999 to 2020">
</div>

<div>
<img src="images/us_mortality_rate_facet_plot.png" alt="US Mortality Rate per 100,000 from 1999 to 2020 (Dual Plots)">
</div>

<div>
<img src="images/us_mortality_rate_roc_facet_plot.png" alt="Rate of Change: US Mortality Rate of Change from 1999 to 2020 (Dual Plots)">
</div>

```{.r}
mortality_rate_roc_comparison =  mortality_comparison_data_wide %>%
  mutate(period = ifelse(year<2020,"1999-2019", "2020"),
         cohort = ifelse(year>=1999 & year<2005, "1999-2004",
                         ifelse(year>=2005 & year<2010, "2005-2009",
                                ifelse(year>=2010 & year<2015, "2010-2014",
                                       ifelse(year>=2015 & year<2020, "2015-2019", "2020"))))) %>%
  group_by(source, cohort) %>%
  mutate(cohort_mortality_rate_roc = round(mean(mortality_rate_roc, na.rm = TRUE),3)) %>%
  ungroup() %>%
  group_by(source, period) %>%
  mutate(period_mortality_rate_roc = round(mean(mortality_rate_roc, na.rm = TRUE), 3)) %>%
  select(source, cohort, period, cohort_mortality_rate_roc, period_mortality_rate_roc) %>%
  distinct()
```

<!-- Thu Jan 14 19:53:55 2021 -->
<table border=1>
<caption align="bottom"> Comparison of US Mortality Rate of Change (ROC) by Data Source, Cohort, and Period </caption>
<tr> <th> Data Source </th> <th> Cohort </th> <th> Period </th> <th> Cohort Mortality Rate ROC </th> <th> Period Mortality Rate ROC </th>  </tr>
  <tr> <td> CDC &amp; Census </td> <td> 1999-2004 </td> <td align="center"> 1999-2019 </td> <td align="center"> -0.008 </td> <td align="center"> 0.001 </td> </tr>
  <tr> <td> CDC &amp; Census </td> <td> 2005-2009 </td> <td align="center"> 1999-2019 </td> <td align="center"> -0.006 </td> <td align="center"> 0.001 </td> </tr>
  <tr> <td> CDC &amp; Census </td> <td> 2010-2014 </td> <td align="center"> 1999-2019 </td> <td align="center"> 0.008 </td> <td align="center"> 0.001 </td> </tr>
  <tr> <td> CDC &amp; Census </td> <td> 2015-2019 </td> <td align="center"> 1999-2019 </td> <td align="center"> 0.010 </td> <td align="center"> 0.001 </td> </tr>
  <tr> <td> CDC &amp; Census </td> <td> 2020 </td> <td align="center"> 2020 </td> <td align="center"> 0.113 </td> <td align="center"> 0.113 </td> </tr>
  <tr> <td> Social Media </td> <td> 1999-2004 </td> <td align="center"> 1999-2019 </td> <td align="center"> -0.009 </td> <td align="center"> 0.001 </td> </tr>
  <tr> <td> Social Media </td> <td> 2005-2009 </td> <td align="center"> 1999-2019 </td> <td align="center"> -0.006 </td> <td align="center"> 0.001 </td> </tr>
  <tr> <td> Social Media </td> <td> 2010-2014 </td> <td align="center"> 1999-2019 </td> <td align="center"> 0.007 </td> <td align="center"> 0.001 </td> </tr>
  <tr> <td> Social Media </td> <td> 2015-2019 </td> <td align="center"> 1999-2019 </td> <td align="center"> 0.011 </td> <td align="center"> 0.001 </td> </tr>
  <tr> <td> Social Media </td> <td> 2020 </td> <td align="center"> 2020 </td> <td align="center"> 0.011 </td> <td align="center"> 0.011 </td> </tr>
</table>
