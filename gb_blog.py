import requests
import bs4
from urllib.parse import urljoin
import database


class GbBlogParse:
    def __init__(self, start_url, dbase):
        self.db = dbase
        self.start_url = start_url
        self.done_urls = set()
        self.tasks = [self.posts_line_parse(self.start_url)]
        self.done_urls.add(self.start_url)

    def _get_soup(self, url):
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, "lxml")
        return soup

    def run(self):
        for task in self.tasks:
            task()

    def posts_line_parse(self, url):
        def task():
            soup = self._get_soup(url)
            pagination = soup.find("ul", attrs={"class": "gb__pagination"})
            for task_url in [
                urljoin(self.start_url, url.get("href"))
                for url in pagination.find_all("a")
            ]:
                if task_url not in self.done_urls:
                    self.tasks.append(self.posts_line_parse(task_url))
                    self.done_urls.add(task_url)

            posts_wrap = soup.find("div",
                                   attrs={"class": "post-items-wrapper"}
                                   )

            for post_url in {
                urljoin(self.start_url, url.get("href"))
                for url in posts_wrap.find_all("a",
                                               attrs={"class": "post-item__title"})
            }:
                if post_url not in self.done_urls:
                    self.tasks.append(self.post_parse(post_url))
                    self.done_urls.add(post_url)

        return task

    def post_parse(self, url):
        def task():
            soup = self._get_soup(url)
            author_name_tag = soup.find("div", attrs={"itemprop": "author"})
            data = {
                "post_data": {
                    "url": url,
                    "title": soup.find("h1").text,
                },
                "author": {
                    "name": author_name_tag.text,
                    "url": urljoin(self.start_url, author_name_tag.parent.get("href")),
                },
            }
            self.save(data)

        return task

    def save(self, data):
        self.db.create_post(data)


if __name__ == "__main__":
    db = database.Database("sqlite:///gb_blog.db")
    parser = GbBlogParse("https://geekbrains.ru/posts", db)
    parser.run()
