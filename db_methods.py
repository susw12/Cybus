import sqlite3, requests, time, random

conn = sqlite3.connect('teenhacks.db', check_same_thread = False)

c = conn.cursor()

APP_KEY = "34d4f83429cfe1e57b09c59ad3f4c886"
APP_ID = "22e4f2a8"

def setup():
    #product table
    #id - food id
    #name - food name
    #tag - food tag
    #desc - food description
    #cid - company id
    #link - food link
    c.execute('''create table if not exists products (id text, price text, name text, tag text, desc text, cid text, link text, zip text, county text)''')
    #company table
    #cid - company id
    #name - company name
    #uname - username
    #psw - password
    #phone/email - contact info
    c.execute('''create table if not exists companies (cid text, name text, uname text, psw text, phone text, email text, zip text, county text, state text)''')
    #student table
    #sid - student id
    #name - student name
    #uname - username
    #psw - password
    #uni - university
    #gid - group id
    c.execute('''create table if not exists students (sid text, name text, uname text, psw text, uni text, zip text, county text, state text, gid text)''')
    #master group table
    #gid - group id
    #gname - group name
    c.execute('''create table if not exists master_groups (gid, gname)''')
    conn.commit()
    

def genID(l=[]):
    while True:
        s = ''
        for i in range(7):
            t = random.randint(0,2)
            if (t == 0):
                s += chr(ord('0') + random.randint(0, 9))
            elif (t == 1):
                s += chr(ord('a') + random.randint(0, 25))
            else:
                s += chr(ord('A') + random.randint(0, 25))
        if (s not in l):
            l.append(s)
            return s

def get_link(name):
    name = name.strip().replace(' ', "%20")
    link = 'https://api.edamam.com/api/food-database/parser?nutrition-type=logging&ingr={}&app_id={}&app_key={}'.format(name, APP_ID, APP_KEY)
    return link

def get_nutrients(link):
    response = requests.get(link)
    r = response.json()
    return r['hints'][0]['food']['nutrients']

def company_login(uname, pswd):
    v = c.execute('''SELECT * FROM companies WHERE uname='{}' AND psw='{}' '''.format(uname, pswd))
    return v.fetchall()

def student_login(uname, pswd):
    v = c.execute('''SELECT * FROM students WHERE uname='{}' AND psw='{}' '''.format(uname, pswd))
    return v.fetchall()

#zc is zipcode
def add_student(name, uname, psw, uni, zc, county, state, gid = ""):
    c.execute('''INSERT INTO students values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(genID(), name, uname, psw, uni, zc, county, state, gid))
    conn.commit()

def get_company(cid):
    info = c.execute('''SELECT * FROM companies WHERE cid = '{}' '''.format(cid))
    return list(info.fetchall()[0])

def get_student(sid):
    info = c.execute('''SELECT * FROM students WHERE sid = '{}' '''.format(sid))
    return list(info.fetchall()[0])

def create_group(name):
    gid = genID()
    c.execute('''INSERT INTO master_groups values('{}', '{}')'''.format(gid, name))
    c.execute('''CREATE TABLE '{}' (id text, timestamp text, content text)'''.format(gid))
    conn.commit()

def get_groups():
    groups = c.execute('''SELECT * FROM master_groups''')
    groups_list = []
    for row in groups:
        groups_list.append(list(row))
    return groups_list

def create_announcement(gid, content):
    timestamp = time.strftime("%a, %d %b %Y %I:%M", time.localtime())
    c.execute('''INSERT INTO {} values('{}', '{}', '{}')'''.format(gid, genID(), timestamp, content))
    conn.commit()

def get_announcement(gid):
    announcements = []
    info = c.execute('''SELECT * FROM {}'''.format(gid))
    for row in info:
        announcements.append(list(row))

    return announcements
    
#zc is zipcode
def add_company(name, uname, psw, phone, email, zc, county, state):
    c.execute('''INSERT INTO companies values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(genID(), name, uname, psw, phone, email, zc, county, state))
    conn.commit()

def add_product(price, name, tag, desc, cid):
    company_info = c.execute('''SELECT * FROM companies WHERE cid="{}"'''.format(cid));
    for row in company_info:
        #print(row)
        info = row
    zc, county = info[6], info[7]
    c.execute('''INSERT INTO products values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(genID(), price, name, tag, desc, cid, get_link(name), zc, county));
    conn.commit()

def get_tags(keyword):
    tags = []
    products = c.execute('''SELECT * FROM products''')
    for row in products:
        #add nlp later
        if keyword in row[3] and row[3] not in tags:
            tags.append(row[3])

    return tags

def get_products(tag, sid):
    products = []
    student_info = c.execute('''SELECT * FROM students WHERE sid = "{}"'''.format(sid))
    for row in student_info:
        info = row
    zc = info[5]
    items = c.execute('''SELECT * FROM products WHERE tag = '{}' AND zip = '{}' '''.format(tag, zc))
    for row in items:
        products.append(list(row))

    return products

def clear_db():
    tables = c.execute('SELECT * FROM sqlite_master WHERE type="table"')
    table_names = []
    for row in tables:
        table_names.append(row[1])
    for t in table_names:
        c.execute("DROP TABLE '{}'".format(t))
        print("dropped {}".format(t))
    conn.commit()

def close():
    conn.close()

if __name__ == '__main__':
    setup()
    #--Tests--
    print(get_groups())
    close()
