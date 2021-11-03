from lbn.input.node import init_nodes_from_json
FORMULA_FILE = '../../../examples/example_formula'
Domain_FILE = '../../../examples/node_domain'

def map_formula(formula: str, nodes: list):
    formula_list = formula.split('\n\n')
    print(f'formula_list =  {formula_list}')
    for node in nodes:
        dict = {}
        for fm in formula_list:
            if f'{node.get_name()}::\n' in fm:
                changed_fm = fm.replace(f'{node.get_name()}::\n', '')
                changed_fm = changed_fm.replace(' ','')
                changed_fm_list = changed_fm.split('\n')
                print(changed_fm_list)
                for changed_fm_part in changed_fm_list:
                    if ':' not in changed_fm_part:
                        dict['self'] = float(changed_fm_part)
                    else:
                        dict[changed_fm_part[
                             :changed_fm_part.index(':')]] \
                            = changed_fm_part[changed_fm_part.index(':') + 1:]
        node.set_distributions(dict)
    return nodes


def read_formula(formula_file):
    with open(formula_file, 'r') as f:
        return f.read()


nodes = init_nodes_from_json(Domain_FILE)

nodes_ = map_formula(read_formula(FORMULA_FILE), nodes)
for node in nodes_:
    print(node.get_distributions())

