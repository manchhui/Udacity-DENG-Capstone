# Udacity Data Engineering Nanodegree Programme - Capstone Project

## Introduction
An online book store company, Valdivian,  wants to analyse the data they've been collecting on books and user ratings of these specific books from their app and online website. The analytics team is particularly interested in understanding which books users rate the most, and the data scientists are interested in using machine learning algorithms to develop a book recommendation system. Currently, they don't have an easy way to query their data, which resides in a directories containing a CSV file on user data, JSON logs of user ratings and another CSV file of metadata on books.

They want to implement a data warehouse which is designed to optimise queries on user rating analysis, additionally, the ETL pipelines are to be high-grade data pipelines that:
* Are automated and easily monitored. 
* Are dynamic and built from reusable tasks.
* Have automated data quality checks that catch any discrepancies in the datasets.

#### Source Data
The source data resides on AWS S3 and needs to be processed in Valdivian's data warehouse which resides on Amazon Redshift. The source datasets consist of JSON file of logs that tell them about users **ratings** of books on their store, CSV files that hold **users** information, and CSV metadata about the **books** the are available on the store.

* **s3://udacity-capstone-project-828/ratings**: data about book ratings, example of row '0' of the data as follows:
  `{'Book-Rating': 0, 'ISBN': '034545104X', 'User-ID': 276725}`

* **s3://udacity-capstone-project-828/users**: data about users, example of row '0' of the data as follows:
  `{'User-ID': 1, 'Location': 'nyc, new york, usa', 'Age': nan}`

* **s3://udacity-capstone-project-828/books**: data books available from this store, example of row '0' of the data as follows:
  `{'ISBN': '0195153448', 'book_title': 'Classical Mythology', 'book_author': 'Mark P. O. Morford', 'year_of_publication': '2002', 'publisher': 'Oxford University Press', 'img_s': 'http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg', 'img_m': 'http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg', 'img_l': 'http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg'}`

#### Project Technologies & Rationale
A brief description of each of the three core technologies that is used in this project and the rationale behind each choice:
> **Description**: Amazon Simple Storage Service is storage for the Internet. It is designed to make web-scale computing easier for developers. **Amazon S3** has a simple web services interface that you can use to store and retrieve any amount of data, at any time, from anywhere on the web. [aws.amazon.com](https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html). 

> **Description**: **Amazon Redshift** is a fully managed, petabyte-scale data warehouse service in the cloud. You can start with just a few hundred gigabytes of data and scale to a petabyte or more. This enables you to use your data to acquire new insights for your business and customers. [aws.amazon.com](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html). 

> **Description**: **Apache Airflow** is an open-source workflow management platform. It started at Airbnb in October 2014 as a solution to manage the company's increasingly complex workflows. Creating Airflow allowed Airbnb to programmatically author and schedule their workflows and monitor them via the built-in Airflow user interface. From the beginning, the project was made open source, becoming an Apache Incubator project in March 2016 and a Top-Level Apache Software Foundation project in January 2019. [Wikipedia](https://en.wikipedia.org/wiki/Apache_Airflow).

> **Rationale**: With a potential for 100x increase in data and hundreds of concurrent users querying the data, from the current approximately one million rows or a few hundred megabytes of data and tens of users, Amazon Redshift coupled with S3 storage and Airflow is the preferred solution going forward. The technology itself is easily scalable removing the need for Valdivian to manage onsite infrastructure, amd therefore can quickly scale up or down computational resources and allow robust ETL pipelines to be built and maintained with ease.

<br/>

## 1. Database Design Description
The data from the three source datasets, described above, will be used to create the following snowflake schema database for optimized queries on book ratings:

![](https://github.com/manchhui/Udacity-DENG-Capstone/blob/master/21EE3C3C-9D3F-43AA-8EC0-A09BCAC3EA57.jpeg)

### 1.1 Fact Table
The fact table in this snowflake scheme will be named "ratings" and is designed to record "ratings" data of books from various users. The following is: `Row 0 '{'idbookratings': 'c2ad834c9e62bdc0067c4ad4081bc491', 'isbn': '0440214041', 'iduser': 181077, 'rating': 0}' of the FACT table 'ratings'`
- idbookratings: Hash of **concatenation** of `isbn' & 'isuser' & 'rating`, to form a unique id for each rating.
- isbn: unique number of each book.
- iduser: unique number for each user.
- rating: rating of by user `iduser` of book `isbn`.


### 1.2 Dimension Tables
The following tables in this snowflake scheme are all dimension tables.
- users - This table will be used to record unique user details. The following is: `Row 0 '{'iduser': 533, 'location': 'london, england, united kingdom', 'age': 31}' of DIMENSION table 'users'
  - iduser: Unique user id.
  - location: Location of the user.
  - age: Age of user, `-1` is used to represent NaN values found in the source data.

- yearofpub - This table will be used to record books (identified via their isbn) that are published in each year. The following is: `Row 0 '{'yearofpub': 1974, 'isbn': '0800706544'}' of DIMENSION table 'yearofpub'`
  - yearofpub: Year as the index.
  - isbn: Unique number for each book.

- books_publisher - This table will be used to record, the number of `ISBN's` for each unique `idpublisher`. The following is: `Row 0 '{'idpublishers': 'cd47a7d6631d514987e4b09da9e71841', 'isbn': '0865050880'}' of DIMENSION table 'books_publisher'`
  - idpublishers: Hash of `publisher`, to form a unique id for each publisher.
  - isbn: Unique number for each book.

- publishers - This table will be used to record unique publisher details. The following is: `Row 0 '{'idpublishers': '9af8b47d680fdeb68d9d26cfaaba70b3', 'publisher': 'Bantam Books'}' of DIMENSION table 'publishers'`
  - idpublishers: Hash of `publisher`, to form a unique id for each publisher.
  - publisher: Publisher name.

- books_author - This table will be used to record the number of `idauthor` for each unique `ISBN`. The following is: `Row 0 '{'isbn': '8445071769', 'idauthor': '153e43074eabeb5d58200def94650acd'}' of DIMENSION table 'books_author'`
  - isbn: Unique number for each book.
  - idauthor: Hash of `authorname`, to form a unique id for each author.

- authors - This table will be used to record unique author details. The following is: `Row 0 '{'idauthor': '1f96f4fd318463bfbff78f45b2691a2d', 'authorname': 'Richard Bruce Wright'}' of DIMENSION table 'authors'`
  - idauthor: Hash of `authorname`, to form a unique id for each author.
  - authorname: Author name.

- books_title -  This table will be used to record the number of `ISBN's` for each unique `idTitle`. The following is: `Row 0 '{'idtitles': '6beeacd4188d25601b22f0073d164f88', 'isbn': '0553280333'}' of DIMENSION table 'books_title'`
  - idtitles: Hash of `title`, to form a unique id for each book title.
  - isbn: Unique number for each book.

- titles -  This table will be used to record unique book title details. The following is: `Row 0 '{'idtitles': '6a9934e08ff5b352fda9c7ed7428f302', 'title': 'Modern Manners: An Etiquette Book for Rude People'}' of DIMENSION table 'titles'`
  - idtitles: Hash of `title`, to form a unique id for each book title.
  - title: Book title.

<br/>

## 2. Files in the repository
There are three source datasets, one called "users", another called "books" and another "ratings" and these are located on the AWS S3 bucket as detailed in the introduction above. Within the root of this repository is a few .jpegs which are used in this README plus "Capstone Project.ipynb" which forms part of the submission to explain the through processes that have gone into this project. 

Finally the following subsections contain brief descriptions of the rest of the files in this repository: 

### 2.1 Files within "/dags" folder:
#### 2.1.1 create_capstone.py
This **dag** must be used first before the **main dag** "udac_capstone_dag.py"

#### 2.1.2 udac_sl_etl_dag.py
This **main dag** contains all the operator calls and task dependencies to correctly perform ETL of the data from AWS S3 into the fact and dimension tables on AWS Redshift. , refer to the diagram below for the details of task dependencies.

![](https://github.com/manchhui/Udacity-DENG-Capstone/blob/master/55F1A69C-CFD1-4AF6-B9CE-21527459BFF8.jpeg)

Furthermore the default parameters are as below:
* The DAG does not have dependencies on past runs
* On failure, the task are retried 3 times
* Retries happen every 5 minutes
* Catchup is turned off
* Do not email on retry

### 2.2 Files within "/plugins/operators/" folder:
#### 2.2.1 stage_cap_redshift.py
This python script is the stage operator and loads any JSON formatted, song and log, files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided by the **main dag** "udac_capstone_dag.py" that calls this operator.

Additionally this operator contains a backfill feature that can load specific timestamped log files from S3 based on the execution time of the dag.

#### 2.2.2 load_cap_dimension.py
This python script is the dimension operator and it utilises the **sql_cap_queries.py** helper file to run data transformations. Dimension loads are loaded, based on the parameters provided by the **main dag** "udac_capstone_dag.py", with the truncate-insert pattern where the target table is emptied before the load. However a parameter exists that allows switching between insert mode or append mode when loading dimensions. 

#### 2.2.3 fact_cap_dimension.py
This python script is the fact operator and it utilises the **sql_cap_queries.py** helper file to run data transformations. Fact loads are loaded as append mode only.

#### 2.2.4 data_cap_quality.py
The final operator is the data quality operator, which is used to run checks on the data itself. The operator's main functionality is to receive perform SQL based tests to ensure data has been copied and exists in each of the fact and dimension tables. The test result and expected result are checked and if there is no match, the operator will raise an exception.

### 2.3 File within "/plugins/helpers/" folder:
#### 2.3.1 sql_cap_queries.py
This is called by the fact and load operators to perform ETL from the users, ratings and books staging tables to each of the fact and dimension tables.

<br/>

## 3. User Guide
### 3.1 Setup Airflow
To use the Airflow's UI you must first configure your AWS credentials and connection to Redshift.

> ##### 1. To go to the Airflow UI:
> * From within the Udacity Project Workspace, click on the blue Access Airflow button in the bottom right.
> * If you run Airflow locally, open http://localhost:8080 in Google Chrome (other browsers occasionally have issues rendering the Airflow UI).

> ##### 2. Click on the Admin tab and select Connections.
> ![](https://github.com/manchhui/Udacity-DENG-P5-Airflow/blob/master/89E90931-37D2-4163-8D8C-937C7957B2D0_4_5005_c.jpeg)

> ##### 3. Under Connections, select Create.
> ![](https://github.com/manchhui/Udacity-DENG-P5-Airflow/blob/master/97F8D006-16BD-4446-B045-1717375552E1_4_5005_c.jpeg)

> ##### 4. On the create connection page, enter the following values:
> * Conn Id: Enter aws_credentials.
> * Conn Type: Enter Amazon Web Services.
> * Login: Enter your Access key ID from the IAM User credentials you downloaded earlier.
> * Password: Enter your Secret access key from the IAM User credentials you downloaded earlier.

> Once you've entered these values, select Save and Add Another.

> ##### 5. On the next create connection page, enter the following values:
> * Conn Id: Enter redshift.
> * Conn Type: Enter Postgres.
> * Host: Enter the endpoint of your Redshift cluster, excluding the port at the end. You can find this by selecting your cluster in the Clusters page of the Amazon Redshift console. See where this is located in the screenshot below. IMPORTANT: Make sure to NOT include the port at the end of the Redshift endpoint string.
> * Schema: Enter dev. This is the Redshift database you want to connect to.
> * Login: Enter awsuser.
> * Password: Enter the password you created when launching your Redshift cluster.
> * Port: Enter 5439.
> Once you've entered these values, select Save.

### 3.2 Running "udac_capstone_dag.py"
* Start the Airflow web server. 
* Once the Airflow web server is ready, access the Airflow UI. 
* First you MUST run "create_capstone.py" before "udac_capstone_dag.py" to ensure all the staging, fact and dimension tables are created before data can be loaded into them.

