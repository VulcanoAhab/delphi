from django.shortcuts import render
# Create your views here.

def sayError(request):
    '''
    '''
    return render(context, 'sayError.html', {})
