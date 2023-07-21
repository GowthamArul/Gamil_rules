from simplegmail import Gmail
import sqlite3
import traceback
from gmail_actions import *
from bs4 import BeautifulSoup
import base64

gmail = Gmail()
conn = sqlite3.connect("mail_db.db")
cursor = conn.cursor()

# Unread messages in your inbox (g_id INT AUTO_INCREMENT PRIMARY KEY) g_msg_body VARCHAR(50)
def _create_db_table():
    try:
        create_sql = '''
                    CREATE TABLE GINBOX(
                    g_id VARCHAR(50),
                    g_to VARCHAR(50),
                    g_from VARCHAR(50),
                    g_subject VARCHAR(50),
                    g_date VARCHAR(50),
                    g_preview VARCHAR(50),
                    g_msg_body VARCHAR(50)
                    );
                    '''
        cursor.execute(create_sql)
        print('Table Created')
        return True
    except Exception as e:
        return False
    
# Function to store the messages into Created Base
def _fetch_mail_from_gmail():
    flag = _create_db_table()
    messages = gmail.get_messages()
    for message in messages:
        try:
            select_sql = f"select g_id from GINBOX where g_id = '{message.id}';"
            result = cursor.execute(select_sql).fetchall()
            print(message.date)
            if len(result) == 0:
                sql = f"""
                        INSERT INTO GINBOX (g_id, g_to, g_from, g_subject, g_date, g_preview, g_msg_body)  VALUES ('{message.id}', '{message.recipient}', '{message.sender}', '{message.subject}', '{message.date}', '{message.snippet}', '{message.plain}');
                        """
                cursor.execute(sql)
                print("Values has been inserted")
            else:
                print("Message already exist")
                pass

        except Exception as e:
            print(traceback.format_exc())
            # print(e)

if __name__ == '__main__':
    _fetch_mail_from_gmail()
    # _insert_message_to_db()
    conn.commit()
    conn.close()
