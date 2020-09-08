# Udacity Data Engineering Nanodegree Programme - Capstone Project

## Introduction
An online book store company, Valdivian,  wants to analyse the data they've been collecting on books and user ratings of these specific books from their app and online website. The analytics team is particularly interested in understanding which books users rate the most, and the data scientists are interested in using machine learning algorithms to develop a book recommendation system. Currently, they don't have an easy way to query their data, which resides in a directories containing a CSV file on user data, JSON logs of user ratings and another CSV file of metadata on books.

They want to implement a data warehouse which is designed to optimise queries on user rating analysis, additionally, the ETL pipelines are to be high-grade data pipelines that:
* Are automated and easily monitored. 
* Are dynamic and built from reusable tasks.
* Have automated data quality checks that catch any discrepancies in the datasets.

#### Source Data
The source data resides on AWS S3 and needs to be processed in Valdivian's data warehouse which resides on Amazon Redshift. The source datasets consist of JSON file of logs that tell them about users **ratings** of books on their store, CSV files that hold **users** information, and CSV metadata about the **books** the are available on the store.

* **s3://udacity-capstone-project-828/ratings**: data book ratings, example of row '0' of the data as follows:
  `{'Book-Rating': 0, 'ISBN': '034545104X', 'User-ID': 276725}`

* **s3://udacity-capstone-project-828/users**: data about artists and songs, example of row '0' of the data as follows:
  `{'User-ID': 1, 'Location': 'nyc, new york, usa', 'Age': nan}`

* **s3://udacity-capstone-project-828/books**: data of logs of usage of the app, example of row '0' of the data as follows:
  `{'ISBN': '0195153448', 'book_title': 'Classical Mythology', 'book_author': 'Mark P. O. Morford', 'year_of_publication': '2002', 'publisher': 'Oxford University Press', 'img_s': 'http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg', 'img_m': 'http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg', 'img_l': 'http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg'}`

#### Project Technologies
A brief description of each of the three core technologies that is used in this project:
> Amazon Simple Storage Service is storage for the Internet. It is designed to make web-scale computing easier for developers. **Amazon S3** has a simple web services interface that you can use to store and retrieve any amount of data, at any time, from anywhere on the web. [aws.amazon.com](https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html)

> **Amazon Redshift** is a fully managed, petabyte-scale data warehouse service in the cloud. You can start with just a few hundred gigabytes of data and scale to a petabyte or more. This enables you to use your data to acquire new insights for your business and customers. [aws.amazon.com](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html)

> **Apache Airflow** is an open-source workflow management platform. It started at Airbnb in October 2014 as a solution to manage the company's increasingly complex workflows. Creating Airflow allowed Airbnb to programmatically author and schedule their workflows and monitor them via the built-in Airflow user interface. From the beginning, the project was made open source, becoming an Apache Incubator project in March 2016 and a Top-Level Apache Software Foundation project in January 2019. [Wikipedia](https://en.wikipedia.org/wiki/Apache_Airflow)

<br/>

## 1. Database Design Description
The data from the three source datasets, described above, will be used to create the following snowflake schema database for optimized queries on book ratings:

![](https://github.com/manchhui/Udacity-DENG-Capstone/blob/master/F306E320-C567-4E03-90F1-8C34CAF13778.jpeg)
