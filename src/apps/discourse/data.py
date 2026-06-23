from django.conf import settings
import requests


def get_discourse_json(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return {}


def get_discourse_index_data():
    categories_url = settings.DISCOURSE_UPSTREAM + '/categories.json'
    categories_data = get_discourse_json(categories_url)
    categories = categories_data.get('category_list', {}).get('categories', [])

    latest_url = settings.DISCOURSE_UPSTREAM + '/latest.json'
    latest_data = get_discourse_json(latest_url)
    latest = latest_data.get('topic_list', {}).get('topics', [])

    topics = []
    for topic in latest[:10]:
        topic_category = None

        for category in categories:
            subcategories = category.get('subcategory_ids', [])
            if category['id'] == topic['category_id']:
                topic_category = category
            elif topic['category_id'] in subcategories:
                topic_category = category

        if not topic_category:
            continue

        topic['category_name'] = topic_category['name']
        topic['category_slug'] = topic_category['slug']

        topics.append(topic)

    return topics
