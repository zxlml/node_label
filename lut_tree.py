import re
class LUT_NODE():
    def __init__(self) -> None:
        self.no = None
        self.name = None
        self.type = None
        self.INIT = None
        self.node_label = 0
        self.child_list = []
        self.child_num = 0
        self.grand_num = 0
        self.traverse_num = 0
        self.prob_one = None

class LUT_TREE():
    def __init__(self) -> None:
        self.input_dict = {}
        self.output_dict = {}
        self.wire_dict = {}
        self.node_dict = {}
        self.Multi_bit_dict = {}

    def analysis_code(self,code_text):
        if '  wire ' in code_text:
            self.read_wire(code_text)
        elif '  input ' in code_text:
            self.read_input(code_text)
        elif '  output ' in code_text:
            self.read_output(code_text)
        elif '  fiftyfivenm_lcell_comb ' in code_text:
            self.read_LUT(code_text)
        elif '  assign ' in code_text:
            self.read_assign(code_text)
        elif 'module ' in code_text:
            pass
        elif '  dffeas ' in code_text:
            self.read_dffeas(code_text)
        else:
            print(code_text)
            int('error')
        
    def read_wire(self,code_text):
        pattern_Multi_bit = re.compile(r'\[[^ ]*\:[^ ]*\][^\;]*')
        patt_Multi_list = pattern_Multi_bit.findall(code_text)
        if patt_Multi_list == []:
            pattern_bit = re.compile(r'[^ ]*[^;];')
            wire = pattern_bit.findall(code_text)[0][:-1]
            if wire in self.input_dict or wire in self.output_dict:
                return 0
            if wire in self.wire_dict:
                print(code_text)
                int('error')
            wire_node = LUT_NODE()
            wire_node.name = wire
            wire_node.type = 'wire'
            self.wire_dict[wire] = wire_node
            self.node_dict[wire] = wire_node
        else:
            pattern_ = re.compile(r'\[[^ ]*\:[^ ]*\]')
            patt_list = pattern_.findall(patt_Multi_list[0])
            list_str = patt_list[0]
            high_low = list_str[1:-1].split(':')
            wire_high = int(high_low[0])
            wire_low = int(high_low[1])
            if wire_high < wire_low:
                wire_high, wire_low = wire_low, wire_high
            if wire_high < wire_low:
                print(code_text)
                int('error')
            wire_name = patt_Multi_list[0].replace('%s '%list_str,'')
            self.Multi_bit_dict[wire_name] = '%s%s'%(wire_name,list_str)
            for item in range(wire_low,wire_high + 1):
                wire = '%s[%s]'%(wire_name,item)
                if wire in self.input_dict or wire in self.output_dict:
                    return 0
                if wire in self.wire_dict:
                    print(code_text)
                    int('error')
                wire_node = LUT_NODE()
                wire_node.name = wire
                wire_node.type = 'wire'
                self.wire_dict[wire] = wire_node
                self.node_dict[wire] = wire_node

    def read_input(self,code_text):
        pattern_Multi_bit = re.compile(r'\[[^ ]*\:[^ ]*\][^\;]*')
        patt_Multi_list = pattern_Multi_bit.findall(code_text)
        if patt_Multi_list == []:
            pattern_bit = re.compile(r'[^ ]*[^;];')
            input = pattern_bit.findall(code_text)[0][:-1]
            if input in self.input_dict:
                print(code_text)
                int('error')
            input_node = LUT_NODE()
            input_node.name = input
            input_node.type = 'input'
            input_node.prob_one = 0.5
            self.input_dict[input] = input_node
            self.node_dict[input] = input_node
        else:
            pattern_ = re.compile(r'\[[^ ]*\:[^ ]*\]')
            patt_list = pattern_.findall(patt_Multi_list[0])
            list_str = patt_list[0]
            high_low = list_str[1:-1].split(':')
            input_high = int(high_low[0])
            input_low = int(high_low[1])
            if input_high < input_low:
                input_high,input_low = input_low,input_high
            if input_high < input_low:
                print(code_text)
                int('error')
            input_name = patt_Multi_list[0].replace('%s '%list_str,'')
            self.Multi_bit_dict[input_name] = '%s%s'%(input_name,list_str)
            for item in range(input_low,input_high + 1):
                input = '%s[%s]'%(input_name,item)
                if input in self.input_dict:
                    print(code_text)
                    int('error')
                input_node = LUT_NODE()
                input_node.name = input
                input_node.type = 'input'
                input_node.prob_one = 0.5
                self.input_dict[input] = input_node
                self.node_dict[input] = input_node

    def read_output(self,code_text):
        pattern_Multi_bit = re.compile(r'\[[^ ]*\:[^ ]*\][^\;]*')
        patt_Multi_list = pattern_Multi_bit.findall(code_text)
        if patt_Multi_list == []:
            pattern_bit = re.compile(r'[^ ]*[^;];')
            output = pattern_bit.findall(code_text)[0][:-1]
            if output in self.output_dict:
                print(code_text)
                int('error')
            output_node = LUT_NODE()
            output_node.name = output
            output_node.type = 'output'
            self.output_dict[output] = output_node
            self.node_dict[output] = output_node
        else:
            pattern_ = re.compile(r'\[[^ ]*\:[^ ]*\]')
            patt_list = pattern_.findall(patt_Multi_list[0])
            list_str = patt_list[0]
            high_low = list_str[1:-1].split(':')
            output_high = int(high_low[0])
            output_low = int(high_low[1])
            if output_high < output_low:
                output_high, output_low = output_low, output_high
            if output_high < output_low:
                print(code_text)
                int('error')
            output_name = patt_Multi_list[0].replace('%s '%list_str,'')
            self.Multi_bit_dict[output_name] = '%s%s'%(output_name,list_str)
            for item in range(output_low,output_high + 1):
                output = '%s[%s]'%(output_name,item)
                if output in self.output_dict:
                    print(code_text)
                    int('error')
                output_node = LUT_NODE()
                output_node.name = output
                output_node.type = 'output'
                self.output_dict[output] = output_node
                self.node_dict[output] = output_node

    def read_LUT(self,code_text):
        patt_name = re.compile(r'\) _.*_ \(')
        LUT_name = patt_name.findall(code_text)[0][2:-2]
        patt_INIT = re.compile(r'\.lut_mask\(.*\)')
        INIT = re.sub(r'.*\'b','',patt_INIT.findall(code_text)[0][:-1])
        LUT_node = LUT_NODE()
        LUT_node.name = LUT_name
        LUT_node.type = 'LUT'
        LUT_node.INIT = INIT
        self.node_dict[LUT_name] = LUT_node
        patt_O = re.compile(r'\.combout\(.*\)')
        O_name = patt_O.findall(code_text)[0][9:-1]
        if O_name in self.output_dict:
            O = self.output_dict[O_name]
        elif O_name in self.input_dict:
            O = self.input_dict[O_name]
        elif O_name in self.wire_dict:
            O = self.wire_dict[O_name]
        else:
            print(code_text)
            int('error')
        O.child_list.append(LUT_node)
        O.child_num += 1
        LUT_node.grand_num += 1
        for item in ['a','b','c','d']:
            patt_I = re.compile('\.data%s\(.*\)'%item)
            I_name = patt_I.findall(code_text)[0][7:-1]
            if I_name in self.output_dict:
                I = self.output_dict[I_name]
            elif I_name in self.input_dict:
                I = self.input_dict[I_name]
            elif I_name in self.wire_dict:
                I = self.wire_dict[I_name]
            elif '\'b' in I_name:
                self.create_constant(I_name)
                I = self.input_dict[I_name]
            else:
                print(code_text)
                int('error')
            LUT_node.child_list.append(I)
            LUT_node.child_num += 1
            I.grand_num += 1
    
    def read_INV(self,code_text):
        wire_list = code_text[9:-2].split(' = ~ ')
        if len(wire_list) != 2:
            int('error')
        INV_node = LUT_NODE()
        INV_node.name = 'INV%s'%wire_list[0]
        INV_node.type = 'INV'
        self.node_dict[INV_node.name] = INV_node
        if wire_list[0] in self.output_dict:
            O = self.output_dict[wire_list[0]]
        elif wire_list[0] in self.input_dict:
            O = self.input_dict[wire_list[0]]
        elif wire_list[0] in self.wire_dict:
            O = self.wire_dict[wire_list[0]]
        else:
            print(code_text)
            int('error')
        O.child_list.append(INV_node)
        O.child_num += 1
        INV_node.grand_num += 1
        if wire_list[1] in self.output_dict:
            I = self.output_dict[wire_list[1]]
        elif wire_list[1] in self.input_dict:
            I = self.input_dict[wire_list[1]]
        elif wire_list[1] in self.wire_dict:
            I = self.wire_dict[wire_list[1]]
        else:
            print(code_text)
            int('error')
        INV_node.child_list.append(I)
        INV_node.child_num += 1
        I.grand_num += 1

    def read_MUX(self,code_text):
        O_and_ = code_text[9:-2].split(' = ')
        if len(O_and_) != 2:
            int('error')
        select_and_ = O_and_[1].split(' ? ')
        if len(select_and_) != 2:
            int('error')
        I_and_ = select_and_[1].split(' : ')
        if len(I_and_) != 2:
            int('error')
        MUX_node = LUT_NODE()
        MUX_node.name = 'MUX%s'%O_and_[0]
        MUX_node.type = 'MUX'
        self.node_dict[MUX_node.name] = MUX_node
        if O_and_[0] in self.output_dict:
            O = self.output_dict[O_and_[0]]
        elif O_and_[0] in self.input_dict:
            O = self.input_dict[O_and_[0]]
        elif O_and_[0] in self.wire_dict:
            O = self.wire_dict[O_and_[0]]
        else:
            print(code_text)
            int('error')
        O.child_list.append(MUX_node)
        O.child_num += 1
        MUX_node.grand_num += 1
        for item in [select_and_[0],I_and_[0],I_and_[1]]:
            if item in self.output_dict:
                I = self.output_dict[item]
            elif item in self.input_dict:
                I = self.input_dict[item]
            elif item in self.wire_dict:
                I = self.wire_dict[item]
            elif '\'b' in item:
                self.create_constant(item)
                I = self.input_dict[item]
            else:
                print(code_text)
                int('error')
            MUX_node.child_list.append(I)
            MUX_node.child_num += 1
            I.grand_num += 1

    def read_assign(self,code_text):
        if '~' in code_text:
            self.read_INV(code_text)
            return 0
        if '?' in code_text:
            self.read_MUX(code_text)
            return 0
        left_right = code_text[9:-2].split(' = ')
        assign_left = left_right[0]
        assign_right = left_right[1]
        if assign_left[0] == '{' and assign_left[-1] == '}':
            splicing_str = assign_left[2:-2]
            splicing_list = splicing_str.split(', ')
            left_list = []
            left_len = 0
            for item in splicing_list:
                return_list, _len = self.wires_analysis(item)
                left_list += return_list
                left_len += _len
        else:
            left_list ,left_len = self.wires_analysis(assign_left)
        if assign_right[0] == '{' and assign_right[-1] == '}':
            splicing_str = assign_right[2:-2]
            splicing_list = splicing_str.split(', ')
            right_list = []
            right_len = 0
            for item in splicing_list:
                return_list, _len = self.wires_analysis(item)
                right_list += return_list
                right_len += _len
        else:
            right_list, right_len = self.wires_analysis(assign_right)
        if left_len != right_len:
            print(code_text)
            int('error')
        len_list = left_len
        for item in range(len_list):
            right_node = right_list[item]
            left_node = left_list[item]
            left_node.child_list.append(right_node)
            left_node.child_num += 1
            right_node.grand_num += 1

    def wires_analysis(self,wire_str):
        if wire_str in self.Multi_bit_dict:
            wire_str = self.Multi_bit_dict[wire_str]
        pattern_list = re.compile(r'\[[0-9]*\:[0-9]*\]')
        list_result = pattern_list.findall(wire_str)
        if list_result == []:
            pattern_value = re.compile(r'[0-9]*\'b[0-9]*')
            value_result = pattern_value.findall(wire_str)
            if value_result == []:
                if wire_str in self.output_dict:
                    wire_node = self.output_dict[wire_str]
                elif wire_str in self.input_dict:
                    wire_node = self.input_dict[wire_str]
                elif wire_str in self.wire_dict:
                    wire_node = self.wire_dict[wire_str]
                else:
                    print(wire_str)
                    int('error')
                empty_list = []
                empty_list.append(wire_node)
                return empty_list, 1
            else:
                split_list = wire_str.split('\'b')
                wire_list = list(split_list[1]) 
                len_list = int(split_list[0])
                empty_list = []
                for item in wire_list:
                    wire_value = '1\'b%s'%item
                    if wire_value not in self.input_dict:
                        self.create_constant(wire_value)
                    empty_list.append(self.input_dict[wire_value])
                return empty_list, len_list
        else:
            match_list = list_result[-1]
            high_low = match_list[1:-1].split(':')
            wire_high = int(high_low[0])
            wire_low = int(high_low[1])
            if wire_high < wire_low:
                wire_high, wire_low = wire_low, wire_high
            wire_list = []
            wire_name = wire_str.replace(match_list,'')
            for item in range(wire_low,wire_high + 1):
                wire = '%s[%s]'%(wire_name,item)
                if wire in self.output_dict:
                    wire_list.append(self.output_dict[wire])
                elif wire in self.input_dict:
                    wire_list.append(self.input_dict[wire])
                elif wire in self.wire_dict:
                    wire_list.append(self.wire_dict[wire])
                else:
                    print(wire_str)
                    int('error')
            return wire_list[::-1], len(wire_list)

    def create_constant(self,constant):
        constant_node = LUT_NODE()
        constant_node.name = constant
        constant_node.type = 'input'
        self.node_dict[constant] = constant_node
        if '0' in constant:
            constant_node.prob_one = 0
        elif '1' in constant:
            constant_node.prob_one = 1
        else:
            int('error')
        self.input_dict[constant] = constant_node

    def read_dffeas(self,code_text):
        dffeas_name = re.compile(r' _.*_ ').findall(code_text)[0][1:-1]
        q_name = re.compile(r'\.q\(.*\)').findall(code_text)[0][3:-1]
        dffeas_node = LUT_NODE()
        dffeas_node.name = dffeas_name
        dffeas_node.type = 'dffeas'
        self.node_dict[dffeas_name] = dffeas_node
        for item in ['clk','clrn','d','ena']:
            I_name = re.compile('\.%s\(.*\)'%item).findall(code_text)[0][2+len(item):-1]
            if I_name in self.output_dict:
                I = self.output_dict[I_name]
            elif I_name in self.input_dict:
                I = self.input_dict[I_name]
            elif I_name in self.wire_dict:
                I = self.wire_dict[I_name]
            elif '\'b' in I_name:
                self.create_constant(I_name)
                I = self.input_dict[I_name]
            else:
                print(code_text)
                int('error')
            dffeas_node.child_list.append(I)
            dffeas_node.child_num += 1
            I.grand_num += 1
        if q_name in self.output_dict:
            q = self.output_dict[q_name]
        elif q_name in self.input_dict:
            q = self.input_dict[q_name]
        elif q_name in self.wire_dict:
            q = self.wire_dict[q_name]
        else:
            print(code_text)
            int('error')
        q.child_list.append(dffeas_node)
        q.child_num += 1
        dffeas_node.grand_num += 1