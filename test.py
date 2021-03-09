import spider_utils

def main():

    result = {
        "lang": "zh",
        "src": "test",
        "cat": "cat",
        "subcat": "subcat",
        "meta": {},
        "body": "<p>asd<a href=\"qwe\">link content</a>bbbbb<icon>cq</icon></p><img src=\"img src\" style=\"display: block;\"><p>qwert</p><li>qwer</li><p>qqqqqq<b>bold</b>asdqqq<!-- comment here --> </p>"
    }

    v = spider_utils.submit(result)

if __name__ == "__main__":
    main()