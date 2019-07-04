import csv
import os

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
    file_name = 'jan_2019_transactions.csv'
    
    titles, data = import_file(path, file_name) #get csv data from mint
    
    data = manipulate_data(titles, data) #perform calculations on data
    
    summary_table = summarize(pay_from_accounts, titles, data) #create a summary table based on accounts
    
    output_results(summary_table) #output data into new csv file
    

def import_file(path, file_name):
    location  = os.path.join(path, file_name)
    fields = []
    rows = []
    
    f = open(location, encoding='utf-8-sig') #https://stackoverflow.com/questions/34399172/why-does-my-python-code-print-the-extra-characters-%C3%AF-when-reading-from-a-tex
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

def output_results(expense_dict):
    
    with open('output.csv', 'w', newline='') as csvfile:
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
            
        

def tests():
    
    
    #testing import_file
    path = r'C:\Users\Andrew\Downloads'
    file_name = 'jan_2019_transactions.csv'
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
    
    
    titles, data = import_file(path, file_name)
    assert titles == ['Date', 'Description', 'Original Description', 'Amount', 'Transaction Type', 'Category', 'Account Name', 'Labels', 'Notes']
    
    #testing manipulate_data
    data = manipulate_data(titles, data)
    
    #testing summaize
    summary = summarize(pay_from_accounts, titles, data)
    #print(summary)
    
    output_results(summary)
    
    
    print('tests done')
    
main()