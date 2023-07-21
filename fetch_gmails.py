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



# def _insert_message_to_db():
#     flag = _create_db_table()
#     messages_id = get_mail_ids()
#     for msg in messages_id:
#         msg_id = msg['id']
#         select_sql = f"select g_id from GINBOX where g_id = '{msg_id}';"
#         result = cursor.execute(select_sql)
#         res = [i[0] for i in result]
#         # if len(res) != 0:
#         #     continue
        
#         txt = get_messages1(msg)
#         try:
#             # Get value of 'payload' from dictionary 'txt'
#             payload = txt['payload']
#             headers = payload['headers']

#             # Look for Subject and Sender Email in the headers
#             for d in headers:
#                 if d['name'] == 'Subject':
#                     subject = d['value']
#                 if d['name'] == 'From':
#                     sender = d['value']
#                 if d['name'] == 'Delivered-To':
#                     g_to = d['value']
#                 if d['name'] == 'Date':
#                     g_date = d['value']
  
#             # The Body of the message is in Encrypted format. So, we have to decode it.
#             # Get the data and decode it with base 64 decoder.
#             parts = payload.get('parts')[0]
#             data = parts['body']['data']
#             data = data.replace("-","+").replace("_","/")
#             decoded_data = base64.b64decode(data)
  
#             # Now, the data obtained is in lxml. So, we will parse 
#             # it with BeautifulSoup library
#             soup = BeautifulSoup(decoded_data , "lxml")
#             body = soup.body()
#             new_msg_body = body.replace("<p>", )
#             # Printing the subject, sender's email and message
#             print("From: ", sender)
#             print("To: ", g_to)
#             print("Subject: ", subject)
#             print("Date: ", g_date)
#             print("Message: ", type(body))

#             sql = f"""
#                     INSERT INTO GINBOX (g_id, g_to, g_from, g_subject, g_date, g_preview)  VALUES ('{msg['id']}', '{g_to}', '{sender}', '{subject}', '{g_date}', '{body}');
#                     """
#             cursor.execute(sql)
#             print("Values has been inserted")
#             # select_sql = 'select * from GINBOX;'
#             # result = cursor.execute(select_sql).fetchall()
#             # print(result)
#             # cursor.close()
#         except Exception as e:
#             print(e)

