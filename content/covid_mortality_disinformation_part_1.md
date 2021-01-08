---
Title: COVID-19 Mortality and Disinformation
Date: 2021-01-07 1:51
author: Kivan Polimis
Category: Tutorials
---

# Covid Mortality and Disinformation (Part 1)
Recently, I was scrolling through social media when I saw a post that gave me pause. The social media post is presented below:

<img src="images/social_media_mortality_data_screenshot.png" alt="COVID-19 Mortality Data from Social Media">

The post caught my attention for three reasons: it presented a falsifiable hypothesis, the conclusion was counter-intuitive, and there was an obvious challenge issued. Anyone reading this knows that falsifiable hypotheses are exciting because they deal with evidence and once we agree on the evidence, some hypothesis can be disproven with evidence. Here the falsifiable hypothesis is also the counter-intuitive conclusion, namely that COVID-19 has not affected mortality rates in the United States ("Nothing abnormal [about 2020 mortality rates], corona is like the flu"). What really spurred this blog post to be written was the message being sent in the last sentence of the blog post and the associated references below the table. The implicit challenge was that given data sources, one could also determine that mortality rates had not changed in the U.S. or other countries. As Barney Stinson would say, "Challenge Accepted!"

This blog represents the first in a multi-part series to investigate the COVID-19 mortality claims made on social media. To understand changes in U.S. mortality over time, we need to gather (1): U.S. mortality data and (2): U.S population data. Then, we need to create mortality rates with these data sources. Lastly, we need to compare the mortality rates from the social media post to the mortality data obtained from government sources. In this post we gather the mortality data.

Government mortality and population data is available via the open data portal [Socrata](https://www.tylertech.com/products/socrata). You can sign up for a Socrata account [here](https://support.socrata.com/hc/en-us/articles/115004055807-Signing-up-for-an-Account) and create a developer application to programmatically download Socrata data by following these [instructions](https://support.socrata.com/hc/en-us/articles/210138558-Generating-an-App-Token)

Once you have established your Socrata Developer credentials, you can leverage an R package that connects to the Socrata API called [RSocrata](https://cran.r-project.org/web/packages/RSocrata/index.html)

First, let's load the libraries we will need for the analysis
``` {.r}
library(here)
library(yaml)
library(RSocrata)
library(tidyverse)
```

Then let's bring in our Socrata credentials from a local file called `socrata_app_credentials.yml`:

``` {.r}
socrata_app_credentials = yaml.load_file(here("credentials/socrata_app_credentials.yml"))
```

contents of `socrata_app_credentials.yml`:
``` {.r}
app_token: "APP_TOKEN"
email: "EMAIL"
password: "PASSWORD"
```


Then we get weekly state mortality data from 2018-2020
``` {.r}
#' Weekly Counts of Deaths by State and Select Causes, 2014-2018NCHS
weekly_deaths_by_state_2014_2018 <- read.socrata(
  "https://data.cdc.gov/resource/3yf8-kanr.json",
  app_token = socrata_app_credentials$app_token,
  email = socrata_app_credentials$email,
  password  = socrata_app_credentials$password
)
```

We follow that up with the weekly state mortality data from 2019-2020
``` {.r}
#' https://data.cdc.gov/NCHS/Weekly-Counts-of-Deaths-by-State-and-Select-Causes/muzy-jte6
#' Weekly Counts of Deaths by State and Select Causes, 2019-2020
weekly_deaths_by_state_2019_2020 <- read.socrata(
  "https://data.cdc.gov/resource/muzy-jte6.json",
  app_token = socrata_app_credentials$app_token,
  email = socrata_app_credentials$email,
  password  = socrata_app_credentials$password
)
```

Quick glimpse at the data
``` {.r}
#glimpse(weekly_deaths_by_state_2014_2018)
glimpse(weekly_deaths_by_state_2019_2020)
```

Combine the 2014-2018 data with the 2019-2020 data and perform some pre-processing like renaming and subsetting columns
``` {.r}
weekly_deaths_2014_2020 = weekly_deaths_by_state_2014_2018 %>%
  select(jurisdiction_of_occurrence, mmwryear, allcause, naturalcause, weekendingdate) %>%
  rename('state_name'='jurisdiction_of_occurrence', 'all_cause'='allcause', 'natural_cause'='naturalcause',
         'year'='mmwryear', 'week_ending_date' = 'weekendingdate') %>%
  mutate(week_ending_date = as.character(week_ending_date)) %>%
  rbind(weekly_deaths_by_state_2019_2020 %>%
          rename('state_name'='jurisdiction_of_occurrence', 'year'='mmwryear') %>%
          select(state_name, year, all_cause, natural_cause, week_ending_date)) %>%
  arrange(state_name, year)

```

This data contains mortality data for more than just U.S. states (specifically, national data, Puerto Rico data and data from New York city). We want to filter to only data in the 50 states and the District of Columbia. Create a variable leveraging the `R` built-in `state.name` to create a list of all state names and the District of Columbia and filter weekly mortality data with this list

``` {.r}
state.name_dc = c(state.name, "District of Columbia")
state.abb_dc = c(state.abb, "DC")
```

Create two filtered data sets. One with only weekly State (and District of Columbia) data and another data set with only weekly mortality data

``` {.r}
weekly_deaths_by_state_2014_2020 = weekly_deaths_2014_2020 %>%
  filter(state_name  %in% state.name_dc)

weekly_deaths_by_national_2014_2020 = weekly_deaths_2014_2020 %>%
  filter(state_name== "United States")
```

Create yearly mortality data for states and national data set
``` {.r}
yearly_deaths_by_state_2014_2020 = weekly_deaths_by_state_2014_2020 %>%
  group_by(state_name, year) %>%
  mutate(all_cause_deaths = sum(as.numeric(all_cause), na.rm = TRUE),
         natural_cause_deaths = sum(as.numeric(natural_cause), na.rm = TRUE)) %>%
  select(state_name, year, all_cause_deaths, natural_cause_deaths) %>%
  distinct()

yearly_deaths_by_national_2014_2020 = weekly_deaths_by_national_2014_2020 %>%
  group_by(state_name, year) %>%
  mutate(all_cause_deaths = sum(as.numeric(all_cause), na.rm = TRUE),
         natural_cause_deaths = sum(as.numeric(natural_cause), na.rm = TRUE)) %>%
  select(state_name, year, all_cause_deaths, natural_cause_deaths) %>%
  distinct()
```
