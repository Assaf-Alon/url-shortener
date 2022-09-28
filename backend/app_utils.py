def is_short_url_valid(short_url):
    with open('forbidden_short_urls.txt') as file:
        if short_url in file.read():
            return False
    return True
    
    
def is_user_id_valid(user_id):
    with open('forbidden_user_ids.txt') as file:
        if user_id in file.read():
            return False
    return True

def get_translation_dict(args):
    user_id  = args["user_id"] if args["user_id"] != None else "anonymous"
    
    trans_dict =  {"short_url": args['short_url'],
                   "long_url":  args['long_url'],
                   "user_id":   user_id}

    return trans_dict

    