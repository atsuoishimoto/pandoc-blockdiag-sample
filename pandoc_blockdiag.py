import sys, json, tempfile, os, tempfile, subprocess

def walk(tree):
    nodes = [tree]
    while nodes:
        node = nodes.pop(0)
        if isinstance(node, list):
            nodes.extend(node)
        elif isinstance(node, dict):
            ret = yield node
            if ret:
                nodes.extend(ret.values())

def find_codeblock(tree):
    w = walk(tree)
    node = w.next()
    while True:
        if u'CodeBlock' in node:
            yield node
            node = None
        node = w.send(node)


blocktype = "blockdiag"
def find_blockdiagblock(tree):
    for b in find_codeblock(tree):
        meta = b['CodeBlock'][0]
        name, args, kwargs = meta
        if blocktype in args:
            yield (b, name, args, kwargs, b['CodeBlock'][1])

IMAGE_DIR = "blockdiag_images"
def run_blockdiag(tree):
    if not os.path.isdir(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)
       
    for b in find_blockdiagblock(tree):
        block, name, args, kwargs, src = b
        with tempfile.NamedTemporaryFile(delete=False) as srcfile:
            srcname = srcfile.name
            srcfile.write(src.encode("utf-8"))

        f = tempfile.NamedTemporaryFile(delete=True, dir=IMAGE_DIR)
        imgfile = f.name+".png"
        f.close()
        
        try:
            cmd = "blockdiag -a -o {imgfile} {src}".format(
                    imgfile=imgfile, src=srcname)
            subprocess.call(cmd, shell=True)
        finally:
            os.unlink(srcname)

        block.clear()
        imgurl = os.path.join(IMAGE_DIR, os.path.split(imgfile)[1])
        img = {u'Image':[
            [{u'Str': name}],
            [unicode(imgurl, sys.getfilesystemencoding()), u'']]}
        block[u'Para'] = [img]
        
def main():
    src = json.load(sys.stdin)
    run_blockdiag(src)
    json.dump(src, sys.stdout)

if __name__ == '__main__':
    main()
