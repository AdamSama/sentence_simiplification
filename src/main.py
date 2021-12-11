## All final work run through here
import parsing
import bert
import handlefile

def main() -> None:
    paragraph = input('please input a paragraph')
    listofsen = handlefile.main(paragraph)
    bagofsen = []
    print(listofsen)
    count = 0

    for each in listofsen:
        newsen = parsing.run(each)
        bagofsen.append(newsen)
    for senlist in bagofsen:
        newlis = bert.main(senlist)
        print(newlis)

if __name__ == '__main__':
    main()