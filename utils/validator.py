import re

def validate_data(data):
    errors = {}

    if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', data['PAN']):
        errors['PAN'] = 'Invalid PAN format'

    try:
        income = int(data['Income'].replace(',', ''))
        if income < 10000:
            errors['Income'] = 'Income too low'
    except:
        errors['Income'] = 'Invalid Income'

    try:
        loan = int(data['Loan Amount'].replace(',', ''))
        if loan < 5000 or loan > 1000000:
            errors['Loan Amount'] = 'Loan amount not realistic'
    except:
        errors['Loan Amount'] = 'Invalid Loan Amount'

    return errors
