import pyodbc as db

def MakeRoom():
    con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};Server=localhost\SQLEXPRESS;Trusted_Connection=yes;Database=Test;')
    cur = con.cursor()
    qry = ''' DELETE FROM URG
              WHERE URG_PK >= 1
    '''
    cur.execute(qry)
    cur.close()
    con.close()


###############################################
#### UPPER RECIEVER GROUPS 
def submitURG(Descript,Barrel_Len,Barrel_type,Price,Cal,Brand,Link,Pic_links,Color,stock):
#connection setup
    con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};Server=localhost\SQLEXPRESS;Trusted_Connection=yes;Database=Test;')
    cur = con.cursor()
    index=0
#QUERY
    qry = '''INSERT INTO dbo.URG
            (Descript,Barrel_len,Barrel_type,Price,Cal,Brand,Link,Pic_links,Color,stock)
            VALUES(?,?,?,?,?,?,?,?,?,?)
    '''
    while(index < len(Descript)):
        param_values = [Descript[index],Barrel_Len[index],Barrel_type[index],Price[index],Cal[index],Brand[index],Link[index],Pic_links[index],Color[index],stock[index]]
        cur.execute(qry,param_values)
        print('{0} row inserted successfully.'.format(cur.rowcount))
        cur.commit()
        index+=1
    cur.close()
    con.close()

###################################################################################
#### LOWER RECIEVER GROUPS ##################
def submitLowerGroup(Descript,Brand,Type,Color,Stock,Butt_Stock,Price,Link,Pic_Links):
    #connection setup
    con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};Server=localhost\SQLEXPRESS;Trusted_Connection=yes;Database=Test;')
    cur = con.cursor()
    index=0
#QUERY
    qry = '''INSERT INTO dbo.Lower_Group
            (Descript,Brand,Type,Color,Stock,Butt_Stock,Price,Link,Pic_Links)
            VALUES(?,?,?,?,?,?,?,?,?)
    '''
    while(index < len(Descript)):
        param_values = [Descript[index],Brand[index],Type[index],Color[index],Stock[index],Butt_Stock[index],Price[index],Link[index],Pic_Links[index]]
        cur.execute(qry,param_values)
        print('{0} row inserted successfully.'.format(cur.rowcount))
        cur.commit()
        index+=1
    cur.close()
    con.close()