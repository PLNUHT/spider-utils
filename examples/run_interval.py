import spider_utils

class MySpider:
    def __init__(self):
        self.x = 0

    def func(self):
        self.x += 1
        print("counter: %d" % self.x)
        v = 1 / (self.x - 3)
    
    def shutdown(self):
        print("Stoped ! [%d]" % self.x)
        print("Save data here")


def main():
    spider = MySpider()

    print("Start: run spider.func every 5 seconds")
    spider_utils.run(spider.func, 5, spider.shutdown)

if __name__ == "__main__":
    main()