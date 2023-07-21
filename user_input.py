import json
import os

rules_actions =  {
        'All/Any': '',
		'Conditions': [],
        'actions':{
            'Move Message': '',
            'Marks' : ''
        }
	}

rule = {}

rule_name = str(input("Enter the Rule_name: "))

try:
    rule[rule_name] = rules_actions
    any_all = str(input("Enter the Rule collection (All/Any): "))
    rule[rule_name]['All/Any'] = any_all.capitalize()
    while True:
        # import pdb;pdb.set_trace()
        feild = str(input("Enter the Feilds for RUle (From/Subject/Message/Date Received): "))
        if str(feild).upper() in ['FROM', 'SUBJECT', 'MESSAGE', 'DATE RECEIVED']:
            ls = []
            if str(feild).capitalize() == 'From':
                Contain = str(input("Enter the From Predicate(Contains,Does not Contain,Equals,Does not equal): "))
                if str(Contain).upper() in ['CONTAINS','DOES NOT CONTAIN','EQUALS','DOES NOT EQUAL']:
                    fmr = 'g_from'
                    val = str(input("Enter the From Details: "))
                    ls.append(fmr)
                    ls.append(Contain)
                    ls.append(val)
                else:
                    print("Invalid Contains")
                    continue
            elif str(feild).capitalize() == 'Subject':
                Contain = str(input("Enter the From Predicate(Contains,Does not Contain,Equals,Does not equal): "))
                if str(Contain).upper() in ['CONTAINS','DOES NOT CONTAIN','EQUALS','DOES NOT EQUAL']:
                    sub = 'g_subject'
                    val = str(input("Enter the Subject value: "))
                    ls.append(sub)
                    ls.append(Contain)
                    ls.append(val)
                else:
                    print("Invalid Contains")
                    continue
            elif str(feild).capitalize() == 'Message':
                Contain = str(input("Enter the From Predicate(Contains,Does not Contain,Equals,Does not equal): "))
                if str(Contain).upper() in ['CONTAINS','DOES NOT CONTAIN','EQUALS','DOES NOT EQUAL']:
                    msg = 'g_preview'
                    val = str(input("Enter the Message value "))
                    ls.append(msg)
                    ls.append(Contain)
                    ls.append(val)
                else:
                    print("Invalid Contains")
                    continue
            elif str(feild).upper() in ['DATE RECEIVED']:
                Contain = str(input("Enter the Date Received Predicate(Less than,Greater than): "))
                if str(Contain).upper() in ['LESS THAN','GREATER THAN']:
                    date = 'g_date'
                    ls.append(date)
                    ls.append(Contain)
                    day_month =  str(input("Enter the Date Received Predicate month or day (12 month or 3 days): "))
                    ls.append(day_month)
                else:
                    print("Invalid Contains")
                    continue
        rule[rule_name]['Conditions'].append(ls) 
        cont = str(input("Would you like to add more fields (Yes/No): "))
        if str(cont).capitalize() == 'Yes':
            continue
        else:            
            break
    move_to = str(input("Enter the Move Message action for the Rule (Inbox/Trash/Happy): "))
    if str(move_to).upper() in ['INBOX','DRAFT','TRASH','HAPPY']:
        rule[rule_name]['actions']['Move Message'] = move_to.capitalize()
    else:
        print("Invalid Input")
    mark = str(input("Enter the action for the Message for the Rule (Mark as Read/ Mark as Unread): "))
    if str(mark).upper() in ['MARK AS READ','MARK AS UNREAD']:
        rule[rule_name]['actions']['Marks'] = mark.capitalize()
    else:
        print("Invalid Input")

    if os.stat('rule_inputs.json').st_size == 0:
        with open("rule_inputs.json", "w") as outfile:
            json.dump(rule, outfile)
    else:
        config = json.load(open('rule_inputs.json'))
        config[rule_name] = rules_actions
        with open("rule_inputs.json", "w") as outfile:
            json.dump(config, outfile)

except ValueError:
    print("Sorry, I didn't understand that.")

