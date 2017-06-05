import hashlib


def compute_file_md5(file):
    hash_md5 = hashlib.md5()
    for chunk in file.chunks():
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_parents(article, parents_list):
    """
    Return all parents from article
    """
    if article.parent_article:
        parents_list.insert(len(parents_list), article.parent_article)
        get_parents(article.parent_article, parents_list)