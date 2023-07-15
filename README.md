# SpaceXLandingClassifier
This repository is a capstone project in the IBM Data Science certification course on Coursera. It showcases my analytical knowledge and abilities in this case study on Space X. Enjoy!

## Background
In this capstone project, I will predict if the Falcon 9 first stage booster rocket will land successfully. On its website, SpaceX advertises Falcon 9 rocket launches at a cost of 62 million dollars. While other providers' launches cost upward of 165 million dollars each, much of the savings is attributable to SpaceX's reuse of rockets. The main purpose of trying to predict the success (or failure) of the launches is to gain insight on the cost of SpaceX launches. By doing this, we hope to be able to model SpaceX's contract bids on new launches going forward so as to assist other companies that are also making competing bids. 

## Executive Summary

## Methodology
### Data Collection - SpaceX API 
*Requested launch data from SpaceX API
*Decoded response using .json() and convert to a dataframe using .json_normalize()
*Requested information about the launches from SpaceX API using custom functions
*Created lists from the data
*Created a dataframe from the lists
*Filtered the dataframe to contain only Falcon 9 launches
*Replaced missing values of Payload Mass with calculated mean of the column
*Classified the landings as boolean for success or failure in a new column "Class" from "Outcome" column
*Exported dataframe to csv file

### Data Collection - SpaceX Wikipedia Falcon 9 Launch Page
*Requested data from Wikipedia Falcon 9 rocket launches page
*Createed a BeautifulSoup object from HTML response
*Extracted column names from HTML table header
*Collected data from parsing HTML tables
*Created dictionary from the data
*Create dataframe from the dictionary
*Classified the landings as boolean for success or failure in a new column "Class_verification" from "landing outcome" column
*Export data to csv file
