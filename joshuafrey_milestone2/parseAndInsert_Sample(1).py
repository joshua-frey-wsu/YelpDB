import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def insert2BusinessTable():
    #reading the JSON file
    
    with open('C:\Cpts451\Yelp-CptS451\yelp_business.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='yelpdb2' user='postgres' host='localhost' port='5432' password='Sho1303Jo$h'")
            print('Connected to DB')
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the cussent business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            sql_str = "INSERT INTO Business(business_id, name, address, state, " \
                      "city, zipcode, latitude, longitude, stars, reviewRating, review_count, " \
                      "open_status, num_checkins) " \
                      "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + \
                      cleanStr4SQL(data["name"]) + "','" + cleanStr4SQL(data["address"]) \
                      + "','" + cleanStr4SQL(data["state"]) + "','" + \
                      cleanStr4SQL(data["city"]) + "','" + cleanStr4SQL(data["postal_code"]) \
                      + "'," + str(data["latitude"]) + "," + str(data["longitude"]) + "," + \
                      str(data["stars"]) + ",0.0 ," + str(data["review_count"]) + "," + \
                      int2BoolStr(data["is_open"]) + ",0);"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to businessTABLE failed!")
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2ReviewTable():
    # reading the JSON file
    with open('C:\Cpts451\Yelp-CptS451\yelp_review.JSON','r') as f:    #TODO: update path for the input file
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='yelpdb2' user='postgres' host='localhost' port='5432' password='Sho1303Jo$h'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            sql_str = "INSERT INTO Review(review_id, user_id, business_id, stars, date, " \
                            "cool, funny, useful, text) " \
                            "VALUES ('" + cleanStr4SQL(data['review_id']) + "','" + \
                            cleanStr4SQL(data["user_id"]) + "','" + cleanStr4SQL(data["business_id"]) \
                            + "'," + str(data["stars"]) + ",'" + cleanStr4SQL(data["date"]) + "'," + \
                            str(data["cool"]) + "," + str(data["funny"]) + "," + \
                            str(data["useful"]) + ",'" + cleanStr4SQL(data["text"]) + "');"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to review table failed!")
            conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

def insert2CategoriesTable():
    # reading the JSON file
    with open('C:\Cpts451\Yelp-CptS451\yelp_business.JSON','r') as f:    #TODO: update path for the input file
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='yelpdb2' user='postgres' host='localhost' port='5432' password='Sho1303Jo$h'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            for val in data['categories']:
                sql_str = "INSERT INTO Categories (category_name, business_id) " \
                          "VALUES ('" + cleanStr4SQL(val) + "', '"  + data['business_id'] + "');"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to categories table failed!")
            conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

def insert2CheckinTable():
    print("Parsing checkins...")
    #reading the JSON file
    with open('C:\Cpts451\Yelp-CptS451\yelp_checkin.JSON','r') as f:  # Assumes that the data files are available in the current directory. If not, you should set the path for the yelp data files.
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='yelpdb2' user='postgres' host='localhost' password='Sho1303Jo$h'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        # read each JSON object and extract data
        while line:
            data = json.loads(line)
            business_id = str(cleanStr4SQL(data['business_id']))
            for day in data['time']:
                count = 0
                for hour in data['time'][day]:
                    if hour in ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']:
                        count += data['time'][day][hour]

                sql_str = "INSERT INTO CheckIn(business_id, day, count) VALUES ('" + \
                                  str(business_id) + "','" + str(day) + "'," + str(count) + ");"
                try:
                    cur.execute(sql_str)
                except:
                    print("Insert to checkin table failed!")
                conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()
    print(count_line)
    f.close()

#insert2BusinessTable()
#insert2ReviewTable()
insert2CategoriesTable()
#insert2CheckinTable()  