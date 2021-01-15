---
Title: COVID-19 Mortality and Disinformation - Part 3
Date: 2021-01-14 07:11
author: Kivan Polimis
Category: Tutorials
---

# Covid Mortality and Disinformation - (Part 3)

In the previous two posts we [downloaded mortality data](http://kivanpolimis.com/covid-19-mortality-and-disinformation-part-1.html) from the [National Center for Health Statistics](https://www.cdc.gov/nchs/about/50th_anniversary.htm) (NCHS) and [downloaded population data](http://kivanpolimis.com/covid-19-mortality-and-disinformation-part-2.html) from the Census from 1999 to 2020

load libraries
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

* What are the variable names in each dataset?

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

* Create a long data set of mortality data
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

Let's recreate the table from the social media post that spurred this blog series

<!-- html table generated in R 3.6.3 by xtable 1.8-4 package -->
<!-- Fri Jan 15 16:00:16 2021 -->
<table border=1>
<caption align="bottom"> US Mortality Rate 1999 to 2020 </caption>
<tr> <th> Year </th> <th> Population </th> <th> Deaths </th> <th> Mortality Rate </th>  </tr>
  <tr> <td> 1999 </td> <td align="center"> 280466621 </td> <td align="center"> 2391399 </td> <td align="center"> 853 </td> </tr>
  <tr> <td> 2000 </td> <td align="center"> 281424600 </td> <td align="center"> 2403351 </td> <td align="center"> 854 </td> </tr>
  <tr> <td> 2001 </td> <td align="center"> 284968955 </td> <td align="center"> 2416425 </td> <td align="center"> 848 </td> </tr>
  <tr> <td> 2002 </td> <td align="center"> 287625193 </td> <td align="center"> 2443387 </td> <td align="center"> 850 </td> </tr>
  <tr> <td> 2003 </td> <td align="center"> 290107933 </td> <td align="center"> 2448288 </td> <td align="center"> 844 </td> </tr>
  <tr> <td> 2004 </td> <td align="center"> 292805298 </td> <td align="center"> 2397615 </td> <td align="center"> 819 </td> </tr>
  <tr> <td> 2005 </td> <td align="center"> 295516599 </td> <td align="center"> 2448017 </td> <td align="center"> 828 </td> </tr>
  <tr> <td> 2006 </td> <td align="center"> 298379912 </td> <td align="center"> 2426264 </td> <td align="center"> 813 </td> </tr>
  <tr> <td> 2007 </td> <td align="center"> 301231207 </td> <td align="center"> 2423712 </td> <td align="center"> 805 </td> </tr>
  <tr> <td> 2008 </td> <td align="center"> 304093966 </td> <td align="center"> 2471984 </td> <td align="center"> 813 </td> </tr>
  <tr> <td> 2009 </td> <td align="center"> 306771529 </td> <td align="center"> 2437163 </td> <td align="center"> 794 </td> </tr>
  <tr> <td> 2010 </td> <td align="center"> 308745538 </td> <td align="center"> 2468435 </td> <td align="center"> 800 </td> </tr>
  <tr> <td> 2011 </td> <td align="center"> 311583481 </td> <td align="center"> 2515458 </td> <td align="center"> 807 </td> </tr>
  <tr> <td> 2012 </td> <td align="center"> 313877662 </td> <td align="center"> 2543279 </td> <td align="center"> 810 </td> </tr>
  <tr> <td> 2013 </td> <td align="center"> 316059947 </td> <td align="center"> 2596993 </td> <td align="center"> 822 </td> </tr>
  <tr> <td> 2014 </td> <td align="center"> 318386329 </td> <td align="center"> 2626418 </td> <td align="center"> 825 </td> </tr>
  <tr> <td> 2015 </td> <td align="center"> 320738994 </td> <td align="center"> 2712630 </td> <td align="center"> 846 </td> </tr>
  <tr> <td> 2016 </td> <td align="center"> 323071755 </td> <td align="center"> 2744248 </td> <td align="center"> 849 </td> </tr>
  <tr> <td> 2017 </td> <td align="center"> 325122128 </td> <td align="center"> 2813503 </td> <td align="center"> 865 </td> </tr>
  <tr> <td> 2018 </td> <td align="center"> 326838199 </td> <td align="center"> 2839076 </td> <td align="center"> 869 </td> </tr>
  <tr> <td> 2019 </td> <td align="center"> 328329953 </td> <td align="center"> 2852609 </td> <td align="center"> 869 </td> </tr>
  <tr> <td> 2020 </td> <td align="center"> 329484123 </td> <td align="center"> 3258883 </td> <td align="center"> 989 </td> </tr>
  </table>

We now have all the data we need to compare the mortality rates obtained from government data with the mortality rates shown in the social media post. Continue to Part 4 to view the results of this comparison.
