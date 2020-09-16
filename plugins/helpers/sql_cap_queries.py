class SqlCAPQueries:
    users_table_insert = ("""
        INSERT INTO users
        SELECT distinct iduser, location, age
        FROM staging_users;
    """)
    
    ratings_table_insert = ("""
        CREATE TEMP TABLE ratings_staging (LIKE ratings);
    
        INSERT INTO ratings_staging
        SELECT distinct
            isbn AS idbookratings,
            isbn AS ISBN,
            CAST(iduser AS INT),
            CAST(bookrating AS INT) AS rating
        FROM staging_ratings ;
    
        INSERT INTO ratings
        SELECT distinct
            md5(rs.ISBN || rs.iduser || rs.rating) AS idbookratings,
            rs.ISBN,
            rs.iduser,
            rs.rating
        FROM (SELECT rs.*
            FROM ratings_staging rs) rs
        LEFT JOIN ratings r
        ON rs.idbookratings = r.idbookratings
        WHERE r.idbookratings IS NULL;
    
        DROP TABLE IF EXISTS ratings_staging;
    """)
    
    yearofpub_table_insert = ("""
        INSERT INTO yearofpub
        SELECT distinct yearofpub, ISBN
        FROM staging_books;
    """)

    authors_table_insert = ("""
        INSERT INTO authors
        SELECT distinct md5(bookauthor) AS idauthor, bookauthor AS authorname
        FROM staging_books;
    """)

    books_author_table_insert = ("""
        INSERT INTO books_author
        SELECT distinct ISBN, md5(bookauthor) AS idauthor
        FROM staging_books;
    """)
  
    titles_table_insert = ("""
        INSERT INTO titles
        SELECT distinct md5(booktitle) AS idTitles, booktitle AS title
        FROM staging_books;
    """)
  
    books_title_table_insert = ("""
        INSERT INTO books_title
        SELECT distinct md5(booktitle) AS idTitles, ISBN
        FROM staging_books;
    """)
  
    publishers_table_insert = ("""
        INSERT INTO publishers
        SELECT distinct md5(publisher) AS idPublishers, publisher
        FROM staging_books;
    """)

    books_publisher_table_insert = ("""
        INSERT INTO books_publisher
        SELECT distinct md5(publisher) AS idPublishers, ISBN
        FROM staging_books;
    """)
