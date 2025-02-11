# load email and password from .env
import os
from dotenv import load_dotenv

from chadd.models.post import Post
from chadd.chadd_scrap import ChaddScraper

load_dotenv()
email = os.getenv('CHADD_USERNAME')
password = os.getenv('CHADD_PASSWORD')


chadd_scraper = ChaddScraper(
    email = email,
    password = password,
    base_url = 'https://healthunlocked.com/'
)

posts = []

def test_chadd_scraper_login():
    chadd_scraper.login()

    assert chadd_scraper.huSessID is not None
    assert chadd_scraper.huBv is not None


def test_get_posts_ids():
    post_ids = chadd_scraper.get_posts_ids(start_date='2020-01', end_date='2020-02', community='adult-adhd')
    assert len(post_ids) > 0
    assert all(isinstance(post_id, int) for post_id in post_ids)


def test_get_post_details():
    post_id = 151579120
    post = chadd_scraper.get_post_details(post_id)
    assert isinstance(post, Post)
    assert post.post_id == post_id

def test_save_cookies():
    chadd_scraper.save_cookies_to_file(filename=f'cookies-test.json')
    assert os.path.exists('cookies-test.json')

def test_load_cookies_from_file():
    scraper = ChaddScraper.from_config(filename=f'cookies-test.json')
    assert scraper.huSessID is not None
    assert scraper.huBv is not None


def test_save_post_to_file():
    post_id = 151579120
    post = chadd_scraper.get_post_details(post_id)
    chadd_scraper.save_post_to_file(post, filename=f"post_{post_id}.json")
    assert os.path.exists(f"post_{post_id}.json")

def test_save_posts_to_file():
    post_ids = chadd_scraper.get_posts_ids(start_date='2020-01', end_date='2020-02', community='adult-adhd')
    for post_id in post_ids:
        post = chadd_scraper.get_post_details(post_id)
        posts.append(post)
    chadd_scraper.save_posts_to_file(posts, filename='posts.json')
    assert os.path.exists('posts.json')

def test_get_user_details():
    username = 'Reformschooldropout'
    user = chadd_scraper.get_user_details(username)
    assert user is not None
    assert user.username == username

def test_save_users_to_file():
    username = 'Reformschooldropout'
    user = chadd_scraper.get_user_details(username)
    users = [user]
    chadd_scraper.save_users_to_file(users, filename='users.json')
    assert os.path.exists('users.json')

def test_get_members():
    members = chadd_scraper.get_members_for_page(1)
    print(members)
    assert len(members) > 0

# runnig the tests
# test_chadd_scraper_login()
# test_save_cookies()
# test_load_cookies_from_file()
# test_get_posts_ids()
# test_get_post_details()
# test_save_post_to_file()
# test_save_posts_to_file()
# test_get_user_details()
# test_save_users_to_file()
# test_get_members()



