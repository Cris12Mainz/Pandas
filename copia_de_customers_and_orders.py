import pandas as pd

url = 'https://raw.githubusercontent.com/anyoneai/notebooks/main/customers_and_orders/data/customers.csv'
customers = pd.read_csv(url, delimiter = ',')
#print(customers)

"""
# Exercise 1: Processing Customers data (difficulty medium)

The sample customer data in 'customers.csv' file has just 5 columns: CustomerId, First Name, Last Name, City and State


**Question 1:** How many customers are in the file?
"""

#There are some Customer IDs repeated in the table, so we drop rows with the same ID, First and Last Name.
clean_customers = customers.drop_duplicates(subset=['LastName', 'FirstName','CustomerID'])
print(len(customers))
#print(clean_LN_FN_customers)
print("There are", len(clean_customers), "customers.")

"""**Question 2:** In how many different states do the customers live in?"""

# Let us drop the rows that are repeated in the "states" column and the length on this table would be how many different states there are.
clean_states_customers = customers.drop_duplicates(subset=['State'])
print(clean_states_customers)
print("There are", len(clean_states_customers)-1, "different states.")#because "one" CA is taken as different of the other CAs

"""**Question 3** What is the state with most customers?"""

state_count = clean_customers.pivot_table(index = ['State'], aggfunc ='size')
print(state_count)
print("\n There is an interesting behaivor because one -CA- is considered as a different state")
print("\nCA has the most customers with 447 customers.")

"""**Question 4** What is the state with the least customers?"""

print(state_count)

print("IN, MA, NH, NM and WA have the least customers with 1 customers.")

"""**Question 5:** What is the most common last name?"""

LastName_count = clean_customers.pivot_table(index = ['LastName'], aggfunc ='size')
print(LastName_count)
print("\nThe most common last name is Abraham with 2 customers.")

"""# Exercise 2: Processing Orders data (difficulty high)

The second sample files contains orders placed by customers from the first file. Be careful, this file has many rows and you most likely should not print the contents of the whole file.

The file contains the following columns: CustomerID, OrderID, Date, OrderTotal, ProductName, Price

![Data sample](https://raw.githubusercontent.com/anyoneai/notebooks/main/customers_and_orders/images/orders.png)

*Hint:* We advise you to take a look at the data before you start.
**if you want to manually take a look at the data before you start, please see the content of the data [here](https://raw.githubusercontent.com/anyoneai/notebooks/main/customers_and_orders/data/orders.csv).

*Hint*: There are many ways to do this exercise you can do your own, although here's some help. You can solve this exercise reading and parsing CSV files, structuring data into dictionaries, and using for loops to navigate the contents

*Hint*: Also, the data is not clean and you will have to figure out how to deal with that data from the code, without having to modify the data source.



**Question #1:** How many unique orders are in the orders.csv file?

**Question #2:** What is the average number of items per order (rounded to two decimal places)?

**Question #3:** What is the highest number of items per order?

**Question #4:** What is the number of orders placed in October 2021?

**Question #5:** Which customer spent the most amount of money in 2021?

**Question #6:** Historically, what is the best month for sales?

Once you get your answers, remember to go back to the course and introduce them in the multiple choice quiz
"""

import pandas as pd

url = 'https://raw.githubusercontent.com/anyoneai/notebooks/main/customers_and_orders/data/orders.csv'
clean_orders = pd.read_csv(url, delimiter = ',')
#print(len(orders))
#Let us first clean the data of repeated rows
#clean_orders = orders.drop_duplicates(subset=['CustomerID', 'OrderID','ProductName','OrderTotal','Price'])#Dropping the rows that are repeated
#clean_orders = orders.drop_duplicates()
#clean_orders = orders.drop_duplicates(subset=['OrderID','ProductName'])#one OrderID can have more than one product
#print(len(clean_orders))
clean_ID_orders = clean_orders.drop_duplicates(subset=['OrderID'])#unique order IDs
#print(len(clean_ID_orders))
print("\n Question #1: How many unique orders are in the orders.csv file?\n" "There are", len(clean_ID_orders), "unique orders.")

############################ Questions 2 ###################################
ProductNum = clean_orders['OrderTotal'].sum() #Total amount of ordered products
Avg = round(ProductNum/len(clean_ID_orders),2)
#print(ProductNum)
#print(Avg)
print("\n Question #2: What is the average number of items per order (rounded to two decimal places)?\n" "The average number of items per order is", Avg)

############################ Questions 2 ###################################
print(len(clean_orders))
print(len(clean_ID_orders))
Avg = round(len(clean_orders)/len(clean_ID_orders),2)
print("\n Question #2: What is the average number of items per order (rounded to two decimal places)?\n" "The average number of items per order is", Avg)

############################ Questions 3 ###################################
orders_sort=clean_orders.sort_values(by=['OrderID'],ascending=False)
clean_order = orders_sort.reset_index() #reseting the index from 0 to 23360
print(clean_order)
number = []
j= 0
if j < len(clean_order)-1:
  number.append(1)
for i in range(1,len(clean_order)):
  if clean_order.loc[i, 'OrderID'] == clean_order.loc[i-1,'OrderID']:
    number.append(number[-1]+1)
  else:
    number.append(1)
clean_order.insert(7,'number',number)
print(clean_order)
total_max = max(number)
#print("\n", total)
print("\n Question #3: What is the highest number of items per order?\n" "The highest number of items per order is", total_max)

############################ Questions 4 ###################################

clean_order["Date"] = pd.to_datetime(clean_order["Date"])  #This line converts the 'Date' column to datetime objects
clean_order['Month'] = clean_order['Date'].dt.month
clean_order['Year'] = clean_order['Date'].dt.year
print(clean_order)

number=0
for i in range(len(clean_orders)):
  if clean_order.loc[i, 'Year'] == 2021:
    if clean_order.loc[i, 'Month'] == 10:
      number=number+1
print("\n Question #4: What is the number of orders placed in October 2021?\n" "The number of orders placed in October 2021 is",number)

############################ Questions 5 ###################################
#print(clean_order)
clean_orders_sort=clean_order.sort_values(by=['CustomerID'],ascending=False) #ordering by Customer ID numbers
clean_order = clean_orders_sort.reset_index(drop=True) #reseting the index from 0 to 23360

print(clean_order)
amount = []
ID = []
j = 0
if j < len(clean_order)-1:
  amount.append(clean_order.loc[0,'Price'])
  ID.append(clean_order.loc[0,'CustomerID'])
for i in range(1,len(clean_order)):
  if clean_order.loc[i, 'Year'] == 2021:
    if clean_order.loc[i, 'CustomerID'] == clean_order.loc[i-1, 'CustomerID']:
      amount.append(clean_order.loc[i,'Price'] + amount[-1])
      ID.append(clean_order.loc[i,'CustomerID'])
    else:
      amount.append(clean_order.loc[i,'Price'])
      ID.append(clean_order.loc[i,'CustomerID'])
print(amount)
print(max(amount))




#print(clean_order)
total = []
ID=[]
j= 0
##### Brandon Divas
total.append(0)

for i in range(0,len(clean_order)):
  if clean_order.loc[i, 'Year'] == 2021:
    if clean_order.loc[i, 'CustomerID'] == 5172443:
      total.append(clean_order.loc[i,'Price'] + total[-1])
print(total)

##### Raul Herrera
total1=[]
total1.append(0)

for i in range(0,len(clean_order)):
  if clean_order.loc[i, 'Year'] == 2021:
    if clean_order.loc[i, 'CustomerID'] == 5415408:
      total1.append(clean_order.loc[i,'Price'] + total1[-1])
print(total1)


##### Sophie Labonte
total2=[]
total2.append(0)

for i in range(0,len(clean_order)):
  if clean_order.loc[i, 'Year'] == 2021:
    if clean_order.loc[i, 'CustomerID'] == 1909369:
      total2.append(clean_order.loc[i,'Price'] + total2[-1])
print(total2)


##### Frances Marquez
total3=[]
total3.append(0)

for i in range(0,len(clean_order)):
  if clean_order.loc[i, 'Year'] == 2021:
    if clean_order.loc[i, 'CustomerID'] == 5172680:
      total3.append(clean_order.loc[i,'Price'] + total3[-1])
print(total3)


##### Kenneth Jones
total4=[]
total4.append(0)

for i in range(0,len(clean_order)):
  if clean_order.loc[i, 'Year'] == 2021:
    if clean_order.loc[i, 'CustomerID'] == 4700014:
      total4.append(clean_order.loc[i,'Price'] + total4[-1])
print(total4)


#total_ID_sort=total_ID.sort_values(by=['total'],ascending=False)
#print(total_ID_sort.reset_index())
print("\n Question #5: Which customer spent the most amount of money in 2021? \n" "The customer is Brandon Divas with the ID -> 5172443 with 7675.0 soles")
print("It is weird because they are just summing the prices and not considering the number of products was ordered")

############################ Questions 6 ###################################
clean_order["Date"] = pd.to_datetime(clean_order["Date"])  #This line converts the 'Date' column to datetime objects
clean_order_sort=clean_order.sort_values(by=['Date'],ascending=True) #ordering by Customer ID numbers
#clean_order = clean_order_sort.reset_index() #reseting the index from 0 to 23360
#print(clean_order)
clean_order['Month_Year'] = clean_order['Date'].dt.to_period('M')
#print(clean_order)
# Now we have to find the best month over the years. Similar to question 5


total = []
time = []
j=0
if j < len(clean_order)-1:
  total.append(clean_order.loc[0,'OrderTotal']*clean_order.loc[0,'Price'])
  time.append(clean_order.loc[0, 'Month_Year'])


for i in range(1,len(clean_order)):
  if clean_order.loc[i,'Month_Year'] == clean_order.loc[i-1,'Month_Year']:
    #total.append(clean_order.loc[i,'OrderTotal'])
    total.append(clean_order.loc[i,'Price'] + total[-1])
    time.append(clean_order.loc[i,'Month_Year'])
  else:
    total.append(clean_order.loc[i,'Price'])
    time.append(clean_order.loc[i, 'Month_Year'])

#print(time)
#print(total)

d = {'total': total, 'month': time}
total_month = pd.DataFrame(d)
#print(total_ID)
total_month_sort=total_month.sort_values(by=['total'],ascending=False)
print(total_month_sort.to_string())
print("\n Question #6: Historically, what is the best month for sales? \n" "The best month is January of 2022 with 17463290.0 currency of incoming")

"""
# Finished!

Hope this was not too difficult and slicing and dicing the datasets was some fun. Now head on back to the course and provide the answers to the questions from this exercise."""
