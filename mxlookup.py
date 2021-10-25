import dns.resolver
import csv

def readCsv(filename):
    result = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            result.append(row)

    return result

def writeCsv(file_name, row):
    with open(file_name, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter =',')
        writer.writerow(row)

def mxLookup(domain):
    mxRecord = ''
    try:
        for x in dns.resolver.resolve(domain, 'MX'):
            mxRecord = x.to_text().split(' ')[1]
    except:
        mxRecord = 'nomxrecord.com.'

    return mxRecord

def isOffice365(mxRecord):
    try:
        domainId = mxRecord.split('.')[::-1][2]
        if domainId == 'outlook':
            return True
        else:
            return False
    except:
        return False

def main():
    writeCsv('result.csv', ['email', 'domain', 'mxRecord'])
    contacts = readCsv('./emails.csv')
    temp = []

    for index, contact in enumerate(contacts[1:len(contacts)]):
        try:
            email = contact[2]
            domain = email.split('@')[1].lower()
            mxRecord = mxLookup(domain)
            completed = round((index / (len(contacts) - 1)) * 100, 2)
            print(str(completed) + '%')
            
            if isOffice365(mxRecord) and (domain not in temp):
                temp.append(domain)
                writeCsv('result.csv', [email, domain, mxRecord])
                print(email, domain, mxRecord)
        except:
            continue

if __name__ == '__main__':
    main()
    # mxLookup('mcneillhotels.com')
    # isOffice365('hilton-com.mail.protection.outlook.com.')