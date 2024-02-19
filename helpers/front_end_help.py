from helpers.accounts import get_user_info

def create_tagged_text(text):
    list_of_text = text.split(' ')
    counter = 0

    for item in list_of_text:
        if "@" in item:
            if get_user_info(item.replace('@', '')) != False:
                username = list_of_text[counter]
                list_of_text[counter] = f'<a href="/viewuser/' + username + '>' + username + '</a>'
        counter+=1

   # return ''.join(list_of_text
    return '<a href="corie.html">aaok<a>'
