'''
Created on 22 Nov 2018

@author: devwarrior
'''
import sqlite3

class State:
    unknown = -1
    new_session = 0
    participant_joined = 1
    init_contract_offered = 2   #<- internal only?
    init_contract_accepted = 3
    part_contract_offered = 4   #<- internal only?    Can the initiator publish both contracts? Yes, both are complete!
    part_contract_accepted = 5
    # Up to this point all can be thrown out
    # and re-done with no opportunity cost
    init_contract_published = 6
    part_contract_published = 7
    
    
def create_table_if_not_exists(cur, con):
    create_table_cmd  = "CREATE TABLE IF NOT EXISTS atomic_swaps "
    create_table_cmd += "("
    create_table_cmd += "session TEXT PRIMARY KEY, "
    create_table_cmd += "participant TEXT, "
    create_table_cmd += "state INTEGER, "
    create_table_cmd += "init_contract TEXT, "
    create_table_cmd += "init_contract_tx TEXT, "
    create_table_cmd += "init_refund_tx TEXT, "
    create_table_cmd += "init_redeem_tx TEXT, "   # INSERT AFTER BROADCASTED AND MINED . . . as a convenience to participant
    create_table_cmd += "init_accept_time INTEGER, "
    create_table_cmd += "init_publish_txid TEXT, "
    create_table_cmd += "part_contract TEXT, "
    create_table_cmd += "part_contract_tx TEXT, "
    create_table_cmd += "part_refund_tx TEXT, "
    create_table_cmd += "part_accept_time INTEGER, "
    create_table_cmd += "part_publish_txid TEXT"
    create_table_cmd += ");"
    try:
        cur.execute(create_table_cmd)
        con.commit()
        print('Created table')
    except:
        print('Table already exists')

def create_new_session(init_address, cur, con):
    sql = "SELECT session FROM atomic_swaps WHERE session = ?;"
    cur.execute(sql, (init_address, ))
    rows = cur.fetchall()
    if len(rows):
        print('session:', init_address, 'already exists')
        return
    sql = "INSERT INTO atomic_swaps VALUES(?,NULL,?,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,0,NULL);"
    cur.execute(sql, (init_address, State.new_session))
    con.commit()
    print('session:', init_address, 'created')
    
def add_participant(part_address, init_address, cur, con):
    sql = "SELECT session FROM atomic_swaps WHERE session = ? AND participant = ?;"
    cur.execute(sql, (init_address, part_address, ))
    rows = cur.fetchall()
    if len(rows):
        print('session:', init_address, 'already exists with', part_address)
        return
    sql = "UPDATE atomic_swaps SET participant = ?, state = ? WHERE session = ?;"
    cur.execute(sql, (part_address, State.participant_joined, init_address, ))
    con.commit()
    print('session:', init_address, 'added', part_address)
        
    
if __name__ == '__main__':
    con = sqlite3.connect('test.db')
    print('module:', sqlite3.version, 'sqlite:', sqlite3.sqlite_version, repr(con))
    cur = con.cursor()
    
    create_table_if_not_exists(cur, con)

    init_address = 'cCxYpbfnnyMifREqz3Wo5uedjnj73xN7qi'
    create_new_session(init_address, cur, con)
    
    part_address = '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2'
    add_participant(part_address, init_address, cur, con)    
    
    con.close()