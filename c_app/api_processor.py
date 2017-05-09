import requests
import json

GITHUB_API = 'https://api.github.com/users/{}?client_id=714686fb18e5d49b6a64&client_secret=5b89bdff692e07f32e4ea4e7799e8b047b3c27a4&{}'
GITHUB_REPOS_API = 'https://api.github.com/users/{}/repos?client_id=714686fb18e5d49b6a64&client_secret=5b89bdff692e07f32e4ea4e7799e8b047b3c27a4&page={}&per_page=10'
GITHUB_LANGUAGES_API = 'https://api.github.com/users/{}/repos?client_id=714686fb18e5d49b6a64&client_secret=5b89bdff692e07f32e4ea4e7799e8b047b3c27a4&page={}&per_page=100'


def get_general_data(user):
    api_data = requests.get(GITHUB_API.format(user, '')).json()

    if api_data.get('message') == 'Not Found':
        return

    if not api_data['name']:
        return 'empty'

    user_email = api_data['email'] if api_data['email'] else '-'

    return {
        'nicname': api_data['name'],
        'email': user_email,
        'avatar': api_data['avatar_url'],
        'repos_count': api_data['public_repos']
    }


def get_repo_data(user, page):
    api_data = requests.get(GITHUB_REPOS_API.format(user, page)).json()
    print (GITHUB_REPOS_API.format(user, page))
    repo_output_data = []
    for r in api_data:
        repo_output_data.append({
            'repo_name': r['name'],
            'repo_url': r['html_url'],
            'repo_forks': r['forks'],
            'language': r['language'],
            'repo_issues_count': r['open_issues_count']
        })

    next_page = page + 1 if len(api_data) == 10 else None

    return repo_output_data, next_page


def get_statistic(user):

    all_languages_list = []
    forks_statistic = [['Repositiry name', 'count of forks']]

    page = 1
    while True:
        api_data = requests.get(GITHUB_LANGUAGES_API.format(user, page)).json()
        if not api_data:
            break
        for r in api_data:
            if r['language'] is None:
                l = 'Others'
            else:
                l = r['language']
            all_languages_list.append(l)
        for r in api_data:
            forks_statistic.append(
                [r['name'], r['forks']]
            )

        page += 1

    u_languages = tuple(set(all_languages_list))
    languages_statistic = [['Language', 'Count']]

    for l in u_languages:
        languages_statistic.append(
            [l, all_languages_list.count(l)]
        )

    return json.dumps(languages_statistic), json.dumps(forks_statistic)
