import networkx as nx
import os


def parse_inf(f_name):
    with open(f_name, 'r', encoding='utf-8') as f:
        text = f.read().split('\n')
    for i, conn in enumerate(text):
        text[i] = conn.split('\t')
    return text


def parse_all(dir):
    l = os.listdir(dir)
    fin = []
    for file in l:
        with open(dir + os.sep + file, 'r', encoding='utf-8') as f:
            text = f.read().split('\n')
            for t in text:
                fin.append(t)
    for i, conn in enumerate(fin):
        fin[i] = conn.split('\t')
    return fin


def create_graph(data, f_name):
    G = nx.Graph()
    for n in data:
        if n[0] not in G.nodes():
            G.add_node(n[0])
        if n[1] not in G.nodes():
            G.add_node(n[1])
        if (n[0], n[1]) not in G.edges():
            G.add_edge(n[0], n[1])
    nx.write_gexf(G, f_name)


def main():
    dirs = ['creakley_hall', 'paranoid', 'train_robbery', 'hamarin', 'escape_artist']
    for dir in dirs:
        if dir + '_gexf' not in os.listdir('graphs'):
            os.mkdir('graphs' + os.sep + dir + '_gexf')
        l = os.listdir(dir)
        for f in l:
            temp = f.split('.')[0]
            create_graph(parse_inf(dir + os.sep + f), 'graphs' + os.sep + dir + '_gexf' + os.sep + temp + '.gexf')
        create_graph(parse_all(dir), 'graphs' + os.sep + dir + '_gexf' + os.sep + dir + '.gexf')


if __name__ == '__main__':
    if 'graphs' not in os.listdir('.'):
        os.mkdir('graphs')
    main()