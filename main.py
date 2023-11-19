import os
import numpy as np
from lut_tree import LUT_TREE

class give_nodelabel():
    
    def __init__(self) -> None:
        self.threshold = None

    def create_LUT_tree(self,filename,wire_label_dict={}):
        print(filename)
        with open(filename,'r') as f:
            LUT_tree = LUT_TREE()
            code_text = ''
            for line in f:
                code_text += line
                if ';\n' in line:
                    LUT_tree.analysis_code(code_text)
                    code_text = ''
        if wire_label_dict != {}:
            for wire in wire_label_dict['trojan']:
                if wire in LUT_tree.wire_dict:
                    LUT_tree.wire_dict[wire].type = 'output'
                    LUT_tree.wire_dict[wire].name = wire
                    LUT_tree.output_dict[wire] = LUT_tree.wire_dict[wire]
                    del LUT_tree.wire_dict[wire]
        return LUT_tree

    def optimize_LUT_tree(self,LUT_tree):
        node_dict = LUT_tree.node_dict
        for key in list(node_dict.keys()):
            node = node_dict[key]
            if node.type == 'wire':
                del node_dict[key]
                continue
            elif node.grand_num == 0 and node.child_num == 0:
                continue
            else:
                i = 0
                while True:
                    if i >= node.child_num:
                        break
                    elif node.child_list[i].type == 'wire':
                        node.child_list[i] = node.child_list[i].child_list[0]
                        continue
                    else:
                        i += 1

        return LUT_tree

    def calculate_prob(self,node):
        if node.type == 'dffeas':
            node.prob_one = node.child_list[4].prob_one
        elif node.type == 'INV':
            node.prob_one = 1 - node.child_list[0].prob_one
        elif node.type == 'MUX':
            sel = node.child_list[0]
            sel_1 = node.child_list[1]
            sel_0 = node.child_list[2]
            node.prob_one = sel.prob_one * sel_1.prob_one + (1-sel.prob_one) * sel_0.prob_one
        elif node.type == 'LUT':
            init_matrix = np.array(list(map(int,node.INIT)))
            _matrix = 1
            for i in range(node.child_num - 1,-1,-1):
                prob_one = node.child_list[i].prob_one
                prob_matrix = np.array([prob_one,1-prob_one]).reshape(1,-1)
                _matrix = np.dot(_matrix,prob_matrix).reshape(-1,1)
            node.prob_one = np.dot(init_matrix,_matrix).item()
        elif node.type == 'output':
            node.prob_one = node.child_list[0].prob_one
        elif node.type == 'wire':
            node.prob_one = node.child_list[0].prob_one
        else:
            int('error')

    def get_node_probability(self,LUT_tree):
        list_node_prob1 = []
        node_dict = LUT_tree.node_dict
        travel_list = []
        for key in node_dict:
            root = node_dict[key]
            if root.prob_one != None:
                continue
            else:
                travel_list.append(root)
                while True:
                    if travel_list == []:
                        break
                    else:
                        node = travel_list[-1]
                        if node.traverse_num != node.child_num:
                            next_node = node.child_list[node.traverse_num]
                            node.traverse_num += 1
                            if next_node.child_num == 0:
                                list_node_prob1.append([next_node.name, next_node.prob_one])
                                continue
                            elif next_node.prob_one != None:
                                continue
                            else:
                                travel_list.append(next_node)
                        else:
                            self.calculate_prob(node)
                            list_node_prob1.append([node.name, node.prob_one])
                            node.traverse_num = 0
                            travel_list.pop(-1)

        return list_node_prob1

def main(this_dir):
    give_label = give_nodelabel()
    LUT_tree = give_label.create_LUT_tree(os.path.join(this_dir,'graph_intel.v'))
    LUT_tree = give_label.optimize_LUT_tree(LUT_tree)
    list_node_prob1 = give_label.get_node_probability(LUT_tree)
    np.savetxt(os.path.join(this_dir,'prob1.txt'), list_node_prob1, fmt='%s %s')

if __name__ == '__main__':
    main('example')