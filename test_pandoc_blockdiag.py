import pdb
import pandoc_blockdiag
def test_walk():
    d1 = {u'Str': u'abc'}
    d2 = {u'Str': u'def'}
    d0 = {u'Para':[d1, d2]}
    w = pandoc_blockdiag.walk(d0)
    ret = []
    try:
        node = w.next()
        while True:
            ret.append(node)
            node = w.send(node)
    except StopIteration:
        pass

    assert ret == [d0, d1, d2]

def test_findcodeblock():
    d1 = {u'CodeBlock': [1,2,3]}
    d2 = {u'CodeBlock': [3,4,5]}
    d3 = {u'Para': [6,7,8,9,0,d2]}
    d4 = {u'CodeBlock': [6,7,8]}
    d0 = {u'Para':[d1, d2, d4]}

    ret = list(pandoc_blockdiag.find_codeblock(d0))
    assert ret == [d1, d2, d4]
    
def test_find_blockdiag():
    d = {u'CodeBlock': [
            ['chart1', ['blockdiag'], []],
            """
            A -> B -> C;
            """]}
    for b in pandoc_blockdiag.find_blockdiagblock([d]):
        block, name, args, kwargs, src = b
        assert block is d
        assert name == 'chart1'
        assert args == ['blockdiag']
        assert kwargs == []

if __name__ == '__main__':
    test_walk()