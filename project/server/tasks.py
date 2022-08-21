import os
import time
from bs4 import BeautifulSoup

from celery import Celery

from project.server.main.db import DB

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@celery.task(name="update_tags")
def update_tags():
    pass


@celery.task(name="process_bookmarks")
def process_bookmarks(filename):
    processed = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.replace("<p>", "")
            line = line.replace("</DL>", "</DL></DT>")
            if line.lstrip().startswith("<DT><A "):
                line = line.rstrip() + "</DT>\n"
            processed.append(line)
    filetxt = ''.join(processed)
    soup = BeautifulSoup(filetxt, 'html.parser')
    collector = []
    visit_dl(soup.dl, collector)
    DB().add_links(collector)
    print(f"processed {filename}")
    update_tags.delay()
    return True


def visit_dt(dt, collector):
    if dt.name != 'dt':
        raise Exception(f"Unknown node passed as dt: {dl.name}")
    for c in dt.children:
        if c.name == 'dl':
            visit_dl(c, collector)
        elif c.name == 'a':
            if not c.has_attr('href'):
                continue
            href = c['href']
            if len(href.strip()) == 0:
                continue
            l_text = c.string
            if not l_text:
                continue
            collector.append((href, l_text, ""))


def visit_dl(dl, collector):
    if dl.name != 'dl':
        raise Exception(f"Unknown node passed as dl: {dl.name}")
    for n in dl.children:
        if not n.name:
            continue
        elif n.name == 'dt':
            visit_dt(n, collector)
        elif n.name == 'dl':
            visit_dl(dl, collector)
        else:
            continue
