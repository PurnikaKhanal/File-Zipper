from huffman_frequency_heap import Node, MinHeap

def buildHuffmanTree(freq):
    heap=MinHeap()#creating an emoty heap
    #pushing every characters as a node into heap
    for byte_val, frequency in freq.items():
        node=Node(byte_val, frequency)
        heap.push(node)
    #if onlt 1 unique character exists
    if heap.size() == 1:
        only=heap.pop()
        root=Node(None, only.frequency, only, None)#fake parent aand current node is left child
        return root
    #keep merging the two smallest nodes until one remains
    while heap.size()>1:
        left = heap.pop()
        right = heap.pop()
        
        merged=Node(None, left.frequency+right.frequency ,left ,right)
        heap.push(merged)

    #last node in the heap is root node
    root=heap.pop()
    return root


def generateCodes(node , prefix="", codes=None):
    if codes is None:
        codes={}

    if node is None:
        return codes
    
    #if node is a leaf node, store code and return
    if node.left is None and node.right is None:
        if prefix=="":
            codes[node.char]="0" #single character
        else:
            codes[node.char] = prefix
        return codes
    
    #go left by adding 0
    generateCodes(node.left, prefix+"0", codes)
    generateCodes(node.right,prefix+"1", codes)

    return codes

def encode(data, codes):
    bitstring=""
    #loop through every byte in data and look up its code
    for byte_val in data:
        bitstring+=codes[byte_val]

    return bitstring
