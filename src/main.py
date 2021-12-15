## All final work run through here
import parsing
import bert
import handlefile
import copy

def main() -> None:
    # paragraph = input('please input a paragraph')
    # listofsen = handlefile.main(paragraph)
    # bagofsen = []
    # print(listofsen)
    # count = 0
    with open('../data/data1/test.txt', 'r') as instream:
        with open('../data/data1/output.txt', 'w') as outstream:
            lines = instream.readlines()
            index = [index for index, line in enumerate(lines) if line == '\n']
            index.insert(0, -1)
            bagofsen = []
            # print(index)
            for i in index:
                
                line = lines[i + 1]
                linetemp = copy.deepcopy(line)
                newsen = parsing.run(linetemp)
                print(newsen)
                bagofsen.append(newsen)
            # print(len(bagofsen), len(index))
            newbag = bert.main(bagofsen)
            print(index)
            for i, sen in enumerate(newbag):
                print(lines[index[i]+1])
                outstream.write(lines[index[i]+1])
                for each in sen:
                    outstream.write(each)
                    outstream.write('\n')
                outstream.write('\n')


if __name__ == '__main__':
    main()