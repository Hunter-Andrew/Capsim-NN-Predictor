# Capsim-CSS-Calculator

By: Andrew Hunter

Project Duration/Timeline: April 2023 to May 2023

## Executive Summary:

Using data from a business simulation called Capsim, the goal of this project is to predict a product's Customer Survey Score (CSS) using given product parameters. The data is extracted from Fast Track reports (specifically pages 5 and 6) using a Python script. Additional attributes/parameters are also derived from this data. The simulation/game has several mechanics and rules essential to understanding how the CSS is calculated, including reasons to eliminate some rows and columns, as well as the reasons 2 models were trained and used, depending on the row's segment. After building and testing the models, it was concluded that the desired prediction accuracy was not achieved, but valuable lessons were learned that will assist in further refining the models in the future.

## Purpose/Context: 

Overall Project Goal: Predict a product's CSS

A few years ago I took an Introduction to Business course (COMM 200) where we competed against our classmates in a business simulation, each team being a company in the simulation. The simulation was called Capsim Foundation, where each team has to make a variety of decisions each round, where a round is equivalent to an in-game year. Since this is a turn-based game, your company can't make any decisions during the year, only at the beginning of each year. 

Being able to precisely and accurately predict your products' market share was incredibly useful, part of the decisions you had to make, was a lower and upper bound for how many units you planned on selling. If the actual number of units sold was lower than the lower bound you predicted, then you wouldn't have as much cash flow as you predicted, likely causing you to take a mandatory emergency loan with a high interest rate. If the actual number of units sold was high than the upper bound you predicted, you wouldn't produce enough units and your product would go out of stock, losing potential profit. Finally, the tighter your bounds are, the more cash flow you'll have that year. If your bounds are very loose, you'll sit on cash that you could've used to invest in your business. Therefore, being able to predict tight bounds for your products' market share can be very beneficial.

The simulation gives a perfectly accurate way to calculate a product's market share: Take that product's Customer Survey Score (CSS), and divide it by the sum of all product's CSS'. A product's CSS is based on many factors, including the product's performance (pfmn), size, price, MTBF (reliability), and age. Furthermore, you can spend money on marketing to increase the customers' awareness of the product, as well the product's accessibility to the customers. But, how the CSS is calculated using these parameters is mostly a mystery. I did try to analyze the data without AI techniques during the simulation, but I had little success. That's why I wanted to see if I could create an AI model now (after the simulation has concluded) to predict a product's CSS using data from the simulation. To clarify, while predicting a product's market share is the underlying motivator for this project, calculating a product's CSS is the goal of this project, as this is what I struggled to predict during the simulation. Calculating a product's market share is beyond the scope of this project, although it's easy enough to do manually using this project as a tool to calculate a product's CSS.

While this project is based on a course project I did in the past, **this is a personal project that I was not graded on**. This project was started after the course and simulation had concluded.

## Rules and Other Information about Capsim:

Each company can have as many products as they want. You can tell which company owns a product because of the starting letter of the product name. For example, my company name is Ferris, so all my products' names will start with an "F", for example: Fast, Far, Fun, etc. 

There are 2 different "segments", the low tech segment and the high tech segment. The low tech segment consists of customers who want a cheap and reliable product, with performance and size not being their focus. The high tech segment consists of customers who want the newest and best performance and size they can get, while willing to sacrifice price and reliability to an extent. It should also be noted that one product can get a market share in both segments. A product can be very specialized towards the low tech segment, but still get a very small market share from the high tech segment. In contrast, a product could try to be generalized trying to get a medium market share in both the high and low tech segment. This also means that a product will have 2 separate CSSs, one for the low segment, and one for the high segment.

Each segment has its own ideal parameters. The low segment prefers products that are 3 years old, while the high segment prefers products that are 0 years old. Any deviations from these ideal values will diminish the CSS for that segment. The ideal price range for the low segment is $15-35, while the ideal price range for the high segment is $25-45. It should also be noted that while a range is given, lower prices in that range are better, but it's unclear exactly how the CSS is affected if the price goes outside of the given range. Furthermore, the price is 41% important to the low segment, while it is only 25% important to the high tech segment, which is consistent with the segments' preferences. 

The product's performance and size are combined to create the "position" parameter, which is a 2d vector consisting of the performance and size. Each segment has an ideal position, with the distance between the product's position and the ideal position affecting the CSS score. Unlike other parameters, the segment's ideal position shifts in a predictable and given manner over time, that is, the ideal position changes to have a high performance, and a lower size as time passes. 

It should be quickly noted that a product's CSS changes over the course of a year, because of both the shifting ideal position, and the product's changing age as time passes. A product's market share is actually based on all the instantaneously calculated CSSs throughout the year, but this is beyond the scope of this project. Furthermore, the CSSs given in the data (fast tracks) are based on the product's parameters on December 31. For the purposes of this project, the CSS on December 31 is what will be used, which should also be able to accurately predict CSS at other times of the year. 

## Extracting the Data:

The data given is presented in pdf files given at the end of each round during the simulation called the Fast Track. Specifically, we're interested in pages 5 and 6, as they contain the top products in that segment, what their parameters are, and the CSS. In the simulation, there were 3 practice rounds to get us familiar with the game, then we restarted everything to go on to the 8 competitive rounds. The fast tracks can be found [here](./fasttracks). 

While I could manually enter the information from these tables into a useable format for python or a csv file, this would take a long time both when making the project, as well as for any users that want to use the model created in this product to predict their product(s)'s CSS. So instead, I copied and pasted the tables from the fast tracks into a text file, where I then created a python script [extract_data.py](./extract_data.py) to extract the information from the text file and put it into a 2d  numpy array. 

In extract_data.py, I also add some new attributes that I think will help the model learn, for example, the difference between the actual and ideal age, rather than making the model figure out the ideal age on its own. A detailed description of all attributes meaning (both already given attributes and newly created attributes) can be found in [attribute descriptions](./attribute_descriptions.md). Finally, I also added some other functionality to this file such as loading a dataset from a csv file instead, and writing the dataset to a csv file. 

## Preprocessing:

Done in the [predict_css.py](./predict_css.py) file. Other than splitting the dataset into training and test data, I deleted some of the data for various reasons:

It seemed like if a product stocked out, then the CSS would be unpredictably higher. My guess is that if a product has a low supply then the increased demand for the product increased the CSS. However, going back to the use of this product, the user shouldn't plan for their product to go out of stock, and whether or not any other companies' products go out of stock can't be predicted, so it's not overly useful to be able to predict a product's CSS if it goes out of stock since it isn't a given parameter. For this reason, I've removed all rows where the product is stocked out.

A product's name and revision date aren't relevant to the product's CSS, so those columns were removed.

A product's market share and units sold are dependent on the product's CSS and all other products' CSS, not the other way around. A product's CSS is independent of the product's market share and units sold. Furthermore, the product's market share and units sold aren't known until after the round, so you couldn't use them to predict the CSS anyways, so these 2 columns are also removed.

Finally, I split the data into low segment data and high segment data, choosing to train 2 separate models for each. The reason is that despite including the product's segment as an attribute, the model wasn't able to properly account for the product's segment. Overall, I achieved better results when I split them into 2 separate models. I think the biggest difference between the low and high segments is the weightings of importance between different parameters. For example, the importance of the price, age, MTBF, and position for the low segment is 41%, 29%, 21%, and 9% respectively, which is different for the high segment (see fast track page 6). I didn't know how to tell the model of these importances especially since there are parameters other than these 4 that affect the CSS (ex. customer awareness), so I just let the models figure these weights out on their own. 

## Building the Model:

Done in the [predict_css.py](./predict_css.py) file.

I used the tensorflow keras sequential library to build the model. I used mean squared error as the loss function, mean absolute error as the metric, and the adam optimizer. I used L1L2 regularization to help prevent overfitting, as well as a 0.8 learning rate. I used a linear activation function for the output layer, and the relu activation function for all other layers. 

I definitely think the model architecture and hyperparameters could be better, to more accurately predict the CSS, as it's not as accurate as I was hoping for, but this was my first project using tensorflow, with little other experience using neural networks. I do want to come back to this project in the future to try and increase the prediction accuracy. 

Calling the build function in [predict_css.py](./predict_css) also tests both models, and automatically saves them in the local directory. This function will also write the test data predicted CSS, along with the segment and actual CSS to the [test_results.csv](./test_results.csv) file, so you can compare the actual and predicted CSS values. 

## Conclusion:

I'm not yet satisfied with the prediction accuracy of this model yet, but after extensive testing of different model architectures and hyperparameters, I've decided to publish what I've done so far, with the intent to further refine the architecture, hyperparameters, and possibly input attributes in the future. There are a couple of factors that make training this model rather difficult: In total, I only have just over 200 records to use for both training and test data, which is definitely on the lower side of dataset sizes, especially for the complexity of the calculating the CSS, along with my desired prediction accuracy. Another factor to consider is that I have no idea how the simulation actually calculates CSSs. Is there an element of randomness to prevent students from predicting the CSS? Are there other necessary input parameters that aren't given and can't be extracted from the given input parameters? 

However, despite not achieving the desired prediction accuracy, I have gained a lot of knowledge throughout this project. This was my first time using tensorflow, and other than a few heavily professor assisted neural network assignments, I didn't have a lot of experience in using neural networks, especially in choosing the architecture and hyperparameters, which is a skill/art that I plan to continue developing. I've also become more comfortable with extracting, formatting, and manipulating data.
