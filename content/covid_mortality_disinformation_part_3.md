---
Title: COVID-19 Mortality and Disinformation - Part 3
Date: 2021-01-14 07:11
author: Kivan Polimis
Category: Tutorials
---

# Covid Mortality and Disinformation - (Part 3)

In the previous two posts we [downloaded mortality data](http://kivanpolimis.com/covid-19-mortality-and-disinformation-part-1.html) from the [National Center for Health Statistics](https://www.cdc.gov/nchs/about/50th_anniversary.htm) (NCHS) and [downloaded population data](http://kivanpolimis.com/covid-19-mortality-and-disinformation-part-2.html) from the Census. The goal of this post is to create mortality statistics by combining the mortality data with population data.

* load libraries
``` {.r}
library(here)
library(reshape2)
library(tidyverse)
library(data.table)
```

* read in Census population data
``` {.r}
national_population_1999_2020 =  read_csv(here("data/national_population_1999_2020.csv"))
```

* read in NCHS population data

``` {.r}
yearly_deaths_by_state_1999_2020 = read_csv(here("data/yearly_deaths_by_state_1999_2020.csv"))
```

```{.r}
names(national_population_1999_2020)
names(yearly_deaths_by_state_1999_2020)
```

* what are the variable names in each dataset?

```
##  [1] "state_name"        "pop_estimate_1999" "pop_estimate_2000"
##  [4] "pop_estimate_2001" "pop_estimate_2002" "pop_estimate_2003"
##  [7] "pop_estimate_2004" "pop_estimate_2005" "pop_estimate_2006"
## [10] "pop_estimate_2007" "pop_estimate_2008" "pop_estimate_2009"
## [13] "pop_estimate_2010" "pop_estimate_2011" "pop_estimate_2012"
## [16] "pop_estimate_2013" "pop_estimate_2014" "pop_estimate_2015"
## [19] "pop_estimate_2016" "pop_estimate_2017" "pop_estimate_2018"
## [22] "pop_estimate_2019" "pop_estimate_2020"
```


```
## [1] "state_name" "year"       "all_deaths"
```

* reshape mortality and population datasets into long datasets
``` {.r}
yearly_deaths_by_state_1999_2020_long = reshape2::melt(yearly_deaths_by_state_1999_2020, id.vars = c("state_name", "year"))
national_population_1999_2020_long = reshape2::melt(national_population_1999_2020, id.vars = c("state_name"))
national_population_1999_2020_long$year = mapply(FUN= function(variable) strsplit(as.character(variable),"estimate_")[[1]][2], national_population_1999_2020_long$variable)
national_population_1999_2020_long$variable = mapply(FUN= function(variable) substr(as.character(variable),1,12), national_population_1999_2020_long$variable)
```

* create national mortality and population data
``` {.r}
mortality_time_series_national = rbindlist(list(national_population_1999_2020_long,
                                                yearly_deaths_by_state_1999_2020_long),
                                           use.names=TRUE) %>% filter(state_name=="United States")

```

Now that we have dataset with mortality and population data, we can create a wide data set to calculate mortality rates and rates of change metric for mortality rates

* reshape national mortality and population data into a wide mortality/population dataset from 1999 to 2020
* create mortality rate for each year (y). we will create mortality rates per 100,000 people to compare with the social media post that used the same scale
* also create mortality rate of change metric to understand how each current year's mortality rate compares to the preceding year's mortality rate

$$\text{Mortality Rate}_{y}= \frac{\text{All Deaths}_{y}}{\text{Population Estimate}_{y}} * \text{100, 000}$$

$$\text{Rate of Change}_{y}= \frac{\text{Mortality Rate}_{y}-\text{Mortality Rate}_{y-1}}{\text{Mortality Rate}_{y-1}}$$

``` {.r}
us_mortality_data_1999_2020 = reshape2::dcast(mortality_time_series_national, state_name + year ~ variable) %>%
  arrange(year) %>%
  mutate(mortality_rate = round((all_deaths/pop_estimate)*100000),
         mortality_rate_lag = lag(mortality_rate, order_by = year),
         mortality_rate_roc = (mortality_rate - mortality_rate_lag)/mortality_rate_lag)
```

Let's use the government data to recreate the table from the social media post that spurred this blog series

<!-- html table generated in R 3.6.3 by xtable 1.8-4 package -->
<!-- Fri Jan 15 16:55:38 2021 -->
<table border=1>
<caption align="bottom"> US Mortality Rate 1999 to 2020 </caption>
<tr> <th> Year </th> <th> Population </th> <th> Deaths </th> <th> Mortality Rate </th>  </tr>
  <tr> <td> 1999 </td> <td> 280,466,621 </td> <td> 2,391,399 </td> <td> 853 </td> </tr>
  <tr> <td> 2000 </td> <td> 281,424,600 </td> <td> 2,403,351 </td> <td> 854 </td> </tr>
  <tr> <td> 2001 </td> <td> 284,968,955 </td> <td> 2,416,425 </td> <td> 848 </td> </tr>
  <tr> <td> 2002 </td> <td> 287,625,193 </td> <td> 2,443,387 </td> <td> 850 </td> </tr>
  <tr> <td> 2003 </td> <td> 290,107,933 </td> <td> 2,448,288 </td> <td> 844 </td> </tr>
  <tr> <td> 2004 </td> <td> 292,805,298 </td> <td> 2,397,615 </td> <td> 819 </td> </tr>
  <tr> <td> 2005 </td> <td> 295,516,599 </td> <td> 2,448,017 </td> <td> 828 </td> </tr>
  <tr> <td> 2006 </td> <td> 298,379,912 </td> <td> 2,426,264 </td> <td> 813 </td> </tr>
  <tr> <td> 2007 </td> <td> 301,231,207 </td> <td> 2,423,712 </td> <td> 805 </td> </tr>
  <tr> <td> 2008 </td> <td> 304,093,966 </td> <td> 2,471,984 </td> <td> 813 </td> </tr>
  <tr> <td> 2009 </td> <td> 306,771,529 </td> <td> 2,437,163 </td> <td> 794 </td> </tr>
  <tr> <td> 2010 </td> <td> 308,745,538 </td> <td> 2,468,435 </td> <td> 800 </td> </tr>
  <tr> <td> 2011 </td> <td> 311,583,481 </td> <td> 2,515,458 </td> <td> 807 </td> </tr>
  <tr> <td> 2012 </td> <td> 313,877,662 </td> <td> 2,543,279 </td> <td> 810 </td> </tr>
  <tr> <td> 2013 </td> <td> 316,059,947 </td> <td> 2,596,993 </td> <td> 822 </td> </tr>
  <tr> <td> 2014 </td> <td> 318,386,329 </td> <td> 2,626,418 </td> <td> 825 </td> </tr>
  <tr> <td> 2015 </td> <td> 320,738,994 </td> <td> 2,712,630 </td> <td> 846 </td> </tr>
  <tr> <td> 2016 </td> <td> 323,071,755 </td> <td> 2,744,248 </td> <td> 849 </td> </tr>
  <tr> <td> 2017 </td> <td> 325,122,128 </td> <td> 2,813,503 </td> <td> 865 </td> </tr>
  <tr> <td> 2018 </td> <td> 326,838,199 </td> <td> 2,839,076 </td> <td> 869 </td> </tr>
  <tr> <td> 2019 </td> <td> 328,329,953 </td> <td> 2,852,609 </td> <td> 869 </td> </tr>
  <tr> <td> 2020 </td> <td> 329,484,123 </td> <td> 3,258,883 </td> <td> 989 </td> </tr>
</table>

We now have all the data we need to compare the mortality rates obtained from government data with the mortality rates shown in the social media post. Continue to [Part 4](http://kivanpolimis.com/covid-19-mortality-and-disinformation-part-4.html) to view the results of this comparison.
