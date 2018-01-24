import json
from collections import deque

def table_to_dict_list(table):
    dict_list = []
    for i in range(1, len(table)):
        tmp_dict = {}
        for j in range(0, len(table[i])):
            tmp_dict[table[0][j]] = table[i][j]
        dict_list.append(tmp_dict)

    return sorted(dict_list, key = lambda x: x['Code'])

def multiple_of_three(data):
    return [x for x in data if x % 3 == 0]

def pick_GlossTerm(data):
    json_obj = json.loads(data)
    return json_obj['glossary']['GlossDiv']['GlossList']['GlossEntry']['GlossTerm']

def sort_and_distinct(data):
    return sorted(list(set(data)))

def sort_by_amount(data):
    return sorted(data, key = lambda item: item.amount, reverse = True)

def calc(cmd, x, y):
    op = None
    if cmd == 'add':
      op = lambda x, y: x + y
    elif cmd == 'subtract':
      op = lambda x, y: x - y
    elif cmd == 'multiply':
      op = lambda x, y: x * y
    elif cmd == 'divide':
      op = lambda x, y: x / y

    return op(x, y)

def find_deepest_child(tree):
    deepest = ""

    queue = deque([])
    queue.append(tree)

    while queue:
        item = queue.popleft()
        if item:
            for key, value in item.items():
                deepest = key
                queue.append(value)

    return deepest

def find_nodes_that_contains_more_than_three_children(tree):
    nodes = set()

    queue = deque([])
    queue.append(tree)

    while queue:
        item = queue.popleft()
        if item:
            for key, value in item.items():
                if value and len(value) >= 3:
                    nodes.add(key)
                queue.append(value)

    return nodes

def count_of_all_distributions_of_linux(tree):
    dists = 0

    queue = deque([])
    queue.append(tree['Linux'])

    while queue:
        item = queue.popleft()
        if item:
            for key, value in item.items():
                queue.append(value)
                dists += 1

    return dists

def Notice(content):
    return {'obj_type': 'notice', 'val': content}

def Message(userid, content):
    return {'obj_type': 'msg', 'val': content, 'uid': userid}

def render_messages(msgs, current_userid):
    page = ''

    for msg in msgs:
        tmp_str = ''
        if msg['obj_type'] == 'notice':
            tmp_str = '''<li class="notice">''' + msg['val'] + '''</li>'''
        elif msg['obj_type'] == 'msg':
            if current_userid == msg['uid']:
                direction = 'right'
            else:
                direction = 'left'

            tmp_str = '''\n<li class="''' + direction + '''">\n''' \
                    + '''    <img class="profile" src="${user_image(''' + str(msg['uid']) + ''')}">\n''' \
                    + '''    <div class="message-content">''' + msg['val'] + '''</div>\n''' \
                    + '''</li>'''

        page += tmp_str

    return page




