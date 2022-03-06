from datetime import datetime, timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from acceso.models import Usuario
from .models import Wish
from core.forms import WishForm
from django.views import View
from django.contrib import messages
from django.db.models import Q, Count


class IndexView(View):
    def get(self, request):
        return redirect(reverse('wishes:wishes'))


class WishesView(View):
    def get(self, request):
        total_nogranted = Wish.objects.all().filter(Q(granted=1) & Q(
            uploaded_by__id=request.session['usuario']['id']))
        total_granted = Wish.objects.all().exclude(granted=1)
        total_likes = Wish.objects.annotate(cantidad=Count("users_who_like"))
        nolike_wish = Wish.objects.all().exclude(Q(
            uploaded_by__id=request.session['usuario']['id']) | Q(
            users_who_like__id=request.session['usuario']['id']))
        contexto = {
            'wishes_usuario_session': total_nogranted,
            'all_wishes_users': total_granted,
            'total_likes': total_likes,
            'nolikes_wish': nolike_wish,
        }
        return render(request, 'core/index.html', contexto)


class WishesAdd(View):
    def get(self, request):
        return render(request, 'core/form_add.html', {'formModel': WishForm()})

    def post(self, request):
        form = WishForm(request.POST)
        this_Usuario_inline = Usuario.objects.get(
            id=request.session['usuario']['id'])
        if form.is_valid():
            deseo_recibido = form.save(commit=False)
            deseo_recibido.uploaded_by = this_Usuario_inline
            deseo_recibido.save()
            messages.success(request, 'Deseo agregado con exito')
            return redirect(reverse('wishes:wishes'))
        else:
            form = WishForm(request.POST)
            contexto = {
                'formModel': form,
            }
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'core/create.html', contexto)


class WishesEdit(View):
    def get(self, request, pk):
        wish_detail = Wish.objects.get(id=pk)
        if request.session['usuario']['id'] == wish_detail.uploaded_by.id:
            description = Wish.objects.get(id=pk).description
            form = WishForm(instance=wish_detail)
            contexto = {
                'formModel': form,
            }
            return render(request, 'core/edit.html', contexto)

    def post(self, request, pk):
        wish_detail = Wish.objects.get(id=pk)
        form = WishForm(request.POST, instance=wish_detail)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deseo editado correctamente')
            return redirect(reverse('wishes:wishes'))
        else:
            WishForm(request.POST, instance=wish_detail)
            if len(request.POST['item']) < 3:
                messages.error(
                    request, 'Tu deseo debe contener al menos 3 caracteres!')
            if len(request.POST['description']) < 1:
                messages.error(
                    request, 'Debes describir tu deseo!')
            return redirect(f'/wishes/edit/{pk}')


class WishGranted(View):
    def post(self, request, pk):
        print(pk)
        print(request.POST)
        estado = int(request.POST['granted'])
        this_wish = Wish.objects.get(id=pk)
        print(this_wish.updated_at)
        print(datetime.now(timezone.utc))
        if estado == 2:
            this_wish.granted = 2
            this_wish.updated_at = datetime.now(timezone.utc)
            this_wish.save()
            messages.success(request, 'Deseo concedido correctamente')
            return redirect(reverse('wishes:wishes'))
        else:
            messages.error(request, 'Con errores, intenta nuevamente!')
            return redirect(reverse('wishes:wishes'))


class WishLike(View):
    def get(self, request, pk):
        this_Usuario_inline = Usuario.objects.get(
            id=request.session['usuario']['id'])
        this_wish = Wish.objects.get(id=pk)
        this_Usuario_inline.liked_whishes_granted.add(this_wish)
        messages.success(request, 'Te ha gustado este deseo concedido.')
        return redirect(reverse('wishes:wishes'))


class WishDestroy(View):
    def get(self, request, pk):
        deletewish = Wish.objects.get(id=pk)
        deletewish.delete()
        return redirect(reverse('wishes:wishes'))


class WhishStats(View):
    def get(self, request):
        total_granted = Wish.objects.annotate(
            cantidad=Count("granted")).filter(granted=2)
        my_granted = Wish.objects.annotate(
            cantidad=Count("granted")).filter(Q(granted=2) & Q(uploaded_by__id=request.session['usuario']['id']))
        no_granted = Wish.objects.annotate(
            cantidad=Count("granted")).filter(Q(granted=1) & Q(uploaded_by__id=request.session['usuario']['id']))
        contexto = {
            'total_granted': total_granted,
            'my_granted': my_granted,
            'no_granted': no_granted,
        }
        return render(request, 'core/stats.html', contexto)
