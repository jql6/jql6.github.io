<head>
  <!-- style sheet -->
  <style type = text/css>
    body{
        color: white;
        background-color: rgb(60, 60, 60);
    }

<!-- I don't know why, but both `a` and `a:link` must be changed -->
<!-- to change link colors-->
    a{
        color: rgb(97, 175, 239) !important;
    }

    a:link{
        color: rgb(97, 175, 239) !important;
    }

    a:visited{
        color: rgb(230, 180, 180) !important;
    }

    :is(h1, h2, h3, h4, h5, h6, p) {
        color: white;
    }

    code{
        outline-style: solid;
        outline-color: rgb(160, 160, 160);
        outline-width: 1px;
        outline-offset: 1px;
        background-color: rgb(50, 50, 50);
    }

  </style>
</head>

<!-- omit in toc -->
# PostgreSQL variables, Psycopg2, and using PostgreSQL with Tableau
<!-- omit in toc -->
## Author: Jackie Lu
<!-- omit in toc -->
## Date: 2021, Apr. 2
<br>

<section class="footer">
  <p>
    <a href="https://jql6.github.io/">
      Return to homepage
    </a>
  </p>
</section>

<!-- omit in toc -->
## Table of Contents
- [Intro](#intro)
- [Variables in PostgreSQL](#variables-in-postgresql)
- [Writing SQL queries in Python](#writing-sql-queries-in-python)
- [Setting up a connection between PostgreSQL and Tableau](#setting-up-a-connection-between-postgresql-and-tableau)
- [Summary](#summary)
- [Resources](#resources)

<br>

# Intro
I'll be discussing how to create variables with PostgreSQL, how to convert data frames in Python to SQL tables, and how to set up a connection between Tableau and a local PostgreSQL server.


# Variables in PostgreSQL
I had difficulty getting variables to work in PostgreSQL queries. What I ended up doing was creating functions that return the value that I'm looking for, and then just used the functions in place of variables. Here's an example:

```{postgresql}
/* Function that gets the start date of the fantasy matchup week */
DROP FUNCTION IF EXISTS get_week_start();
CREATE FUNCTION get_week_start() RETURNS date
AS $$
#print_strict_params on
DECLARE
week_start_date date;
BEGIN
    SELECT yahoo_matchups.week_start INTO STRICT week_start_date
        FROM yahoo_matchups LIMIT 1;
    RETURN week_start_date;
END;
$$ LANGUAGE plpgsql;

/* Get the list of games that occur at the start of the fantasy matchup week */
SELECT * FROM nba_schedule
WHERE (gdte = get_week_start())
```

I then found out that single row, single column query results can also work. So for example, this works too:

```{postgresql}
SELECT * FROM nba_schedule
WHERE gdte = (SELECT week_start FROM yahoo_matchups LIMIT 1)
```

You can even temporarily store query results themself with the following syntax:
```{postgresql}
WITH todays_games AS(
    SELECT * FROM nba_schedule
    WHERE gdte = (SELECT week_start FROM yahoo_matchups LIMIT 1)
)
SELECT gdte, stt, home_team FROM todays_games
```


# Writing SQL queries in Python
You can write SQL queries in Python with Psycopg2. Here's some code I modified from [Naysan][1].

```{python}
import psycopg2

login_info = json.load(open("./sql_login.json"))

conn = psycopg2.connect(
    host = login_info["host"],
    database = login_info["database"],
    user = login_info["user"],
    password = login_info["password"]
)

try:
    query1 = ("""
              SELECT * FROM yahoo_matchups
              ORDER BY matchup_number, team_key, stat_type;
              """)
    cursor.execute("""
                   {}
                   """.format(query1))
    conn.commit()
    cursor.close()
except (Exception, psycopg2.DatabaseError) as error:
    print("Error: {}".format(error))
    conn.rollback()
    cursor.close()
```
I modified this code

As you can see, you do this by creating a connection to the SQL database, creating a cursor, executing the queries, then committing them to the database. You can visit my [example sql login json file](https://github.com/jql6/Fantasy_NBA/blob/main/example_sql_login.json) as a template for your own `sql_login.json` file.  

The try and except blocks are important if the query has an error. I found that if there was an SQL error and I didn't have `conn.rollback()`, then Python would hang on the next SQL query that I try to execute.

# Setting up a connection between PostgreSQL and Tableau
You'll need to change the `postgresql.conf` file. For me on MacOS, this is found through `~/Library/Application\ Support/Postgres/var-13/postgresql.conf`. Go to connection settings and uncomment the `listen_addresses` line. Replace the `listen_addresses` line with `listen_addresses = '*'`. Here's [an explanation of what setting `listen_addresses` to `*` does.][2]

Next, in the same folder that contained `postgresql.conf`, search for the `pg_hba.conf` file. Search for "Put your actual configuration here" and look at the non-commented code. You can create a new line and place `host   all              all             all                     md5` underneath the existing rows. This code comes from an answer about [the code for the `pg_hba.conf` file][3].

After doing these steps, you should be able to connect to your local PostgreSQL server with Tableau and start plotting from the database's data.


# Summary
Hopefully this gives some insight into some of the issues I had with PostgreSQL, Python, and Tableau and what solutions I used to solve these issues.


# Resources
[1]: <https://naysan.ca/2020/06/21/pandas-to-postgresql-using-psycopg2-copy_from/> "Try and except blocks for psycopg2"

1. **Try and except blocks for psycopg2**
<br>
https://naysan.ca/2020/06/21/pandas-to-postgresql-using-psycopg2-copy_from/
<br>

[2]: <https://stackoverflow.com/a/9765021> "An explanation of what setting listen_addresses to * does"

2. **An explanation of what setting listen_addresses to * does**
<br>
https://stackoverflow.com/a/9765021
<br>

[3]: <https://stackoverflow.com/a/11754169> "Setting up the pg_hba.conf file"

3. **Setting up the pg_hba.conf file**
<br>
https://stackoverflow.com/a/11754169
<br>