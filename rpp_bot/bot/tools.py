my_list = [
    {'day': 1, 'ordinal_number': 1, 'content_type': 'TXT', 'content': 'Message 1 at day 1'},
    {'day': 1, 'ordinal_number': 2, 'content_type': 'TXT', 'content': 'Message 2 at day 1'},
    {'day': 1, 'ordinal_number': 3, 'content_type': 'IMG', 'content': 'Image 3 at day 1'}]

result = []
for dictionary in my_list:
    concat = 'Message ' + dictionary['ordinal_number'].__str__() + ' > Type: ' + dictionary['content_type'] + '\nContent: ' + dictionary['content']
    print(concat)
    result.append(concat)

result_string = '\n'.join(result)
print(type(result_string))
print(result_string)