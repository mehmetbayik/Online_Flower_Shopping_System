
-- 1) Find ename and bname for employees who work in a branch located in Ankara. 
-- Order the list in ascending employee name within branch name.

SELECT e.ename, b.bname
FROM Employee e, Branch b
WHERE e.branch_id = b.branch_id AND b.city = 'Ankara'
ORDER BY e.ename, b.bname;

-- 2) Find name and birthdate of employees who are older than their branch’s manager. 

SELECT e.ename, e.birthdate
FROM Employee e, Branch b
WHERE e.branch_id = b.branch_id AND e.birthdate <  (SELECT e.birthdate 
                                                    FROM Employee e, Branch b
                                                    WHERE e.SSN = b.manager_SSN);

-- 3) Find branch_id and name of branches which has female employees only

SELECT b.branch_id, b.bname
FROM Branch b, Employee e
WHERE b.branch_id = e.branch_id AND b.branch_id NOT IN (SELECT e.branch_id 
                                                        FROM Employee e
                                                        WHERE e.gender = 'M');
GROUP BY b.branch_id, b.bname;

-- 4) Find name of customer whose has more money in their accounts than their loans 
-- (Hint: compare sum of balance and sum of loan for customer)

SELECT c.cname 
FROM Customer c
WHERE c.cust_id IN 
    (SELECT c.cust_id
     FROM Customer c, Account a, Loan l
     WHERE c.cust_id = a.cust_id AND c.cust_id = l.cust_id AND SUM(a.balance) > SUM(l.amount));

-- 5) For each branch, find branch_id, branch name and total amount of money deposited.

SELECT b.branch_id, b.bname, SUM(a.balance)
FROM Branch b, Account a
WHERE b.branch_id = a.branch_id
GROUP BY b.branch_id, b.bname;

-- 6) Find minimum, maximum and average salary for each job title where at least there are 10 employees with that job title

SELECT job_title, MIN(salary), MAX(salary), AVG(salary)
FROM Employee
GROUP BY job_title
HAVING COUNT(*) >= 10;

-- 7) Find branch name and manager’s name of branches which has at least 50 accounts with a balance higher than 1,000,000 TL

SELECT b.bname, e.ename
FROM Branch b, Employee e
WHERE b.manager_SSN = e.SSN AND b.manager_SSN IN 
    (SELECT b.manager_SSN
     FROM Branch b, Employee e, Account a
     WHERE b.branch_id = e.branch_id AND b.branch_id = a.branch_id AND a.balance > 1000000 
     GROUP BY b.manager_SSN 
     HAVING COUNT(*) >= 50)

-- 8) Find name of customers who have account in a branch located in a city where they don’t live (hint: compare cities)

SELECT c.cname
FROM Customer c, Account a, Branch b
WHERE c.cust_id = a.cust_id AND a.branch_id = b.branch_id AND c.city != b.city;
GROUP BY c.cname;

-- 9) Find name, hiredate and birthdate of employees who were older than 30 years when they joined the bank.
-- (Hint: strftime('%Y', date)function returns the year part of a date as integer in SQLite)

SELECT ename, hiredate, birthdate
FROM Employee
WHERE (strftime('%Y', hiredate) - strftime('%Y', birthdate)) > 30;

-- 10) Find name of employees who work in the same branch with the employee(s) who has the highest salary

SELECT ename
FROM Employee
WHERE branch_id IN  
    (SELECT branch_id 
     FROM Employee 
     WHERE salary = (SELECT MAX(salary) FROM Employee));
