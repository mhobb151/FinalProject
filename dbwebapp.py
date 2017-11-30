# To use this app:
#   pip install bottle

import bottle
from datetime import datetime
from mysql.connector import connect

con = connect(user='root', password='root', database='wsoapp')
cursor = con.cursor()
    
@bottle.route('/')
def hello():

    cursor.execute("""
    select * FROM Person;""")

    # Retrieve results
    result = cursor.fetchall()


    resultstring = ""
    for row in result:
        resultstring += str(row) + "<\br>"
        
    return """<html><body>
        {0}</body></html>""".format(
            resultstring)

# Launch the BottlePy dev server
if __name__ == "__main__":
    bottle.run(host='localhost', debug=True)

