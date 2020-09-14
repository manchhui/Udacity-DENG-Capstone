DROP TABLE IF EXISTS "staging_users"; 
DROP TABLE IF EXISTS "staging_books"; 
DROP TABLE IF EXISTS "staging_ratings"; 
DROP TABLE IF EXISTS yearofpub ;
DROP TABLE IF EXISTS ratings ;
DROP TABLE IF EXISTS users ;

CREATE TABLE "staging_users" ("iduser" int,
                            "location" varchar(256),
                            "age" real);

CREATE TABLE "staging_books" ("isbn" varchar,
                            "booktitle" varchar(512),
                            "bookauthor" varchar(256),
                            "yearofpub" int,
                            "publisher" varchar,
                            "img_s" varchar(512),
                            "img_m" varchar(512),
                            "img_l" varchar(512));

CREATE TABLE "staging_ratings" ("bookrating" varchar,
                                "isbn" varchar,
                                "iduser" varchar);
                                            
CREATE TABLE IF NOT EXISTS users (
  iduser INT NOT NULL,
  Location VARCHAR(256) NOT NULL,
  Age INT NOT NULL,
  PRIMARY KEY (iduser));
               
CREATE TABLE IF NOT EXISTS ratings (
  idbookratings VARCHAR(256) NOT NULL,
  ISBN VARCHAR(256) NOT NULL,
  iduser INT NOT NULL,
  rating INT NOT NULL,
  PRIMARY KEY (idbookratings),
  FOREIGN KEY (iduser) REFERENCES users (iduser));

CREATE TABLE IF NOT EXISTS yearofpub (
  yearofpub INT NOT NULL,
  ISBN VARCHAR(256) NOT NULL,
  PRIMARY KEY (yearofpub),
  FOREIGN KEY (ISBN) REFERENCES ratings (idbookratings));
                                         
CREATE TABLE IF NOT EXISTS authors (
  idauthor VARCHAR(256) NOT NULL,
  authorname VARCHAR(256) NOT NULL,
  PRIMARY KEY (idauthor));
               
CREATE TABLE IF NOT EXISTS books_authors (
  ISBN VARCHAR(256) NOT NULL,
  idauthor VARCHAR(256) NOT NULL,
  PRIMARY KEY (ISBN),
  FOREIGN KEY (idauthor) REFERENCES authors (idauthor),
  FOREIGN KEY (ISBN) REFERENCES ratings (idbookratings));
                                         
CREATE TABLE IF NOT EXISTS titles (
  idTitles VARCHAR(256) NOT NULL,
  title VARCHAR(512) NOT NULL,
  PRIMARY KEY (idTitles));
               
CREATE TABLE IF NOT EXISTS books_title (
  idTitles VARCHAR(256) NOT NULL,
  ISBN VARCHAR(256) NOT NULL,
  PRIMARY KEY (idTitles),
  FOREIGN KEY (idTitles) REFERENCES titles (idTitles),
  FOREIGN KEY (ISBN) REFERENCES ratings (idbookratings));
                                         
CREATE TABLE IF NOT EXISTS publishers (
  idPublishers VARCHAR(256) NOT NULL,
  publisher VARCHAR(256) NOT NULL,
  PRIMARY KEY (idPublishers));
               
CREATE TABLE IF NOT EXISTS books_publisher (
  idPublishers VARCHAR(256) NOT NULL,
  ISBN VARCHAR(256) NOT NULL,
  PRIMARY KEY (idPublishers),
  FOREIGN KEY (idPublishers) REFERENCES publishers (idPublishers),
  FOREIGN KEY (ISBN) REFERENCES ratings (idbookratings));
