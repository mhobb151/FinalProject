# To use this app:
#   pip install bottle

import bottle
from datetime import datetime
from mysql.connector import connect



def service_exists_at_datetime(d:datetime, c:connect):
        cursor = c.cursor()
        cursor.execute("""SELECT service_id 
                            FROM service 
                            WHERE Svc_DateTime = {}""".format(d))
        if len(cursor.fetchall()) > 0:
            return True
        else:
            return False


def generate_service_dropdown_options(rows):
    options = ""
    for row in rows:
        (ID, dtime, title) = row
        options += "<option value='{}'>{} -- {}</option>".format(ID, str(dtime.date()), title)

    return options


def generate_songleader_dropdown_options(rows):
    options = ""
    for row in rows :
        (ID, name) = row
        options += "<option value='{}'>{}</option>".format(ID, name)

    return options






con = connect(user='root', password='root', database='wsoapp')
cursor = con.cursor()
    
@bottle.get('/')
def hello():

    cursor.execute("SELECT service_id, Svc_DateTime, title FROM service where Svc_DateTime < current_timestamp() order by Svc_DateTime asc")
    service_results = cursor.fetchall()
    service_dropdown = generate_service_dropdown_options(service_results)

    

    cursor.execute("""Select distinct person_id, CONCAT(First_Name, ' ', Last_Name) 
                        FROM Service Join Person on service.Songleader_ID = person.Person_ID
                        WHERE service_ID < current_timestamp();""")
    songleader_results = cursor.fetchall()
    songleader_dropdown = generate_songleader_dropdown_options(songleader_results)

    

    templatefile = open("template.html")
    html_template = templatefile.read()
    templatefile.close()



    return html_template.format(service_dropdown, songleader_dropdown)


@bottle.post('/')
def create():
    return """<!DOCTYPE>
               <html>
               <body>
               <h1>
               POST (MALONE)
               </h1>
               <a href="/">go back tho . . .</a>
               </body>
               </html>"""




@bottle.route('/static/<filename>')
def stylesheets(filename):
    print("STYLESHEET!")
    return bottle.static_file(filename, root='static')



# Launch the BottlePy dev server
if __name__ == "__main__":
    bottle.run(host='localhost', debug=True)
    con.disconnect()

