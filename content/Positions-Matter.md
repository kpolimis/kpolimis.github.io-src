---
Author: Kivan Polimis
Category: Projects
Date: '2016-8-1 3:06'
Title: Positions Matter
---

The Combine's Positional Variability in Predicting Career NFL Performance
=========================================================================
collaborators: Long Chen, Melaku Dubie, Rich Lee and Kivan Polimis

## Background
Every year, hundreds of collegiate football players are invited to participate in a week-long scouting combine. Players are evaluated by NFL personnel departments on a series of physical and mental tests. Results from these “measurables” influence positioning in the NFL draft. Our goal with this project was to determine the association between pre-draft metrics and career performance. We Used Python to gather data from online sources (see Additional Information below) and create the plots. The plots show that for some positions, different combine metrics are more important predictors of career NFL performance. 

The example plot below describes the analysis and interactive plotting features.

## Interactive plotting
Press the [![Binder](http://mybinder.org/badge.svg)](http://mybinder.org:/repo/kpolimis/nfl-combine-evaluation-plots){:target="_blank"} link to open a jupyter notebook directory window.
Select plots.ipynb to start an interactive notebook that plots the relationship between assorted Combine
metrics (40 time, vertical, speed score, etc.) and total yards in a NFL career for quarterbacks, running backs and wide receivers. 

Below each metric-specific plot is an explanation of the metric, the goal of the combine test, and a short discussion about variation between positions. LaDainian Tomlinson (highlighted player in example), is an elite running back that demonstrates a strong observed positional relationship between combine metrics and career performance: 

> There appears to be a slight negative relationship between 40 time and yardage for running backs indicating that faster running backs are more likely to have more productive careers. In contrast, there does not appear to be any clearly discernable relationship between yardage and 40 time for wide receivers or quarterbacks, suggesting that success for these positions may be more dependent on other characteristics such as skill, intelligence, or agility. 

Hovering over an individual point on the plot reveals the following information: player name, result in the selected metric, and a combination of career rushing, receiving and passing yards depending on the player's position (selected by changing the tabs in the plot's upper left). Plots can also be zoomed in/out, saved, etc.

## Example Plot 
![rb-plot-example](../../images/rb-plot-example.png)

## Additional Information
### Data Sources
Passing, rushing and receiving data for individual seasons:  
[Pro-football reference](http://www.pro-football-reference.com/years/2015/passing.htm)  
Scouting combine and player database:  
[NFL savant](http://www.nflsavant.com/about.php) 

For more information about this project, visit the [NFL Combine Evaluation Repository](https://github.com/kpolimis/nfl-combine-evaluation) for all relevant code.
In this repository, we have the functions that gather and evaluate the relationship between pre-draft Combine metrics and career NFL performance.
