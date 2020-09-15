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

## 1.1 Fact Table
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
