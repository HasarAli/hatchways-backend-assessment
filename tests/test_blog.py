import pytest
from blog_api import blog


def test_get_posts_with_no_tags(client):
    response = client.get("/api/posts")
    assert b"error" in response.data
    assert b"Tags" in response.data
    assert response.status_code == 400

def test_get_posts_with_one_tag(client):
    response = client.get("/api/posts?tags=tech")
    assert b"posts" in response.data
    assert response.status_code == 200

def test_get_posts_with_many_tags(client):
    response = client.get("/api/posts?tags=tech,history")
    assert b"posts" in response.data
    assert response.status_code == 200

def test_get_posts_with_invalid_sort_by(client):
    response = client.get("/api/posts?tags=tech&sortBy=author")
    assert b"error" in response.data
    assert b"sortBy" in response.data
    assert response.status_code == 400

def test_get_posts_with_valid_sort_by(client):
    response = client.get("/api/posts?tags=tech&sortBy=id")
    assert b"posts" in response.data
    assert response.status_code == 200

def test_get_posts_with_invalid_direction(client):
    response = client.get("/api/posts?tags=tech&direction=l2r")
    assert b"error" in response.data
    assert b"direction" in response.data
    assert response.status_code == 400

def test_get_posts_with_valid_direction(client):
    response = client.get("/api/posts?tags=tech&sdirection=asc")
    assert b"posts" in response.data
    assert response.status_code == 200


# made it a fixture for potential future uses
@pytest.fixture
def mock_api(monkeypatch):
    def mock_get_posts_with_tag(tag, _=None):
        return [{"id":1, "likes": 1, "popularity":1, "reads":1, "tags":[tag]}]
    monkeypatch.setattr(blog, "get_posts_with_tag", mock_get_posts_with_tag)

def test_combine_posts(mock_api):
    existing_posts_dict = {}
    new_posts_list = blog.get_posts_with_tag("health") # id = 1
    blog.combine_posts(new_posts_list, existing_posts_dict)
    new_posts_list = blog.get_posts_with_tag("tech") # id = 1
    blog.combine_posts(new_posts_list, existing_posts_dict)

    assert len(existing_posts_dict) == 1


def test_post_sorting():
    posts = [
        {"id":1, "reads":1, "likes":1, "popularity":1}, 
        {"id":2, "reads":2, "likes":2, "popularity":2}
    ]
    sorted_posts = blog.sort_posts(posts, "id", "asc")
    assert sorted_posts[0]['id'] == 1
    
    sorted_posts = blog.sort_posts(posts, "id", "desc")
    assert sorted_posts[0]['id'] == 2
    
    sorted_posts = blog.sort_posts(posts, "likes", "desc")
    assert sorted_posts[0]['likes'] == 2
