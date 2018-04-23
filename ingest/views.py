from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import MinimalImgMetadata
from .forms import MinimalImagingMetadataForm
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('..')
    else:
        form = SignUpForm()
    return render(request, 'ingest/signup.html', {'form': form})


class IndexView(generic.ListView):
    template_name = 'ingest/index.html'
    context_object_name = 'latest_metadata_list'

    def get_queryset(self):
        """Return the last five published metadata."""
        return MinimalImgMetadata.objects.order_by('-organization_name')[:5]


class DetailView(generic.DetailView):
    model = MinimalImgMetadata
    template_name = 'ingest/detail.html'
    context_object_name = 'metadata'


def post_new(request):
    if request.method == "POST":
        form = MinimalImagingMetadataForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('..', pk=post.pk)
    else:
        form = MinimalImagingMetadataForm()
    return render(request, 'ingest/post_edit.html', {'form': form})
