import asyncio
import httpx
from flask import Blueprint, request
from blog_api import InvalidAPIUsage

URL = "https://api.hatchways.io/assessment/blog/posts"
VALID_SORT = ["id", "reads", "likes", "popularity"]
VALID_DIR = ["asc", "desc"]

bp = Blueprint('blog', __name__)

@bp.route('/posts')
async def posts():
    tags = request.args.get("tags")
    sort_by = request.args.get("sortBy", "id")
    direction = request.args.get("direction", "asc")
    
    if not tags:
        raise InvalidAPIUsage("Tags parameter is required", 400)
    tags = tags.split(",")

    if sort_by not in VALID_SORT:
        raise InvalidAPIUsage("sortBy paramater is invalid", 400)
    
    if direction not in VALID_DIR:
        raise InvalidAPIUsage("direction parameter is invalid", 400)
    
    posts = await get_posts_with_tags(tags)
    sorted_posts = sort_posts(posts, sort_by, direction)

    return {"posts": sorted_posts}


def sort_posts(posts, sort_by, direction):
    return sorted(posts, key=lambda post: post[sort_by], reverse=direction == "desc")


async def get_posts_with_tag(client, tag):
    response = await client.get(URL, params={"tag": tag})
    posts = response.json()["posts"]
    return posts


def combine_posts(new_posts_list, existing_posts_dict):
    for post in new_posts_list:
        key = post["id"]
        if not existing_posts_dict.get(key):
            existing_posts_dict[key] = post


async def get_posts_with_tag_and_combine(client, tag, all_posts_dict):
    new_posts_list = await get_posts_with_tag(client, tag)
    combine_posts(new_posts_list, all_posts_dict)


async def get_posts_with_tags(tags):
    async with httpx.AsyncClient() as client:
        all_posts = {}
        tasks = [get_posts_with_tag_and_combine(client, tag, all_posts) for tag in tags]
        await asyncio.gather(*tasks, return_exceptions=True)
        return list(all_posts.values())

