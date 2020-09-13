DROP TABLE IF EXISTS "staging_users"; 
DROP TABLE IF EXISTS "staging_books"; 
DROP TABLE IF EXISTS "staging_ratings"; 

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
