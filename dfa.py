
class DFA:
    '''Табличное представление ДКА.'''

    def __init__(self, states, alphabet, table, start_state, accepting_states):
        '''Сохраняет компоненты автомата (Q, Sigma, delta, q0, F).'''
        self.states = states
        self.alphabet = alphabet
        self.table = table
        self.start_state = start_state
        self.accepting_states = accepting_states

    def run(self, word_symbols):
        '''Прогоняет цепочку по таблице переходов, возвращает результат и трассу.'''
        current = self.start_state
        trace = [current]
        for symbol in word_symbols:
            current = self.table[current][symbol]
            trace.append(current)
        accepted = current in self.accepting_states
        return accepted, trace

    def print_table(self):
        '''Печатает таблицу переходов ДКА.'''
        print("Таблица переходов ДКА:")
        print("state".ljust(10) + "0".ljust(10) + "1".ljust(10) + "accept")
        for state in self.states:
            row = state_name(state).ljust(10)
            for symbol in self.alphabet:
                row += state_name(self.table[state][symbol]).ljust(10)
            row += "yes" if state in self.accepting_states else "no"
            print(row)


def state_name(state_tuple):
    '''Строит имя состояния вида "q00000" по кортежу битов.'''
    name = "q"
    for bit in state_tuple:
        name = name + chr(48 + bit)
    return name


def build_dfa_position5():
    '''Строит минимальный ДКА.'''
    alphabet = (0, 1)
    states = []

    def generate(prefix, depth):
        '''Перечисляет все 32 кортежа длины 5.'''
        if depth == 5:
            states.append(prefix)
            return
        generate(prefix + (0,), depth + 1)
        generate(prefix + (1,), depth + 1)

    generate((), 0)

    table = {}
    for state in states:
        table[state] = {}
        for symbol in alphabet:
            table[state][symbol] = state[1:] + (symbol,)

    start_state = (0, 0, 0, 0, 0)

    accepting_states = set()
    for state in states:
        if state[0] == 1:
            accepting_states.add(state)

    return DFA(states, alphabet, table, start_state, accepting_states)


def read_binary_word(raw):
    '''Читает строку посимвольно, возвращает список.'''
    symbols = []
    for ch in raw:
        if ch == '0':
            symbols.append(0)
        elif ch == '1':
            symbols.append(1)
    return symbols


if __name__ == "__main__":
    print("ДКА: на пятой позиции справа стоит 1")
    dfa = build_dfa_position5()
    print(f"Число состояний ДКА: {len(dfa.states)}")
    print()
    dfa.print_table()

    test_words = ["1", "10000", "01111", "110000", "100000",
                  "111111", "00001", "0000100"]
    print()
    print("Тестовые прогоны:")
    for raw in test_words:
        symbols = read_binary_word(raw)
        accepted, trace = dfa.run(symbols)
        print(f"  w = {raw:<10} {'Accept' if accepted else 'Reject'}")
