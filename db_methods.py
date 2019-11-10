import sqlite3, requests, time, random

conn = sqlite3.connect('teenhacks.db', check_same_thread = False)

c = conn.cursor()

APP_KEY_ING = "34d4f83429cfe1e57b09c59ad3f4c886"
APP_ID_ING = "22e4f2a8"

APP_ID_REC = '96c1e2f7'
APP_KEY_REC = '3ebcdeef7ffd746d62f6ad3e60da28e6'

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

def get_recipes(name, tags=[]):
    url = "https://api.edamam.com/search?q={}&app_id=${}&app_key=${}&from=0&to=10".format(name, APP_ID_REC, APP_KEY_REC)

    for i in tags:
        if i in ['balanced', 'high-fiber', 'high-protein', 'low-carb', 'low-fat', 'low-sodium']:
            url += '&diet={}'.format(i)
        elif i != '':
            url += '&health={}'.format(i)

    response = requests.get(url)

    r = response.json()['hits']
    recipes = []
    for i in range(10):
        recipes.append({})

    for i, recipe in enumerate(r):
        #name
        recipes[i]['name'] = r[i]['recipe']['label']
        recipes[i]['ingredients'] = r[i]['recipe']['ingredientLines']
        recipes[i]['source'] = r[i]['recipe']['source']
        recipes[i]['source_url'] = r[i]['recipe']['url']
    
    nonempty = []

    for x in recipes:
        if x != {}:
            nonempty.append(x)

    return nonempty

def get_restrictions():
    return ['high-fiber', 'high-protein', 'low-carb', 'low-fat', 'low-sodium', 'alcohol-free', 'celery-free', 'crustacean-free', 'dairy-free', 'egg-free', 'fish-free', 'fodmap-free', 'gluten-free', 'keto-friendly', 'kidney-friendly', 'low-potassium', 'lupine-free', 'mustard-free', 'low-fat-abs', 'No-oil-added', 'No-sugar', 'low-sugar', 'peanut-free', 'pork-free', 'meat-free', 'red-meat-free', 'sesame-free', 'shellfish-free', 'soy-free', 'sugar-conscious', 'tree-nut-free','wheat-free', 'vegetarian', 'vegan', 'pescatarian']

def get_link(name):
    name = name.strip().replace(' ', "%20")
    link = 'https://api.edamam.com/api/food-database/parser?nutrition-type=logging&ingr={}&app_id={}&app_key={}'.format(name, APP_ID_ING, APP_KEY_ING)
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

def change_company(cid, name, uname, psw, phone, email, zc, county, state):
    c.execute('''UPDATE companies SET name='{}', uname='{}', psw='{}', phone='{}', email='{}', zip='{}', county='{}', state='{}' WHERE cid='{}' '''.format(name, uname, psw, phone, email, zc, county, state, cid))
    conn.commit()

def get_student(sid):
    info = c.execute('''SELECT * FROM students WHERE sid = '{}' '''.format(sid))
    return list(info.fetchall()[0])

def change_student(sid, name, uname, psw, uni, zc, county, state):
    c.execute('''UPDATE students SET name='{}', uname='{}', psw='{}', uni='{}', zip='{}', county='{}', state='{}' WHERE sid='{}' '''.format(name, uname, psw, uni, zc, county, state, sid))
    conn.commit()

def create_group(name):
    gid = genID()
    c.execute('''INSERT INTO master_groups values('{}', '{}')'''.format(gid, name))
    c.execute('''CREATE TABLE '{}' (id text, timestamp text, content text)'''.format(gid))
    conn.commit()

    return gid

def get_groups():
    groups = c.execute('''SELECT * FROM master_groups''')
    groups_list = []
    for row in groups:
        groups_list.append(list(row))
    return groups_list

def set_group(sid, gid):
    c.execute('''UPDATE students SET gid = '{}' WHERE sid = '{}' '''.format(gid, sid))
    conn.commit()

def create_announcement(gid, content):
    timestamp = time.strftime("%a, %d %b %Y %I:%M", time.localtime())
    c.execute('''INSERT INTO {} values('{}', '{}', '{}')'''.format(gid, genID(), timestamp, content))
    conn.commit()

def get_announcement(gid):
    announcements = []
    info = c.execute('''SELECT * FROM "{}"'''.format(gid))
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
    #set_group('G5v63r8', '0N3iYU2')
    #change_company('Ul86qZ8DlOar1Pu758ZQc1meUAfALm943I8p575LBWjL8ZCbK8', 'colin galen', 'galen_colin', '', '', 'tjhsst', '20479', 'Fairfax', 'VA')
    close()