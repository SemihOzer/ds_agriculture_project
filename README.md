# Data Science Agricultural Products' Price Estimator: Project Overview
* Created a tool that estimates agricultural products to help sellers or consumers who trade from different markets.
* Scraped over 2M price for about 200 products from [marketing information system](http://webapps.daff.gov.za/amis/amis_price_search.jsp).
* Optimized Linear, Losso, and Random Forest Regressors using GridsearchCV to reach the best model.
* Built a client facing API using flask.

## Data Collection

Datasets are scrapped from [marketing information system](http://webapps.daff.gov.za/amis/amis_price_search.jsp) with Python Selenium library. With each product , we got the following:
* Variety
* Class
* Size
* Package
* Unit
* Price
* Total Sales
* Sales Quantity
* Closing Stock
* Market

You can use data collection script for any product you want.

## Data Cleaning
After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:

* Dropped rows that have missing values.

* Price, Total Sales and Unit columns are converted to int data type.

* Market columns are renamed.

* Variety, Class, Size, Package and Market columns are converted to category data type.

* Added a column for kilogram price.

## EDA
I looked at the distributions of the data and the value counts for the various categorical variables. Below are a few highlights from the pivot tables.

![Alt text](https://github.com/SemihOzer/ds_agriculture_project/blob/315ad9d218d0d9c1314c3e60186f9de4740c536a/eda_tables/Screenshot%202023-08-24%20at%2020.02.54.png)
![Alt text](https://github.com/SemihOzer/ds_agriculture_project/blob/315ad9d218d0d9c1314c3e60186f9de4740c536a/eda_tables/Screenshot%202023-08-24%20at%2020.03.07.png)
![Alt text](https://github.com/SemihOzer/ds_agriculture_project/blob/315ad9d218d0d9c1314c3e60186f9de4740c536a/eda_tables/Screenshot%202023-08-24%20at%2020.03.22.png)


## Model Building
First, I transformed the categorical variables into dummy variables. I also split the data into train and tests sets with a test size of 20%.

I tried three different models and evaluated them using Mean Absolute Error. I chose MAE because it is relatively easy to interpret and outliers aren’t particularly bad in for this type of model.

I tried three different models:

* Multiple Linear Regression – Baseline for the model
* Lasso Regression – Because of the sparse data from the many categorical variables, I thought a normalized regression like lasso would be effective.
* Random Forest – Again, with the sparsity associated with the data, I thought that this would be a good fit.

## Model Performance
The Random Forest model far outperformed the other approaches on the test and validation sets.

* Random Forest : MAE = 0.46
* Linear Regression: MAE = 3.25
* Lasso Regression: MAE = 2.67

## Productionization
In this step, I built a flask API endpoint that was hosted on a local webserver by following along with the TDS tutorial in the reference section bottom. The API endpoint takes in a request with a list of values from a product listing and returns an estimated price.

## Code and Resources Used
Python Version: 3.7

Packages: pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle

Flask Productionization: [Document](https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2)

The tutorial that I follow while working on this project: [Tutorial](https://www.youtube.com/watch?v=MpF9HENQjDo&list=PL2zq7klxX5ASFejJj80ob9ZAnBHdz5O1t&ab_channel=KenJee)
