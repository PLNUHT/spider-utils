import spider_utils

def main():
    v = spider_utils.submit({
        "lang": "zh",
        "src": "test",
        "cat": "cat",
        "subcat": "subcat",
        "meta": {},
        "body": "<p>asd<a href=\"qwe\">link content</a>bbbbb<icon>cq</icon></p><img src=\"img src\" style=\"display: block;\"><p>qwert</p><li>qwer</li><p>qqqqqq<b>bold</b>asdqqq<!-- comment here --> </p>"
    })
    print(v)
    v["_"].print()

if __name__ == "__main__":
    main()