
class NFA:
    '''Табличное представление НКА.'''

    def __init__(self, states, alphabet, table, start_state, accepting_states):
        '''Сохраняет компоненты автомата.'''
        self.states = states
        self.alphabet = alphabet
        self.table = table
        self.start_state = start_state
        self.accepting_states = accepting_states

    def run(self, word_symbols):
        '''Прогоняет цепочку методом множества активных состояний.'''
        current_set = set()
        current_set.add(self.start_state)
        trace = [frozenset(current_set)]
        for symbol in word_symbols:
            next_set = set()
            for state in current_set:
                destinations = self.table[state].get(symbol)
                if destinations is not None:
                    for d in destinations:
                        next_set.add(d)
            current_set = next_set
            trace.append(frozenset(current_set))
            if len(current_set) == 0:
                break
        accepted = len(current_set & self.accepting_states) > 0
        return accepted, trace

    def print_table(self):
        '''Печатает таблицу переходов НКА.'''
        print("Таблица переходов НКА:")
        print("state".ljust(8) + "a".ljust(12) + "b".ljust(12) + "accept")
        for state in self.states:
            row = state.ljust(8)
            for symbol in self.alphabet:
                dest = self.table[state].get(symbol, set())
                cell = "{"
                first = True
                for d in sorted(dest):
                    if not first:
                        cell = cell + ","
                    cell = cell + d
                    first = False
                cell = cell + "}"
                row += cell.ljust(12)
            row += "yes" if state in self.accepting_states else "no"
            print(row)


def build_nfa_a_or_b_star_a_star():
    '''Строит НКА на 2 состояниях.'''
    states = ["q0", "q1"]
    alphabet = ("a", "b")
    table = {
        "q0": {"a": {"q1"}, "b": {"q0"}},
        "q1": {"a": {"q1"}},
    }
    return NFA(states, alphabet, table, "q0", {"q0", "q1"})


def read_ab_word(raw):
    '''Читает строку посимвольно, возвращает список символов.'''
    symbols = []
    for ch in raw:
        if ch == 'a' or ch == 'b':
            symbols.append(ch)
    return symbols


def main():
    print("НКА: {a^n : n>=1} U {b^m a^k : m,k>=0}")
    nfa = build_nfa_a_or_b_star_a_star()
    print(f"Число состояний НКА: {len(nfa.states)}")
    print()
    nfa.print_table()

    test_words = ["", "a", "aaa", "b", "bbb", "bba", "ba",
                  "ab", "bab", "aab"]
    print()
    print("Тестовые прогоны:")
    for raw in test_words:
        symbols = read_ab_word(raw)
        accepted, trace = nfa.run(symbols)
        label = raw if raw != "" else "ε"
        print(f"  w = {label:<10} {'Accept' if accepted else 'Reject'}")

if __name__ == "__main__":
    main()
