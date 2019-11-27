import re
import sys
import os

numbers_pattern = '\d+'
amount_pattern = ['(\d+)\s(one|ten|hundred|thousand|ten thousand|hundred thousand|million|billion)',
                  '(almost|generally|relatively|roughly|about|around|ballpark figure|bordering on|circa|close to|closely|comparatively|in the ballpark|in the neighborhood of|in the region of|in the vicinity of|just about|loosely|more or less|most|much|not far from|not quite|proximately|upwards of|very close)\s(\d+)',
                  '(almost|generally|relatively|roughly|about|around|ballpark figure|bordering on|circa|close to|closely|comparatively|in the ballpark|in the neighborhood of|in the region of|in the vicinity of|just about|loosely|more or less|most|much|not far from|not quite|proximately|upwards of|very close to)\s(\d+)\s(one|ten|hundred|thousand|ten thousand|hundred thousand|million|billion)',
                  '(almost|generally|relatively|roughly|about|around|ballpark figure|bordering on|circa|close to|closely|comparatively|in the ballpark|in the neighborhood of|in the region of|in the vicinity of|just about|loosely|more or less|most|much|not far from|not quite|proximately|upwards of|very close to)\s(\d+)\s(one|ten|hundred|thousand|ten thousand|hundred thousand|million|billion)\s(rupees|dollars|million rupees|millions)']
date_pattern = [
    '(1st|2nd|3rd|4th|5th|6th|7th|8th|9th|10th|11th|12th|13th|14th|15th|16th|17th|18th|19th|20th|21st|22nd|23rd|24th|25th|26th|27th|28th|29th|30th|31st)\s(of)\s(january|february|march|april|may|june|july|august|september|october|november|december)',
    '(january|february|march|april|may|june|july|august|september|october|november|december|January|February|March|April|May|June|July|August|September|October|November|December)\s(1st|2nd|3rd|4th|5th|6th|7th|8th|9th|10th|11th|12th|13th|14th|15th|16th|17th|18th|19th|20th|21st|22nd|23rd|24th|25th|26th|27th|28th|29th|30th|31st)',
    '(next week|next time|next day|next year|today|in one hour| i the evening)']
phone_number_pattern = [
    '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}|\{\d{3}\}\s*\d{3}[-\.\s]??\d{4})|\{\d{3}\}\s*\d{3}[-\.\s]??\d{4}|\(\d{3}\)[-\.\s]*\d{3}[-\.\s]??\d{4}',
    '\(\d{3}\)[-\.\s]*\d{3}\s-??\d{4}', '07\d{8}', '\d{9']
email_pattern = '[\w\.-]+@[\w\.-]+'
url_pattern = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'


def get_number_values(text):
    number_values = re.findall(numbers_pattern, text)
    return number_values

#print(get_number_values("The date today is 24th of July. He is 30 yeards old. The price is 25.11. percentage is 5.0%"))

def get_amounts(text):
    my_amounts = []
    count = 0
    # Extract Phone Numbers
    for pattern in amount_pattern:
        count = count + 1
        amounts = re.findall(pattern, text)

        if amounts:
            my_amounts += amounts
    return my_amounts


def get_dates(text):
    my_dates = []
    count = 0
    # Extract Phone Numbers
    for pattern in date_pattern:
        count = count + 1
        dates = re.findall(pattern, text)

        if dates:
            my_dates += dates
    return my_dates


def get_phone_numbers(text):
    my_phone_numbers = []
    count = 0
    # Extract Phone Numbers
    for pattern in phone_number_pattern:
        count = count + 1
        phone_numbers = re.findall(pattern, text)
        if phone_numbers:
            my_phone_numbers += phone_numbers
    return my_phone_numbers


def get_urls(text):
    # Extract Urls
    urls = re.findall(url_pattern, text)
    return urls


def get_emails(text):
    # Extract Email
    emails = re.findall(email_pattern, text, re.I)
    return emails


def get_raw_text(filename):
    try:
        file_pointr = open(filename, 'r')
        return file_pointr.read()
    except Exception as exception_instance:
        return ''


def get_file_info(raw_text):
    output = {}

    NumberValues = get_number_values(raw_text)
    #print(NumberValues)

    Amounts = get_amounts(raw_text)
    AmountList = []
    for amounts in Amounts:
        AmountList.append(' '.join(amounts))
    #print(AmountList)

    Emails = get_emails(raw_text)
    #print(Emails)

    Dates = get_dates(raw_text)
    DateList = []
    for dates in Dates:
        DateList.append(' '.join(dates))
    #print(DateList)

    Urls = get_urls(raw_text)
    #print(Urls)

    PhoneNumbers = get_phone_numbers(raw_text)
    #rint(PhoneNumbers)

    output['NumberValues'] = NumberValues
    output['Amounts'] = AmountList
    output['Emails'] = Emails
    output['Urls'] = Urls
    output['PhoneNumbers'] = PhoneNumbers
    output['Dates'] = DateList
    #print(output)

    if NumberValues==[] and AmountList==[] and Emails==[] and Urls==[] and PhoneNumbers==[] and DateList==[]:
        #print("false")
        return False
    else:
        print("True")
        return True
    #print(output)


def main(convo):
    words = convo.split(" ")
    if len(words)>4:
        return False
    else:
        return get_file_info(convo)

# if __name__ == '__main__':
#     try:
#         filename = 'C:/Users/Sadeepa/PycharmProjects/Hello/sources/audios/ES2004c.txt'
#
#         try:
#             if not os.path.isfile(filename):
#                 print("Invalid File Path")
#             else:
#                 raw_text = get_raw_text(filename)
#                 get_file_info(raw_text)
#
#         except:
#             print("Invalid File Path")
#     except:
#         print("Pass Valid File Name parameter")
#         print("For Ex: python sample.py filename.txt")
#         sys.exit()

if __name__ == '__main__':

    main("The project will cost 10 million.")
