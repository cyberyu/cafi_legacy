import unicodedata

def format_phone_number(phone):
    if phone is None or phone.strip() == '':
        return ''
    else:
        """
        return '-'.join((phone[:3], phone[3:6], phone[6:]))
        """
        return '(' + phone[:3] + ') ' + phone[3:6] + '-' + phone[6:]

def normalize(string):
    return unicodedata.normalize('NFKD', string).encode('ascii','ignore').strip()
