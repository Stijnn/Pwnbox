def main():
    [print(l.replace('\n','')) for l in open('./banner.txt', 'r').readlines()]
    pass


if __name__ == "__main__":
    main()