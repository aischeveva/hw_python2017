import sys
import gensim, logging
import networkx as nx
import json
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def open_model():
    m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
    if m.endswith('.vec.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
    elif m.endswith('.bin.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    else:
        model = gensim.models.KeyedVectors.load(m)
    model.init_sims(replace=True)
    return model


def count_dist(m):
    with open('field.txt', 'r', encoding='utf-8') as f:
        field = f.read().split()
    dic_w = {}
    for word in field:
        temp = []
        for w in field:
            if w != word:
                distance = m.similarity(word, w)
                if distance >= 0.5:
                    temp.append({w[:-5]: distance})
        dic_w[word[:-5]] = temp
    with open('results_dist.json', 'w', encoding='utf-8') as f:
        json.dump(dic_w, f, ensure_ascii=False, indent=4)


def open_json():
    with open('results_dist.json', 'r', encoding='utf-8') as f:
        dic_w = json.load(f)
    return dic_w


def create_graph(dic):
    G = nx.Graph()
    for nod in dic:
        if nod not in G.nodes():
            G.add_node(nod)
        for i in dic[nod]:
            for k in i:
                if k not in G.nodes():
                    G.add_node(k)
                if (nod, k) not in G.edges():
                    G.add_edge(nod, k, weight=i[k])
    nx.write_gexf(G, 'graph_semfield.gexf')
    return G


def draw_smth(G):
    pos = nx.spring_layout(G)
    # То же, но добавим ещё подписи к узлам
    nx.draw_networkx_nodes(G, pos, node_color='blue', node_size=10)
    nx.draw_networkx_edges(G, pos, edge_color='green')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='Arial')
    plt.axis('off')
    plt.savefig('matpltlib.png')
    plt.show()


def count_info(G):
    with open('results.txt', 'w', encoding='utf-8') as f:
        f.write('Пять самых центральных слов графа:\n')
        deg = nx.degree_centrality(G)
        c = 0
        for nodeid in sorted(deg, key=deg.get, reverse=False):
            if c == 5:
                break
            f.write('\t{0}\n'.format(nodeid))
            c += 1
        f.write('Коэффициент кластеризации:\n\t{0}\n'.format(nx.average_clustering(G)))
        comp = nx.connected_components(G)
        c = 1
        for sub in comp:
            sub1 = G.subgraph(sub)
            f.write('Компонента связности №{0}\n'.format(c))
            c += 1
            f.write('\tУзлы: ')
            for nod in sub1.nodes():
                f.write('{0}; '.format(nod))
            f.write('\n\tРадиус: {0}\n'.format(nx.radius(sub1)))
            if len(sub1.nodes()) > 1:
                f.write('\tТри самых центральных узла:\n')
                deg = nx.degree_centrality(sub1)
                i = 0
                for nodeid in sorted(deg, key=deg.get, reverse=False):
                    if i == 3:
                        break
                    f.write('\t\t{0}\n'.format(nodeid))
                    i += 1
            else:
                for nod in sub1.nodes():
                    f.write('\tЕдинственный узел:\n\t\t{0}\n'.format(nod))


if __name__ == '__main__':
    #count_dist(open_model()) ##посчитать косинусную близость и сложить в json только те, где она выше 0.5
    graph = create_graph(open_json()) ## создать граф на основе созданного джейсона
    draw_smth(graph) ## отрисовать граф
    count_info(graph) ## посчитать все необходимое