# views.py
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Service, Booking, Profile, Review, ServiceItem
from .forms import BookingForm,  ServiceForm, RegistrationForm ,ProfileForm, ServiceItemForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import UpdateUsernameForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import UpdateUsernameForm, UpdatePasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required

def highest_rated_service_providers():
    #TODO: implement this method
    service_providers = Service.objects.all()
    return service_providers[:3]

def home_view(request):
    featured_service_providers = highest_rated_service_providers()
    print("featured_service_providers:", featured_service_providers)
    return render(request, 'home.html', {'featured_services': featured_service_providers})

def about_view(request):
    return render(request, 'about.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Create a profile instance for the user
            Profile.objects.create(user=user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    service_items = ServiceItem.objects.filter(owner=request.user)
    print("service items:", service_items)
    return render(request, 'profile.html', {'form': form, 'profile': profile, 'service_items': service_items})

@login_required
def update_username_view(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        if new_username:
            if Profile.objects.filter(user__username=new_username).exists():
                return render(request, 'update_username.html', {'error': 'Username already exists'})
            request.user.username = new_username
            request.user.save()
            return redirect('profile')  # Redirect to user's profile page after updating username
        else:
            # Handle invalid form submission
            return render(request, 'update_username.html', {'error': 'Invalid username'})
    else:
        return render(request, 'update_username.html')
@login_required
def update_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for maintaining user's session
            return redirect('profile')  # Redirect to user's profile page after updating password
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'update_password.html', {'form': form})

@login_required
def booking_view(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            service_item = form.cleaned_data['service_item']
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            client_notes = form.cleaned_data['client_notes']

            # Perform any additional validation or processing here
            if check_in_date >= check_out_date:
                form.add_error('check_out_date', 'Check-out date must be later than check-in date')
                return render(request, 'service_detail.html', {'service_provider': service, 'form': form})

            if _check_availability(service, check_in_date, check_out_date):
                # Create a Booking instance
                booking = Booking.objects.create(
                    user=request.user,
                    service_item=service_item,
                    service=service,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    status='pending',
                    client_notes=client_notes,
                )
                booking.save()

                messages.success(request, 'Booking successful! Check your booking history for details.')
                return redirect('booking_history')
            else:
                messages.error(request, 'Booking failed! The service is fully booked for the selected dates.')
                return render(request, 'service_provider_detail.html', {'service': service, 'form': form,'error':'Booking failed! The service is fully booked for the selected dates.'})
    else:
        form = BookingForm(user=request.user)
    return render(request, 'service_detail.html', {'service': service, 'form': form})

@login_required
def booking_history_view(request):
    bookings = Booking.objects.filter(user=request.user)
    # Get all service_providers that the user has reviewed
    reviewed_services = [service for service in Service.objects.all() if Review.objects.filter(user=request.user, service=service).exists()]
    return render(request, 'booking_history.html', {'bookings': bookings, 'reviewed_services': reviewed_services})

@login_required
def service_provider_dashboard_view(request):
    user = request.user
    services = Service.objects.filter(user=user)
    bookings = Booking.objects.filter(service__in=services)
    context = {'services': services, 'bookings': bookings}
    return render(request, 'service_provider_dashboard.html', context)

@login_required
def update_booking_status_view(request, booking_id):
    print("request.POST:", request.POST)
    if request.method == 'POST':
        print("request.POST:", request.POST)
        new_status = request.POST.get('status')
        notes = request.POST.get('service_provider_notes')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking = Booking.objects.get(id=booking_id)
            booking.status = new_status
            booking.service_provider_notes = notes
            booking.save()
            return redirect('service_provider_dashboard')
    return HttpResponseBadRequest('Invalid form submission')

def _get_service_rating(service):
    reviews = Review.objects.filter(service=service)
    if reviews:
        return sum([review.rating for review in reviews]) / len(reviews), len(reviews)
    return ()

def service_list_view(request):
    services = Service.objects.all()
    services_and_average_rates = {}
    
    for service in services:
        services_and_average_rates[service] = _get_service_rating(service)
    
    return render(request, 'service_list.html', {'services_and_rates': services_and_average_rates})

def _check_availability(service, check_in_date, check_out_date):
    bookings = Booking.objects.filter(service=service)
    occupied_in_date = 0
    for booking in bookings:
        if check_in_date < booking.check_out_date and check_out_date > booking.check_in_date:
            occupied_in_date += 1
    return occupied_in_date < service.available_spaces
def service_detail_view(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    form = BookingForm(user=request.user) if request.user.is_authenticated else None
    return render(request, 'service_detail.html', {'service': service, 'form': form})

def add_service_view(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            service.save()
            messages.success(request, 'Service has been successfully added.')
            return redirect('service_provider_dashboard')
    else:
        form = ServiceForm()
    return render(request, 'add_service.html', {'form': form})

def delete_service_view(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if service.user != request.user:
        messages.error(request, 'You are not authorized to delete this service.')
        return redirect('service_provider_dashboard')
    bookings = Booking.objects.filter(service=service)
    for booking in bookings:
        booking.status = 'declined'
        booking.owner_notes = 'Service has been deleted.'
        booking.save()
    service.delete()
    messages.success(request, 'Service has been successfully deleted.')
    return redirect('owner_dashboard')

def add_review_view(request, service_id):
    if request.method == 'POST':
        if Review.objects.filter(user=request.user, service=service_id).exists():
            messages.error(request, 'You have already reviewed this service provider.')
            return redirect('service_provider_detail', service_id=service_id)
        service = get_object_or_404(Service, id=service_id)
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        if rating and review_text:
            review = Review.objects.create(
                user=request.user,
                service=service,
                rating=rating,
                review=review_text,
            )
            messages.success(request, 'Review has been successfully added.')
            return redirect('service_detail', service_id=service_id)
    return HttpResponseBadRequest('Invalid form submission')

def review_view(request, service_id):
    service_name = get_object_or_404(Service, id=service_id).name
    user_reviews = Review.objects.filter(user=request.user, service=service_id)
    reviews = Review.objects.filter(service=service_id)
    return render(request, 'reviews.html', {'reviews': reviews, 'user_reviews': user_reviews, 'service_name': service_name})

def delete_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if not request.user.has_perm('Website.delete_review') or review.user != request.user:
        messages.error(request, 'You are not authorized to delete this review.')
        return redirect('service_provider_list')
    review.delete()
    messages.success(request, 'Review has been successfully deleted.')
    return redirect('reviews', service_id=review.service.id)

def add_service_item_view(request):
    if request.method == 'POST':
        form = ServiceItemForm(request.POST)
        if form.is_valid():
            service_item = form.save(commit=False)
            service_item.owner = request.user
            identifier = request.POST.get('identifier')
            if ServiceItem.objects.filter(identifier=identifier).exists():
                form.add_error('identifier', 'This identifier is already in use.')
                return render(request, 'add_service_item.html', {'form': form})
            service_item.save()
            messages.success(request, 'Service item has been successfully added.')
            return redirect('profile')
    else:
        form = ServiceItemForm()
    return render(request, 'add_service_item.html', {'form': form})

def service_item_detail_view(request, identifier):
    service_item = get_object_or_404(ServiceItem, identifier=identifier)
    return render(request, 'service_item_detail.html', {'service_item': service_item})

def service_item_delete_view(request, service_item_id):
    service_item = get_object_or_404(ServiceItem, id=service_item_id)
    if service_item.owner != request.user:
        messages.error(request, 'You are not authorized to delete this service item.')
        return redirect('profile')
    service_item_bookings = Booking.objects.filter(service_item=service_item)
    for booking in service_item_bookings:
        booking.status = 'declined'
        booking.client_notes = 'Service Item has been deleted.'
        booking.save()
    service_item.delete()
    messages.success(request, 'Service item has been successfully deleted.')
    return redirect('profile')

def service_item_update_view(request, identifier):
    service_item = get_object_or_404(ServiceItem, identifier=identifier)
    if request.method == 'POST':
        form = ServiceItemForm(request.POST, instance=service_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service item has been successfully updated.')
            return redirect('service_item_detail', identifier=service_item.identifier)
    else:
        form = ServiceItemForm(instance=service_item)
    return render(request, 'dog_update.html', {'form': form})