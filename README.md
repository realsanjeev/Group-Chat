# Group-Chat
DBMS project to create a chat group web-application

# DATABASE
| user     |  	 	
|----------|		
| userid   | 		
| username | 		
| password | 		


| group      |
|------------|
| groupid(p) |
| groupname  |
| userid     |

## SQL Join
Consider two tables: `Customers` and `Orders`.

Customers Table:
```
+----+--------------+
| ID | CustomerName |
+----+--------------+
| 1  | John         |
| 2  | Alice        |
| 3  | Bob          |
| 4  | Emma         |
+----+--------------+
```

Orders Table:
```
+--------+------------+
| OrderID| CustomerID |
+--------+------------+
| 101    | 2          |
| 102    | 1          |
| 103    | 3          |
| 104    | 3          |
| 105    | 1          |
+--------+------------+
```

1. INNER JOIN:
The INNER JOIN returns only the rows where there is a match in both tables. It filters out non-matching rows.

Example:

SQL Query:
```sql
SELECT Orders.OrderID, Customers.CustomerName
FROM Orders
INNER JOIN Customers ON Orders.CustomerID = Customers.ID;
```

Result:
```
+--------+--------------+
| OrderID| CustomerName |
+--------+--------------+
| 101    | Alice        |
| 102    | John         |
| 103    | Bob          |
| 104    | Bob          |
| 105    | John         |
+--------+--------------+
```

2. LEFT JOIN (or LEFT OUTER JOIN):
The LEFT JOIN returns all the rows from the left table and the matching rows from the right table. If there is no match in the right table, the result will contain NULL values for the right table columns.

Example:

SQL Query:
```sql
SELECT Customers.CustomerName, Orders.OrderID
FROM Customers
LEFT JOIN Orders ON Customers.ID = Orders.CustomerID;
```

Result:
```
+--------------+--------+
| CustomerName | OrderID|
+--------------+--------+
| John         | 102    |
| Alice        | 101    |
| Bob          | 103    |
| Bob          | 104    |
| John         | 105    |
| Emma         | NULL   |
+--------------+--------+
```

3. RIGHT JOIN (or RIGHT OUTER JOIN):
The RIGHT JOIN returns all the rows from the right table and the matching rows from the left table. If there is no match in the left table, the result will contain NULL values for the left table columns.

Example:

SQL Query:
```sql
SELECT Customers.CustomerName, Orders.OrderID
FROM Customers
RIGHT JOIN Orders ON Customers.ID = Orders.CustomerID;
```

Result:
```
+--------------+--------+
| CustomerName | OrderID|
+--------------+--------+
| Alice        | 101    |
| John         | 102    |
| Bob          | 103    |
| Bob          | 104    |
| John         | 105    |
| NULL         | 106    |
+--------------+--------+
```

4. FULL JOIN (or FULL OUTER JOIN):
The FULL JOIN returns all the rows when there is a match in either the left or right table. If there is no match, the result will contain NULL values for the respective table's columns.

Example:

SQL Query:
```sql
SELECT Customers.CustomerName, Orders.OrderID
FROM Customers
FULL JOIN Orders ON Customers.ID = Orders.CustomerID;
```

Result:
```
+--------------+--------+
| CustomerName | OrderID|
+--------------+--------+
| John         | 102    |
| Alice        | 101    |
| Bob          | 103    |
| Bob          | 104    |
| John         | 105    |
| Emma         | NULL   |
| NULL         | 106    |
+--------------+--------+
```

Note: In this modified example, Customer with ID 4 (Emma) didn't place any orders, resulting in a `NULL` value in the `OrderID` column when using LEFT JOIN, RIGHT JOIN, and FULL JOIN operations.

## GROUP BY clause
In SQL, the `GROUP BY` clause is used to group rows from a table based on the values of one or more columns. It allows you to apply aggregate functions to each group, such as `SUM`, `COUNT`, `AVG`, `MAX`, `MIN`, etc., and perform calculations on the grouped data.

Let's take an example with a table named `Orders`, which contains information about orders placed by customers:

Orders Table:
```
+---------+------------+---------+
| OrderID | CustomerID | Amount  |
+---------+------------+---------+
| 1       | 101        | 100.50  |
| 2       | 102        | 75.20   |
| 3       | 101        | 50.00   |
| 4       | 103        | 30.75   |
| 5       | 102        | 125.80  |
| 6       | 103        | 40.00   |
+---------+------------+---------+
```

Example:

Suppose we want to calculate the total amount spent by each customer. We can use the `GROUP BY` clause to group the data based on the `CustomerID` and then use the `SUM` function to calculate the total amount for each customer.

SQL Query:
```sql
SELECT CustomerID, SUM(Amount) AS TotalAmount
FROM Orders
GROUP BY CustomerID;
```

Result:
+------------+-------------+
| CustomerID | TotalAmount |
+------------+-------------+
| 101        | 150.50      |
| 102        | 201.00      |
| 103        | 70.75       |
+------------+-------------+


Explanation:

In the above query, we selected the `CustomerID` column and used the `SUM(Amount)` function to calculate the total amount spent by each customer. The `GROUP BY CustomerID` clause grouped the data based on the `CustomerID` column, and then the `SUM` function was applied to each group, resulting in the total amount spent by each customer.
