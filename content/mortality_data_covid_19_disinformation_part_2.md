---
Title: Mortality Data and COVID-19 Disinformation - Part 2
Date: 2021-01-11 08:10
author: Kivan Polimis
Category: Tutorials
---

# Mortality Data and COVID-19 Disinformation - Part 2

In the [previous post](http://kivanpolimis.com/mortality-data-and-covid-19-disinformation-part-1.html) we used [RSocrata](https://cran.r-project.org/web/packages/RSocrata/index.html) to download mortality data from the [National Center for Health Statistics](https://www.cdc.gov/nchs/about/50th_anniversary.htm) (NCHS) from 1999 to 2020.

The goal of this post is to pair the mortality data with population data from the same time period to create mortality rates. [Mortality rates](https://en.wikipedia.org/wiki/Mortality_rate) (also known as death rates) are a scaled metric that capture the amount of deaths in a population. Typically that scaled population expresses the deaths per 1,000 or 100,000 people in the population (e.g., the U.S. mortality rate in 2000 was 854 deaths per 100,000 residents). We will combine 3 [Census](https://www.census.gov/about/what.html) datasets to get U.S. population estimates from 1999 to 2020.

* load libraries
``` {.r}
library(here)
library(tidyverse)
```

Use the `readr` package (part of the [Tidyverse](https://www.tidyverse.org/packages/)) to go from census urls of .csv data to create data frames of census data

* census urls
``` {.r}
national_pop_1999_url = "https://www2.census.gov/programs-surveys/popest/datasets/1990-2000/intercensal/national/us-est90int-07-1999.csv"
national_pop_2000_2010_url = "https://www2.census.gov/programs-surveys/popest/datasets/2000-2010/intercensal/national/us-est00int-alldata-5yr.csv"
national_2010_2020_pop_url = "https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/national/totals/nst-est2020.csv"
```

* create data frames from census urls and do some column pre-processing
``` {.r}
national_pop_1999 = read_csv(national_pop_1999_url, skip = 3,
                             col_names = c("date", "age_group", "total_population",
                                           "male_population", "female_population"),
                             col_types = cols(date  = col_date("%B %d, %Y")))
national_pop_2000_2010 = read_csv(national_pop_2000_2010_url)
national_pop_2010_2020 = read_csv(national_2010_2020_pop_url)
```

We know the column names of the `national_pop_1999` dataframe because we manually added them. What are the column names for other population data?
``` {.r}
names(national_pop_2000_2010)
names(national_pop_2010_2020)
```


```
##  [1] "SUMLEV"            "REGION"            "DIVISION"         
##  [4] "STATE"             "NAME"              "CENSUS2010POP"    
##  [7] "ESTIMATESBASE2010" "POPESTIMATE2010"   "POPESTIMATE2011"  
## [10] "POPESTIMATE2012"   "POPESTIMATE2013"   "POPESTIMATE2014"  
## [13] "POPESTIMATE2015"   "POPESTIMATE2016"   "POPESTIMATE2017"  
## [16] "POPESTIMATE2018"   "POPESTIMATE2019"   "POPESTIMATE2020"
```

Let's do some pre-processing and [reshaping of the data](https://www.tutorialspoint.com/r/r_data_reshaping.htm) to create a wide data set. Typically, record entry is done using a long data format where multiple variables are stored in one column. However, when analyses need to be performed on long data in a sequential way, for instance, in a time-series, the data needs to be wide. Wide data has each variable occupy it's own column instead of sharing a column as in long data.

* pre-process and reshape data by selecting last month of data in 1999 and all age groups
``` {.r}
national_pop_1999_wide = national_pop_1999 %>%
  filter(date=="1999-12-01" & age_group=="All Age") %>%
  mutate(state_name = "United States") %>%
  rename("pop_estimate_1999"="total_population") %>%
  select(state_name, pop_estimate_1999)
```

* pre-process 2000 to 2010 data by filtering on age group that encompasses the entire population
``` {.r}
national_pop_2000_2010_filtered = national_pop_2000_2010 %>%
  group_by(year) %>%
  filter(AGEGRP==0) %>%
  rename("value"="TOT_POP") %>%
  mutate(state_name="United States", variable = paste("pop_estimate", year, sep="_")) %>%
  slice(1) %>%
  ungroup() %>%
  select(state_name, variable, value)

```

* use `reshape` library to transform 2000 to 2010 census data from long to wide format
``` {.r}
national_pop_2000_2010_wide = reshape2::dcast(national_pop_2000_2010_filtered,
                                              state_name  ~ variable,
                                              value.var = "value", fun.aggregate = sum)

```

* subset 2010 to 2020 data to include on US data and rename columns to match 1999 to 2010 data
* subset will be in wide form
``` {.r}
national_pop_2010_2020_wide = national_pop_2010_2020 %>%
  filter(NAME %in% "United States") %>%
  rename("state_fips" = "STATE",  "state_name" = "NAME", "census_estimate_2010" = "CENSUS2010POP",
         "base_estimate_2010" = "ESTIMATESBASE2010", "pop_estimate_2010" = "POPESTIMATE2010",
         "pop_estimate_2011" = "POPESTIMATE2011", "pop_estimate_2012" = "POPESTIMATE2012",
         "pop_estimate_2013" = "POPESTIMATE2013", "pop_estimate_2014" = "POPESTIMATE2014",
         "pop_estimate_2015" = "POPESTIMATE2015", "pop_estimate_2016" = "POPESTIMATE2016",
         "pop_estimate_2017" = "POPESTIMATE2017", "pop_estimate_2018" = "POPESTIMATE2018",
         "pop_estimate_2019" = "POPESTIMATE2019", "pop_estimate_2020" = "POPESTIMATE2020") %>%
  select(state_fips:pop_estimate_2020)
```

* combine all 3 census population data sets into one wide data set of 1999 to 2020 population data. select only columns available across all 3 population data sets
``` {.r}
national_1999_2020_pop_wide = cbind(national_pop_1999_wide,
                                    national_pop_2000_2010_wide %>% select(-state_name),
                                    national_pop_2010_2020_wide %>% select(-state_fips:-pop_estimate_2010))
```

* View of population data from 1999 to 2020

```
##      state_name pop_estimate_1999 pop_estimate_2000 pop_estimate_2001
## 1 United States         280466621         281424600         284968955
##   pop_estimate_2002 pop_estimate_2003 pop_estimate_2004 pop_estimate_2005
## 1         287625193         290107933         292805298         295516599
##   pop_estimate_2006 pop_estimate_2007 pop_estimate_2008 pop_estimate_2009
## 1         298379912         301231207         304093966         306771529
##   pop_estimate_2010 pop_estimate_2011 pop_estimate_2012 pop_estimate_2013
## 1         308745538         311583481         313877662         316059947
##   pop_estimate_2014 pop_estimate_2015 pop_estimate_2016 pop_estimate_2017
## 1         318386329         320738994         323071755         325122128
##   pop_estimate_2018 pop_estimate_2019 pop_estimate_2020
## 1         326838199         328329953         329484123
```

In the [next post](http://kivanpolimis.com/covid-19-mortality-and-disinformation-part-3.html) we will combine the mortality and population data to create mortality rates.
