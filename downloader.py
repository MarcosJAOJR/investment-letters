import os
import time
from crawlers.dynamo import Dynamo
from crawlers.berkshirehathaway import Berkshirehathaway
import requests

def save_letter(pdf, filename, dest_dir):
    path = os.path.join(dest_dir, filename)
    with open(path, 'wb') as fp:
        fp.write(pdf)


def get_letter(link):
    resp = requests.get(link)
    return resp.content


def download_many(letters):
    for letter in letters:
        print("Downloading {} ...".format(letter[0]))
        pdf = get_letter(letter[1])
        save_letter(pdf, '{}.pdf'.format(letter[0]), letter[2])
    return len(letters)

def main():
    t0 = time.time()

    pt = Dynamo("pt")
    en = Dynamo("en")
    bh = Berkshirehathaway()

    letters = pt.crawl()
    letters.extend(en.crawl())
    letters.extend(bh.crawl())

    count = download_many(letters)

    elapsed = time.time() - t0
    msg = '\n{} letters downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == "__main__":
    main()
