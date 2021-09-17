########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = True

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "dhislop3"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = "CREATE TABLE movies(id integer, title text, score real);"
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = "CREATE TABLE movie_cast(movie_id integer, cast_id integer, cast_name text, birthday text, popularity real);"
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################
        cur = connection.cursor()
        a_file = open("./data/movies.csv")
        rows = csv.reader(a_file)
        cur.executemany("INSERT INTO movies VALUES (?, ?, ?)", rows)
        connection.commit()
       ######################################################################
        
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        cur = connection.cursor()
        a_file = open("./data/movie_cast.csv")
        rows = csv.reader(a_file)
        cur.executemany("INSERT INTO movie_cast VALUES (?, ?, ?, ?, ?)", rows)
        connection.commit()
        ######################################################################
        
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = "CREATE TABLE cast_bio(cast_id integer, cast_name text, birthday text, popularity real);"
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql = "INSERT INTO cast_bio (cast_id, cast_name, birthday, popularity) SELECT er.cast_id, er.cast_name, er.birthday, er.popularity FROM movie_cast er GROUP BY er.cast_id;"
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = "CREATE INDEX movie_index ON movies(id);"
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = "CREATE INDEX cast_index ON movie_cast(cast_id);"
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = "CREATE INDEX cast_bio_index ON cast_bio(cast_id);"
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        #part_c_sql = "SELECT count(*) FROM movies WHERE score > 50 AND title like '%war%'"
        part_c_sql = """SELECT  printf("%.2f", 100.0 * (chosen / total)) AS pro from (SELECT (SELECT count(*) FROM movies)*1.0 AS total, (SELECT count(*) FROM movies WHERE score > 50 AND title like '%war%')*1.0 AS chosen)"""
        #part_c_sql = "select count(*) from movies AS total, (select count(*) from movies where score > 10) AS chosen;"
        ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = "select cast_name, count(*) as appearance_count from movie_cast WHERE popularity > 10 group by cast_name order by appearance_count desc, cast_name asc limit 5;"
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        #That being said, a few things to check are that: the movie score is formatted to two decimal places after sorting, that the columns are returned in the right order, and that the result is limited to 5 rows. Hope that helps!
        part_e_sql = """SELECT m.title as movie_title, printf("%.2f", m.score) as movie_score, count(c.cast_id) as cast_count FROM movies m INNER JOIN movie_cast c ON m.id = c.movie_id group by m.title order by score desc, cast_count ASC, title ASC LIMIT 5;"""
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = """SELECT c.cast_id as cast_id, c.cast_name as cast_name, printf("%.2f", avg(m.score)) as average_score FROM movies m INNER JOIN movie_cast c ON m.id = c.movie_id   WHERE m.score >= 25 group by cast_id HAVING count(c.movie_id) > 2 AND avg(m.score) >= 25 order by avg(m.score) desc, cast_name ASC LIMIT 10;"""
        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    #SELECT movie_id, DISTINCT cast_member_id1, cast_member_id2 FROM (SELECT c1.movie_id AS movie_id, c1.cast_id AS cast_member_id1, c2.cast_id AS cast_member_id2 FROM movie_cast AS c1 LEFT JOIN movie_cast AS c2 ON c1.movie_id = c2.movie_id WHERE c1.cast_id != c2.cast_id AND c1.cast_id = 539)
    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = """CREATE VIEW good_collaboration AS SELECT  c1.cast_id AS cast_member_id1, c2.cast_id AS cast_member_id2, count() AS movie_count, printf("%.2f", avg(m.score)) AS average_movie_score FROM movie_cast AS c1 INNER JOIN movie_cast AS c2 ON c1.movie_id = c2.movie_id AND c1.cast_id < c2.cast_id LEFT JOIN movies m on m.id = c1.movie_id WHERE c1.cast_id != c2.cast_id  GROUP BY c1.cast_id, c2.cast_id HAVING count() >= 3 AND avg(m.score) >= 40;"""
        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql = """select DISTINCT(x.cast_member)AS cast_id, c.cast_name, x.collaboration_score FROM (select cast_member_id1 AS cast_member, printf("%.2f",avg(average_movie_score)) AS collaboration_score from good_collaboration  GROUP BY cast_member UNION select cast_member_id2 AS cast_member, printf("%.2f",avg(average_movie_score)) AS collaboration_score  from good_collaboration  GROUP BY cast_member) x LEFT JOIN movie_cast c on c.cast_id = x.cast_member ORDER BY collaboration_score DESC, cast_name ASC  LIMIT 5;"""
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = "CREATE VIRTUAL TABLE movie_overview USING fts3(id integer, overview text)"
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        cur = connection.cursor()
        a_file = open("./data/movie_overview.csv")
        rows = csv.reader(a_file)
        cur.executemany("INSERT INTO movie_overview VALUES (?, ?)", rows)
        connection.commit()
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = "SELECT count(*) FROM movie_overview WHERE overview MATCH 'fight';"
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = "SELECT count(*) FROM movie_overview WHERE overview MATCH 'space NEAR/5 program';"
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    print("HI ")
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except:
        print("Error in Table Drops")

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except:
         print("Error in Part a.i")

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except Exception as e:
        print("Error in part a.ii", e)

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except:
        print("Error in part a.iii")

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except:
        print("Error in part b")

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except Exception as e:
        print("Error in part c", e)

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except Exception as e:
        print("Error in part d", e)

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part e", e)

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part f", e)
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part g", e)

    try:   
        print('\033[32m' + "part h.i: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.iii: " + '\033[m' + str(db.part_hii(conn)))
    except Exception as e:
        print("Error in part h", e)

    conn.close()
    #################################################################################
    #################################################################################
  
