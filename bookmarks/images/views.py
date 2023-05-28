from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ImageCreateForm
from .models import Image
from actions.utils import create_action
import redis
from django.conf import settings

from account.models import Profile

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class ImageCreationView(View, LoginRequiredMixin):
    def get(self, request):
        form = ImageCreateForm(data=request.GET)
        return render(request, 'images/image/create.html', {'section': 'images', 'form': form})

    def post(self, request):
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'bookmarked image', new_image)
            messages.success(request, 'Image added successfully')
            # redirect to new created image detail view
            return redirect(new_image.get_absolute_url())


class ImageDetailView(View):
    def get(self, request, id, slug):
        image = get_object_or_404(Image, id=id, slug=slug)
        users = Profile.objects.filter(is_active=True)

        """
        Counting total number of viewed images using Redis
        r.incr - a command which increments the value of given key by 1. 
        If the key does not exist, the (incr) creates it and save it in database.
        the incr() method returns the final value of key after performing operation
        """

        total_views = r.incr(f'image:{image.id}:views')

        # increment image ranking by 1
        r.zincrby('image_ranking', 1, image.id)
        return render(request, 'images/image/detail.html',
                      {'section': 'images', 'image': image, 'total_views': total_views, 'users': users})


class ImageListView(View, LoginRequiredMixin):
    def get(self, request):
        images = Image.objects.all()
        paginator = Paginator(images, 8)
        page = request.GET.get('page')
        images_only = request.GET.get('images_only')
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            images = paginator.page(1)
        except EmptyPage:
            if images_only:
                # If AJAX request and page out of range
                # return an empty page
                return HttpResponse('')
            # If page out of range return last page of results
            images = paginator.page(paginator.num_pages)
        if images_only:
            return render(request, 'images/image/list_images.html', {'section': 'images', 'images': images})

        return render(request, 'images/image/list.html', {'section': 'images', 'images': images})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


class ImageRankingView(View, LoginRequiredMixin):
    def get(self, request):
        # get image ranking dictionary
        image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
        image_ranking_ids = [int(id) for id in image_ranking]
        # get the most viewed images
        most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
        # sort images according to their id:
        # 1.img - 40
        # 2.img - 20
        # 3.img - 33...
        most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
        for p in most_viewed:
            print(f"id: {p.id}, title: {p.title}\n")
        return render(request, 'images/image/ranking.html', {'section': 'ranking', 'most_viewed': most_viewed})
