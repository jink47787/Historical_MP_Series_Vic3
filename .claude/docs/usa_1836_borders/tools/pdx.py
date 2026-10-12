import re
def tokenize(t):
    t=re.sub(r'#[^\n]*','',t)
    return re.findall(r'"[^"]*"|[{}=]|[^\s{}=]+',t)
def parse(t):
    toks=tokenize(t);i=0
    def block():
        nonlocal i
        out=[]
        while i<len(toks):
            tk=toks[i]
            if tk=='}': i+=1; return out
            if i+1<len(toks) and toks[i+1]=='=':
                i+=2
                if toks[i]=='{': i+=1; out.append((tk,block()))
                else: out.append((tk,toks[i])); i+=1
            elif tk=='{': i+=1; out.append((None,block()))
            else: out.append((None,tk)); i+=1
        return out
    return block()
def get(b,k): return [v for kk,v in b if kk==k]
