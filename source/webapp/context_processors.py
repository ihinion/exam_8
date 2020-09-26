from webapp.forms import SearchForm

def search_form(request):
    form = SearchForm(request.GET)
    return {'search_form': form}