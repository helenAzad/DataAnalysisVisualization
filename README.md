# DataAnalysisVisualization
design a robot to work with digital currencies

In this project, we want to design a robot to work with digital currencies.
Our cryptocurrency robot has different parts with different functions. Also, this robot saves all the obtained information in CSV, TXT, JSON files to access them for future use. (To use csv files, you must use data frames from the pandas library, and for json files, you can use any desired library.)
The robot has the following parts.

## 1- Adding a currency:
Two methods can be used to add currency.
First method: enter the name of the password
Second method: enter the currency symbol
After adding each name by the user, the correctness of the existence of the associated currency must be checked. For this, you can get help from the search on the mentioned sites or the list of currencies in the exchanges or... but you cannot save the names of the currencies in advance in the program and it must be done online. (One of the possible methods is to search in the list of passwords on the first few pages of a site, of course, to use the method, you must note it as the default.) If there is a successful addition message, otherwise, the appropriate report message. do.

## 2- Viewing the price of cryptocurrency:

To view the price of one or more currencies, first select the desired currencies from the list of available currencies added in the previous section. (The list of available currencies must be shown to the user.) After selecting the desired currencies, their prices will be received online and along with the exact time (date + hour + minute + second) the price will be shown to the user in alphabetical order. Show the alphabet. To see the price of cryptocurrency, you should pay attention to the following:
The display of selected currencies should be in the form of a table with the exact time of each one. (The name of the currency must be accompanied by its symbol.)
The price list, date and desired currency should be loaded as a data frame and saved in CSV files to be used at the right time. (How to manage and save CSV files is up to you, and it is important to run the files correctly and at a suitable speed.)

## 3- View the chart of changes of a currency:
The user should be able to view the graph of developments checked by the bot with the help of previously stored data related to a specific currency and loading them. When viewing changes, you should pay attention to the following:

After selecting the name of the desired currency from the stored list, only the previously available information stored (offline) is checked and we do not need any new online data. If there is no data for a currency, the appropriate message will be displayed.

If there is more than one price for a currency in a one-hour period, only one data point which is the average of the available values ​​will be shown, and in the stored data, all the stored states will be deleted and the average value will be replaced. (to calculate the interval) You can use any formula you want, for example, 24-hour time periods can be a suitable option, and the average minutes can be obtained by dividing the number of minutes by the sum of minutes.
The output graph can be with the help of matplotlib library or other libraries, but you must be careful that the time and price graph is accurate and with appropriate data points and labels for the graph and axes.

## 4- Favorite list:

This list contains some of the currencies included in the general list, which are of interest to the user, and there should be the ability to add, display and delete currencies from this list.
The way to display and store this list is not important, and it should only meet the requirements of the question and be saved in a way that can be retrieved after closing and re-running the list of favorite passwords.)

## 5- Checking the daily chart and comparing currencies:
By selecting one or more currencies from the list and selecting the desired daily time frame, the user should be able to see the daily evolution of currencies and then the best currency will be offered to him. To implement this feature, pay attention to the following:
The time period is the number of days from the current day to the previous day. (Like 10, which refers to the price of the cryptocurrency in the last 10 days.) The maximum value will be 30.
The number of selected currencies for comparison will be maximum 6.

Getting the information of the previous days must be done online and you cannot use the information of the previous parts in this part. But if this operation has already been done, the program should use the saved information related to the same part that it received in the previous execution. (The program first checks whether it has already received and saved the information of the desired days for the desired currency or not. If it finds the desired information, it uses them, and otherwise it goes to receive online.) (It is clear that if part of the desired data is available and the rest is not available, you can only download the non-available data from the Internet and complete the data.)

The information received in each step should be loaded and stored by the data frame to be used for later times. The way to record information is arbitrary, but you should note that at least the symbol, date, and price information need to be stored, and you may need to store something else or not.

The price chart in the past days should be drawn in one of the 3 forms: Boxplot, Fill_between, or Step.

In the boxplot and fill_between models, the lowest and highest daily cryptocurrency prices are considered as high and low levels.
If the sum of the percentage changes of consecutive days in a currency (the days when the price has fallen is a negative percentage and the days when the price has increased compared to the previous day is a positive percentage) compared to other currencies, that currency is considered as Recommend the suggested currency for purchase to the user and show the sum of the final percentage changes of each currency to the user.

Be careful, the robot must have the ability to return to the previous stage or home at each stage. Also, as long as no currency is added, if the other parts are selected, it will show the appropriate message of the absence of currency.
Also, the robot must save its important information, such as the names of the added currencies, etc., in appropriate files so that it can continue to work every time it is turned off and on, and there is no need for initialization.

