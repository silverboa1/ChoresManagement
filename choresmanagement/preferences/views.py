from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import (
    UserPreference,
    UserCategoryPreference,
    UserCategoryExperience,
    UserPhysicalLimitation,
    PhysicalLimitation
)
from .forms import (
    UserPreferenceForm,
    UserCategoryPreferenceFormSet,
    UserCategoryExperienceFormSet,
    UserPhysicalLimitationFormSet,
    PhysicalLimitationForm
)

@login_required
def edit_preferences(request):
    user = request.user

    preference, created = UserPreference.objects.get_or_create(user=user)

    prefixes = {
        'category_pref': 'usercategorypreference_set',
        'experience': 'usercategoryexperience_set',
        'limitation': 'userphysicallimitation_set',
    }

    if request.method == 'POST':
        pref_form = UserPreferenceForm(
request.POST
, instance=preference)

        category_pref_formset = UserCategoryPreferenceFormSet(
            
request.POST
, instance=user, prefix=prefixes['category_pref']
        )
        experience_formset = UserCategoryExperienceFormSet(
            
request.POST
, instance=user, prefix=prefixes['experience']
        )
        physical_lim_formset = UserPhysicalLimitationFormSet(
            
request.POST
, instance=user, prefix=prefixes['limitation']
        )

        if (pref_form.is_valid()
            and category_pref_formset.is_valid()
            and experience_formset.is_valid()
            and physical_lim_formset.is_valid()):

            pref_form.save()
            category_pref_formset.save()
            experience_formset.save()
            physical_lim_formset.save()

            return redirect('preferences:edit')

    else:
        pref_form = UserPreferenceForm(instance=preference)
        category_pref_formset = UserCategoryPreferenceFormSet(
            instance=user, prefix=prefixes['category_pref']
        )
        experience_formset = UserCategoryExperienceFormSet(
            instance=user, prefix=prefixes['experience']
        )
        physical_lim_formset = UserPhysicalLimitationFormSet(
            instance=user, prefix=prefixes['limitation']
        )

    context = {
        'pref_form': pref_form,
        'category_pref_formset': category_pref_formset,
        'experience_formset': experience_formset,
        'physical_lim_formset': physical_lim_formset,
    }

    return render(request, 'preferences/edit_preferences.html', context)

# Список обмежень
class PhysicalLimitationListView(ListView):
    model = PhysicalLimitation
    template_name = 'preferences/physicallimitation_list.html'
    context_object_name = 'limitations'

# Деталі обмеження
class PhysicalLimitationDetailView(DetailView):
    model = PhysicalLimitation
    template_name = 'preferences/physicallimitation_detail.html'
    context_object_name = 'limitation'

# Створення обмеження
class PhysicalLimitationCreateView(CreateView):
    model = PhysicalLimitation
    form_class = PhysicalLimitationForm
    template_name = 'preferences/physicallimitation_form.html'
    success_url = reverse_lazy('preferences:limitation_list')

# Редагування обмеження
class PhysicalLimitationUpdateView(UpdateView):
    model = PhysicalLimitation
    form_class = PhysicalLimitationForm
    template_name = 'preferences/physicallimitation_form.html'
    success_url = reverse_lazy('preferences:limitation_list')

# Видалення обмеження
class PhysicalLimitationDeleteView(DeleteView):
    model = PhysicalLimitation
    template_name = 'preferences/physicallimitation_confirm_delete.html'
    success_url = reverse_lazy('preferences:limitation_list') 