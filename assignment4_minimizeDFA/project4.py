import xml.etree.ElementTree as ET

alphabet = {'0', '1'}


def read_file_jflap(file_name):
    """
    Get data of automata with format is .jff has name is file_name
        Input: file .jff automata
        Output: return Q, alphabet, from, to, read, start, F
    """
    Q = set()
    froms, tos, reads = [], [], []
    start = ''
    F = {}
    try:
        tree = ET.parse(file_name)
        root = tree.getroot()
    except:
        print('File not found.')
    for state in root.iter('state'):
        Q.add(state.attrib.get('id'))

    froms = [_from.text for _from in root.iter('from')]
    tos = [_to.text for _to in root.iter('to')]
    reads = [_read.text for _read in root.iter('read')]
    for state_initial in root.iter('state'):
        if state_initial.findall('initial'):
            start = state_initial.attrib.get('id')

    F = {state.attrib.get('id') for state in root.iter(
        'state') if state.findall('final')}
    M = froms, reads, tos

    return Q, froms, tos, reads, start, F


Q, froms, tos, reads, start, F = read_file_jflap('/home/haitien/Downloads/VSCode/Automata/assignment4_minimizeDFA/input_DFA.jff')
# print(Q)
# print(start)
# print(F)
print(tos)

# Transition function
def transition(_from, _read, froms=froms, reads=reads, tos=tos):
    for i in range(len(reads)):
        if froms[i] == _from and reads[i] == _read:
            return tos[i]

def inverse_transition(_to, _read, froms=froms, reads=reads, tos=tos):
    res = set()
    for i in range(len(reads)):
        if tos[i] == _to and reads[i] == _read:
            res.add(froms[i])
    return res

graph = dict()
for element in Q:
    graph[element] = [transition(element, '0'), transition(element, '1')]
# print(graph)

# DFS
def dfs(graph, start, visited=[]):
    if start not in visited:
        visited.append(start)
        for n in graph[start]:
            dfs(graph, n, visited)
    return visited
visited = dfs(graph, start) # new states (Q_new) after using dfs 
# print(visited)

def minimize_dfa(F=F):
    pi = {0,1}
    
    block = dict()
    for p in Q:
        if p in F:
            block[p] = '1'
        else:
            block[p] = '0'
    while True:
        bags = set()
        _pi = pi
        cache = block.copy()
        for q in visited:
            block[q] = cache[q] + cache[transition(q, '0')] + cache[transition(q, '1')]
            bags.add(block[q])

        counter = len(bags)
        pi = set(i for i in range(counter))
        if len(_pi) == counter:
            break
    rev_block = {}
    for key, value in block.items():
        if len(value) > 1:
            rev_block.setdefault(value, set()).add(key)
    return rev_block, counter
print(minimize_dfa(F))
rev_block, counter = minimize_dfa()


def transitions(s, a): 
    next_states = set()
    for q in s:
        next_states = next_states.union(transition(q, a))
    return next_states

Q_new = [value for value in rev_block.values()]
froms_new = Q_new*2
reads_new = [None]*len(froms_new)
tos_new = [None]*len(froms_new)
start_new = None
F_new = []
for i in range(2*len(Q_new)):
    if i < len(Q_new):
        reads_new[i] = '0'
        for q in Q_new:
            if transitions(froms_new[i], '0').issubset(q):
                tos_new[i] = q
    else:
        reads_new[i] = '1'
        for q in Q_new:
            if transitions(froms_new[i], '1').issubset(q):
                tos_new[i] = q


for q in Q_new:
    if start in q:
        start_new = q
    for f in F:
        if f in q and q not in F_new:
            F_new.append(q)

print(Q_new)
print(froms_new)
print(reads_new)
print(tos_new)
print(start_new)
print(F_new)

F = []
Q = []
for i in range(len(Q_new)):
    Q.append(str(i))
froms = Q*2
reads = ['0' for _ in range(len(Q))] + ['1' for _ in range(len(Q))]
tos = [None]*len(froms)
for i in range(len(Q)):
    for j in range(len(froms)):
        if tos_new[j] == Q_new[i]:
            tos[j] = Q[i]
    if start_new == Q_new[i]:
        start = Q[i]
    for j in range(len(F_new)):
        if F_new[j] == Q_new[i]:
            F.append(Q[i])

print(Q)
print(froms)
print(reads)
print(tos)
print(start)
print(F)
def write_file_jflap(file_name, Q, froms, reads, tos, start, F):
    """
    This function allows output a file .jff with data of automata 
    """
    pass
    root = ET.Element('structure')
    type_ = ET.SubElement(root, 'type')
    type_.text = 'fa'
    automaton = ET.SubElement(root, 'automaton')
    for i in range(len(Q)):
        state = ET.SubElement(automaton, 'state', {
                              'id': str(i), 'name': 'q' + str(i)})
        x = ET.SubElement(state, 'x')
        y = ET.SubElement(state, 'y')
        x.text = str(i*100 + 150)
        y.text = str(200)

        if str(i) == start:
            initial = ET.SubElement(state, 'initial')
        if str(i) in F:
            final = ET.SubElement(state, 'final')
    for j in range(len(reads)):
        transition = ET.SubElement(automaton, 'transition')
        from_ = ET.SubElement(transition, 'from')
        from_.text = str(froms[j])
        to = ET.SubElement(transition, 'to')
        to.text = str(tos[j])
        read = ET.SubElement(transition, 'read')
        read.text = str(reads[j])

    tree = ET.ElementTree(root)
    # output file
    tree.write(file_name, encoding="utf8", method='xml')
    print('Builded success file {}'.format(file_name))


write_file_jflap('/home/haitien/Downloads/VSCode/Automata/assignment4_minimizeDFA/output_minDFA.xml', Q, froms, reads, tos, start, F)
