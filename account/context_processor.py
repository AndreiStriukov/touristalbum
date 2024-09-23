from .forms import LoginUserForm


def get_context_data(request):
    context = {
        'login': LoginUserForm()
    }
    return context
