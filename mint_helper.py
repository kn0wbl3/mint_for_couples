import csv
import os
import datetime

def main():
    
    pay_from_accounts = {
                    'Apartment Cushion':'3756', 
                    'Gifts':'3729', 
                    'From Us Gifts':'3699', 
                    'End of Yr Staff Tip':'8490', 
                    'From Us Apartment':'0498', 
                    'From Us Vacation':'4728', 
                    'From Us Wedding':'0923', 
                    'Golf-Ski Seasons':'6886', 
                    'Big Weekends':'4116', 
                    'My Vacations':'6768', 
                    'New Years 2017':'3701', 
                    'Big Purchase':'3738', 
                    'Holding Acct':'8347', 
                    'WF Checking':'7027',
                    'WF Savings':'4969'
                    }
    
    
    path = r'C:\Users\Andrew\Downloads'
    work_path = r'C:\Users\amanuele2\AppData\Local\Temp\Bloomberg\data'
    
    file_name = 'transactions.csv'
    output_fl_name = 'output.csv'
    location  = os.path.join(path, file_name)
    
    try: #test to see where I am running this, at work or at home?
        f = open(location) #https://stackoverflow.com/questions/34399172/why-does-my-python-code-print-the-extra-characters-%C3%AF-when-reading-from-a-tex
        f.close()
        
    except FileNotFoundError:
        path = work_path
        location  = os.path.join(work_path, file_name)
    
    
    titles, data = import_file(location, work_path, file_name) #get csv data from mint
    
    data = manipulate_data(titles, data) #perform calculations on data
    
    summary_table = summarize(pay_from_accounts, titles, data) #create a summary table based on accounts
    
    output_results(summary_table, path) #output data into new csv file
    
    rename_file(file_name, path, 'transactions-')
    rename_file(output_fl_name, path, 'transaction_summary-')
    

def import_file(location, bckup_path, file_name):
    fields = []
    rows = []
    
    f = open(location, encoding='utf-8-sig')
    
    csv_f = csv.reader(f)
    fields = next(csv_f)
    #print(fields)
    
    for row in csv_f:
        rows.append(row)
           
    f.close()
        
    return fields, rows
    
    #print(rows)
    
def manipulate_data(columns, rows):
    #find Amount column
    #change Amount column to a negative or pos number based on 'Transaction Type' column
    
    for i in range(len(columns)):
        if columns[i] == 'Amount':
            amount_col = i
        if columns[i] == 'Transaction Type':
            trans_type_col = i
    
    for row in rows:
        #print(row[amount_col])
        #print(row[trans_type_col])
        
        if row[trans_type_col] == 'debit':
            row[amount_col] = -float(row[amount_col])
        else:
            row[amount_col] = float(row[amount_col])
            
    return rows

def summarize(accounts, columns, rows):
    summary_dict = {'My Expenses': [0, '7027'], 'Venture': [0, '7027']}
    
    for i in range(len(columns)):
        if columns[i] == 'Labels':
            labels_col = i
        if columns[i] == 'Amount':
            amount_col = i
        if columns[i] == 'Account Name':
            acct_name_col = i
            
    for row in rows:
        if (row[acct_name_col] == 'Venture') and (row[labels_col] == ''):
            summary_dict['Venture'][0] += (row[amount_col] / 2) #split between me and liz
        elif row[labels_col] == '':
            summary_dict['My Expenses'][0] += row[amount_col]
        else:
            summary_dict[row[labels_col]] = [(summary_dict.get(row[labels_col][0], 0) + row[amount_col]), accounts[row[labels_col]]]
    
    return summary_dict

def output_results(expense_dict, path):
    
    with open(path + '\output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category', 'Total Expenses', 'Account to Pay'])
        for data in expense_dict.items():
            category = data[0]
            expense = '${:,.2f}'.format(data[1][0])
            account = data[1][1]
            
            agg = [category, expense, account]
            writer.writerow(agg)
            #print(category)
            #print(expense)
            #print(account)
        
    csvfile.close()
    
    
def rename_file(file_name, path, new_name):
    #rename file
    location  = os.path.join(path, file_name)
    today = datetime.date.today()
    today = str(today.month - 1) + '_' + str(today.year)
    new_name = new_name + today + '.csv'
    new_loc = os.path.join(path, new_name)
    os.rename(location, new_loc)
    
main()
