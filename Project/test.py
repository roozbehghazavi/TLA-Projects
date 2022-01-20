import copy

class Regex:
    def __init__(self, states, alphabets, init_state, final_states, transition_funct):
        self.states = states
        self.alphabets = alphabets
        self.init_state = init_state
        self.final_states = final_states
        self.transition_funct = transition_funct
        self.regex = ''
        self.ds = {}
        self.transition_dict = {}
        self._setTransDictionary()

    def _setTransDictionary(self):
        dict_states = {r: {c: ':L' for c in self.states} for r in self.states}
        for i in self.states:
            for j in self.states:
                indices = [ii for ii, v in enumerate(self.transition_funct[i]) if v == j]  # get indices of states
                if len(indices) != 0:
                    dict_states[i][j] = '+'.join([str(self.alphabets[v])
                                                 for v in indices])
        self.ds = dict_states
        self.transition_dict = copy.deepcopy(dict_states) 

    def _getIntermediateStates(self):
        return [state for state in self.states if state not in ([self.init_state] + self.final_states)]

    def _getPredecessors(self, state):
        return [key for key, value in self.ds.items() if state in value.keys() and value[state] != ':L' and key != state]

    def _getSuccessors(self, state):
        return [key for key, value in self.ds[state].items() if value != ':L' and key != state]

    def _getIfLoop(self, state):
        if self.ds[state][state] != ':L':
            return self.ds[state][state]
        else:
            return ''

    def _optimize(self, r):
        # most develop
        r = r.replace('(:L)', '').replace('()', '').replace('(+', '(')
        for i in self.alphabets:
            r = r.replace('('+i+')', i)
            r = r.replace('('+i+'*)', i+'*')
            r = r.replace('('+i+'*)', i+'*')
            r = r.replace('**', '*')
        for i in self.alphabets:
            r = r.replace('('+i+'*'+i+')', i+'^+')
        return r

    def genRegex(self):
        intermediate_states = self._getIntermediateStates()
        dict_states = self.ds
        for inter in intermediate_states:
            predecessors = self._getPredecessors(inter)
            successors = self._getSuccessors(inter)
            for i in predecessors:
                for j in successors:
                    inter_loop = self._getIfLoop(inter)
                    dict_states[i][j] = '+'.join(('(' + dict_states[i][j] + ')', ''.join(('(' + dict_states[i][
                        inter] + ')', '(' + inter_loop + ')' + '*', '(' + dict_states[inter][j] + ')'))))

            dict_states = {r: {c: v for c, v in val.items() if c != inter} for r, val in dict_states.items() if
                           r != inter}
            self.ds = copy.deepcopy(dict_states)

        init_loop = dict_states[self.init_state][self.init_state]
        init_to_final = dict_states[self.init_state][self.final_states[0]] + '(' + dict_states[self.final_states[0]][
            self.final_states[0]] + ')' + '*'
        final_to_init = dict_states[self.final_states[0]][self.init_state]
        re = '(' + '(' + init_loop + ')' + '+' + '(' + init_to_final + ')' +\
            '(' + final_to_init + ')' + ')' + '*' + '(' + init_to_final + ')'

        return self._optimize(re)