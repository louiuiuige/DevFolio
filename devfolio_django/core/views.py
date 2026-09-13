from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.paginator import Paginator

from .forms import ProjectForm, ProjectImageUploadForm, RegistrationForm
from .models import Category, Project, ProjectImage, Review, User, Technology


def staff_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role not in [User.ROLE_MODERATOR, User.ROLE_ADMIN]:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped


def verify_email(request, token):
    try:
        payload = signing.loads(token)
    except signing.BadSignature:
        messages.error(request, 'Verification link is invalid or expired.')
        return redirect('login')

    user = User.objects.filter(pk=payload.get('user_id')).first()
    if user is None:
        messages.error(request, 'User account could not be found.')
        return redirect('login')

    user.email_verified = True
    user.is_active = True
    user.save(update_fields=['email_verified', 'is_active'])
    messages.success(request, 'Your email has been verified successfully. You can now log in.')
    return redirect('login')


def home(request):
    featured_projects = Project.objects.filter(status=Project.STATUS_APPROVED)[:6]
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'featured_projects': featured_projects,
        'categories': categories,
    })


def project_list(request):
    projects = Project.objects.filter(status=Project.STATUS_APPROVED).select_related('owner', 'category')

    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '')
    technology_slug = request.GET.get('technology', '')
    course = request.GET.get('course', '').strip()
    year = request.GET.get('year', '')

    if query:
        projects = projects.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(description__icontains=query)
            | Q(owner__username__icontains=query)
            | Q(owner__full_name__icontains=query)
            | Q(owner__course__icontains=query)
            | Q(category__name__icontains=query)
            | Q(technologies__name__icontains=query)
        ).distinct()

    if category_slug:
        projects = projects.filter(category__slug=category_slug)

    if technology_slug:
        projects = projects.filter(technologies__slug=technology_slug)

    if course:
        projects = projects.filter(owner__course__icontains=course)

    if year:
        projects = projects.filter(owner__year_level=year)

    projects = projects.distinct()
    paginator = Paginator(projects, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    technologies = Technology.objects.all()
    course_choices = sorted({user.course for user in User.objects.exclude(course='').exclude(course__isnull=True)}, key=str.lower)
    year_choices = list(range(1, 9))

    return render(request, 'projects.html', {
        'projects': page_obj,
        'categories': categories,
        'technologies': technologies,
        'courses': course_choices,
        'year_choices': year_choices,
        'current_query': query,
        'current_category': category_slug,
        'current_technology': technology_slug,
        'current_course': course,
        'current_year': year,
    })


def project_detail(request, slug):
    project = Project.objects.select_related('owner', 'category').prefetch_related('technologies', 'gallery', 'reviews__reviewer').get(slug=slug)

    related_projects = Project.objects.filter(
        status=Project.STATUS_APPROVED,
        category=project.category,
    ).exclude(pk=project.pk)[:4]

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()

        if rating:
            review, created = Review.objects.get_or_create(
                project=project,
                reviewer=request.user,
                defaults={'rating': int(rating), 'comment': comment},
            )
            if not created:
                review.rating = int(rating)
                review.comment = comment
                review.save()
            messages.success(request, 'Your review has been saved.')
        else:
            messages.error(request, 'Please provide a rating before submitting your review.')
        return redirect('project_detail', slug=project.slug)

    return render(request, 'project_detail.html', {
        'project': project,
        'related_projects': related_projects,
        'user_review': project.reviews.filter(reviewer=request.user).first() if request.user.is_authenticated else None,
    })


@login_required(login_url='login')
def dashboard(request):
    my_projects = Project.objects.filter(owner=request.user).order_by('-created_at')
    paginator = Paginator(my_projects, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_reviews = Review.objects.filter(project__owner=request.user).count()
    approved_projects = my_projects.filter(status=Project.STATUS_APPROVED).count()
    return render(request, 'dashboard.html', {
        'my_projects': page_obj,
        'total_reviews': total_reviews,
        'approved_projects': approved_projects,
    })


@login_required(login_url='login')
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.status = Project.STATUS_UNDER_REVIEW
            project.save()
            form.save_m2m()
            messages.success(request, 'Your project has been submitted for review.')
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form, 'mode': 'Create'})


@login_required(login_url='login')
def project_edit(request, slug):
    project = Project.objects.get(slug=slug, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.status = Project.STATUS_UNDER_REVIEW
            updated.save()
            form.save_m2m()
            messages.success(request, 'Project updated and sent back for review.')
            return redirect('dashboard')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form, 'mode': 'Edit', 'project': project})


@login_required(login_url='login')
def project_delete(request, slug):
    project = Project.objects.get(slug=slug, owner=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('dashboard')
    return render(request, 'project_confirm_delete.html', {'project': project})


@login_required(login_url='login')
def project_gallery_upload(request, slug):
    project = Project.objects.get(slug=slug)
    is_allowed = request.user == project.owner or request.user.role in [User.ROLE_MODERATOR, User.ROLE_ADMIN]
    if not is_allowed:
        messages.error(request, 'You are not allowed to upload images for this project.')
        return redirect('project_detail', slug=project.slug)

    if request.method == 'POST':
        form = ProjectImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = ProjectImage.objects.create(
                project=project,
                image=form.cleaned_data['image'],
                caption=form.cleaned_data.get('caption', ''),
            )
            messages.success(request, f'Image "{image.caption or image.image.name}" uploaded successfully.')
            return redirect('project_detail', slug=project.slug)
    else:
        form = ProjectImageUploadForm()

    return render(request, 'project_gallery_upload.html', {'project': project, 'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.is_active = False
            user.save()
            verification_link = user.generate_verification_token(request)
            send_mail(
                'Verify your DevFolio account',
                f'Click the link below to verify your email:\n\n{verification_link}\n\nIf you did not create this account, ignore this email.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Registration successful. Please check your email to verify your account.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.email_verified:
                messages.error(request, 'Please verify your email before logging in.')
                return render(request, 'login.html')
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


@login_required(login_url='login')
@require_POST
def custom_logout(request):
    logout(request)
    return redirect('home')


@staff_required
def moderation_queue(request):
    pending_projects = Project.objects.filter(status=Project.STATUS_UNDER_REVIEW).select_related('owner', 'category')
    return render(request, 'moderation_queue.html', {'pending_projects': pending_projects})


@staff_required
@require_POST
def project_approve(request, slug):
    project = Project.objects.get(slug=slug)
    project.status = Project.STATUS_APPROVED
    project.save()
    messages.success(request, f'Project "{project.title}" has been approved.')
    return redirect('moderation_queue')


@staff_required
@require_POST
def project_reject(request, slug):
    project = Project.objects.get(slug=slug)
    project.status = Project.STATUS_REJECTED
    project.save()
    messages.success(request, f'Project "{project.title}" has been rejected.')
    return redirect('moderation_queue')


@login_required(login_url='login')
def admin_dashboard(request):
    if request.user.role != User.ROLE_ADMIN:
        messages.error(request, 'Admin access required.')
        return redirect('dashboard')

    stats = {
        'total_users': User.objects.count(),
        'students': User.objects.filter(role=User.ROLE_STUDENT).count(),
        'moderators': User.objects.filter(role=User.ROLE_MODERATOR).count(),
        'projects': Project.objects.count(),
        'approved': Project.objects.filter(status=Project.STATUS_APPROVED).count(),
        'pending': Project.objects.filter(status=Project.STATUS_UNDER_REVIEW).count(),
        'rejected': Project.objects.filter(status=Project.STATUS_REJECTED).count(),
    }
    recent_projects = Project.objects.select_related('owner', 'category').order_by('-created_at')[:8]
    return render(request, 'admin_dashboard.html', {'stats': stats, 'recent_projects': recent_projects})


@login_required(login_url='login')
def admin_users(request):
    if request.user.role != User.ROLE_ADMIN:
        messages.error(request, 'Admin access required.')
        return redirect('dashboard')

    users = User.objects.order_by('-date_joined')
    return render(request, 'admin_users.html', {'users': users})
