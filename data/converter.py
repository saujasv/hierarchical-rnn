lines = open("no_agreement/"+'train.txt' ,).\
        read().strip().split('\n')
inp = []
out = []
for line in lines :
    sent = line.split("\t")
    inp.append(sent[0])
    out.append(sent[1])
f = open("no_agreement/"+'train.txt' ,"w")
for index in range(len(inp)):
    f.write(out[index] + "\t" + inp[index] + "\n")
