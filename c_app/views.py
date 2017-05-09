from django.shortcuts import render
from c_app.api_processor import *
from .forms import SearchForm


def index(request):
    return render(request, 'index.html', {'form': SearchForm()})


def get_user(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['enter_company']
            org_info = get_general_data(user)

            if org_info == 'empty':
                message = 'Found user without any information by parameters "{}"'.format(user)
                return render(request, 'index.html', {'form': form, 'not_found': message})

            elif org_info:
                stat_language, stat_forks = get_statistic(user)
                repo_info, next_page = get_repo_data(user, 1)

                resp_data = {
                    'form': form,
                    'repo_info': repo_info,
                    'next_page': next_page,
                    'user': user,
                    'stat_language': stat_language,
                    'stat_forks': stat_forks
                }
                resp_data.update(org_info)
                return render(request, 'data.html', resp_data)
            else:
                not_found_message = 'Not found any users by parameters "{}"'.format(user)
                return render(request, 'index.html', {'form': form, 'not_found': not_found_message})
    else:
        form = SearchForm()
        return render(request, 'index.html', {'form': form})


def get_next_repo_data(request):
    user = request.GET['user']
    next_url = request.GET['next_page']
    repo_info,  next_page = get_repo_data(user, int(next_url))
    resp_data = {'repo_info': repo_info, 'next_page': next_page, 'user': user}
    return render(request, 'ajax_repo_data.html', resp_data)
