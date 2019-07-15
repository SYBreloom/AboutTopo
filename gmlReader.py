def extract_switches(file):
    file = open(unicode(file, 'utf-8'), "r")
    switches = []
    links = []
    for line in file:
        # find switch
        if line.startswith("    id "):
            token = line.split("\n")
            token = token[0].split(" ")
            line = line[7:]
            if not line.startswith("\""):
                token = line.split("\n")
                switches.append(int(token[0])+1)
        # find link 从1开始计数
        if line.startswith("    source"):
            token = line.split("\n")
            token = token[0].split(" ")
            sw1 = int(token[-1])+1
        if line.startswith("    target"):
            token = line.split("\n")
            token = token[0].split(" ")
            sw2 = int(token[-1])+1
            links.append((sw1, sw2))

    for s in switches:
        pass
        # self.addLink("h%s" %s, "s%s" %s, 0)

    for dpid1, dpid2 in links:
        pass
        # self.addLink(node1="s%s" % dpid1, node2="s%s" % dpid2)
    return links, switches