from sh import pstree


def tree_roll():
    for l in str(pstree('-A')).split('\n'):
        row = []
        for c in list(l):
            if c != ' ':
                row.append(1)
            else:
                row.append(0)
        print row

tree_roll()
