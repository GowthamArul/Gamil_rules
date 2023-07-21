import json
import os
import sqlite3
from gmail_actions import *
import datetime

conn = sqlite3.connect("mail_db.db")
cursor = conn.cursor()
    
def _sql_return(config, key):
    rule = config[key]

    conditions = rule['Conditions']
    ls_sql = []
    for con in conditions:
        field = str(con[0]).lower()
        predicate = str(con[1]).upper()
        value = con[2]
        q_str = ""
        #contains / not equals / less than
        if field == "g_date":
            current_utc_time = datetime.datetime.utcnow()
            val = int(value.split(' ')[0])
            day_month = value.split(' ')[1]
            if str(day_month).upper() in ['DAYS', 'DAY']:
                if str(predicate).upper() == 'LESS THAN':
                    utc_now = current_utc_time - datetime.timedelta(days=val)
                    q_str = f"{field} < '{utc_now}'" 
                elif str(predicate).upper() ==  'GREATER THAN':
                    utc_now = current_utc_time + datetime.timedelta(days=val)
                    q_str = f"{field} > '{utc_now}'" 
            elif str(day_month).upper() in ['MONTH', 'MONTHS']:
                if str(predicate).upper() == 'LESS THAN':
                    utc_now = current_utc_time - datetime.timedelta(months=val)
                    q_str = f"{field} < '{utc_now}'" 
                elif str(predicate).upper() ==  'GREATER THAN':
                    utc_now = current_utc_time + datetime.timedelta(months=val)
                    q_str = f"{field} > '{utc_now}'" 

        elif predicate == "CONTAINS":
            q_str = f"{field} like '%{value}%'"
        elif predicate == "DOES NOT CONTAINS":
            q_str = f"{field} not like '%{value}%'"
        elif predicate == "NOT EQUALS":
            q_str = f"{field} != '{value}'"
        elif predicate == "EQUALS":
            q_str = f"{field} == '{value}'"
        ls_sql.append(q_str)

    if  str(rule['All/Any']).upper() == "ALL":
        query = " and ".join(ls_sql)
    elif  str(rule['All/Any']).upper() == 'ANY':
        query = " or ".join(ls_sql)
   
    return query
            

def _rule_action(rule_config):
    config = rule_config
    if not isinstance(config, type(None)):
        for key in config.keys():
            sql = _sql_return(config, key)
            select_sql = f"select g_id from GINBOX where {sql};"
            result = cursor.execute(select_sql).fetchall()
            message_id  = [i[0] for i in result]
            if len(message_id) != 0:
                action_on_move = config[key]['actions']['Move Message']
                action_on_read = config[key]['actions']['Marks']
                if len(message_id) == 1:
                    if str(action_on_read).upper() in ['MARK AS READ']:
                        mark_as_read(message_id[0])
                    elif str(action_on_read).upper() in ['MARK AS UNREAD']:
                        mark_as_unread(message_id[0])
                    if str(action_on_move).upper not in ['INBOX', 'TRASH']:
                        label_id = get_label(action_on_move)
                        move_to(message_id[0], label_id['id'])
                    elif str(action_on_move).upper in ['TRASH']:
                        label_id = get_label(action_on_move)
                        move_to(message_id[0], label_id['id'])
                elif len(message_id) > 1:
                    for id in message_id:
                        if str(action_on_read).upper() in ['MARK AS READ']:
                            mark_as_read(id)
                        elif str(action_on_read).upper() in ['MARK AS UNREAD']:
                            mark_as_unread(id)
                        if str(action_on_move).upper not in ['INBOX', 'TRASH']:
                            label_id = get_label(action_on_move)
                            move_to(id, label_id['id'])
                        elif str(action_on_move).upper in ['TRASH']:
                            label_id = get_label(action_on_move)
                            move_to(id, label_id['id'])
            else:
                print("Entered action does not exisit in gmail")



if __name__ == '__main__':
    rule_config = None
    try:
        rule_config = json.load(open('rule_inputs.json'))
    except Exception as e:
        print('The json file is empty or incorrect')
    _rule_action(rule_config)
    conn.commit()
    conn.close()
