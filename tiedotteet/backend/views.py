from datetime import timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import gettext as _
from tiedotteet.backend.forms import (
    CategoryForm,
    EditForm,
    MailConfigurationForm,
    PublishForm,
    SendEmailForm,
    TagForm,
)
from tiedotteet.backend.models import Category, MailConfiguration, Message, Tag


def index(request):
    """The main public view.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    return render(request, "tiedotteet/index.html")


@staff_member_required(login_url="/login")
def control_panel(request):
    """The main admin view.

    Messages are published from this view.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
        The template is renders a PublishForm and shows latest messages.
    """

    form = PublishForm()
    latest_messages = Message.objects.filter(visible=True).order_by("-pk")[:10]
    if request.method == "POST":
        form = PublishForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("New bulletin added"))
            return redirect("tiedotteet:cp")
    return render(
        request, "control/cp.html", {"form": form, "latest_messages": latest_messages}
    )


@staff_member_required(login_url="/login")
def control_messages(request, filter, category):
    """Admin view - control messages.

    Messages can be edited and deleted in this view.

    Args:
        request: HttpRequest object from Django.
        filter: a string based on which to filter.
        category: message category.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    if filter == "now":
        messages = Message.objects.filter(end_date__gte=timezone.now()).order_by("-pk")
        filter_label = _("Now")
    elif filter == "new":
        messages = Message.objects.filter(
            start_date__gte=timezone.now() - timedelta(days=7)
        ).order_by("-pk")
        filter_label = _("New")
    elif filter == "upcoming":
        messages = Message.objects.filter(start_date__gte=timezone.now()).order_by(
            "-pk"
        )
        filter_label = _("Upcoming")
    elif filter == "old":
        messages = Message.objects.filter(end_date__lt=timezone.now()).order_by("-pk")
        filter_label = _("Old")
    else:
        messages = Message.objects.all().order_by("-pk")
        filter_label = _("All")

    categories = (
        Category.objects.filter(messages__in=messages).distinct().order_by("order")
    )

    for c in categories:
        if str(c.pk) == category:
            messages = messages.filter(category=c)

    paginator = Paginator(messages, 100)
    page = request.GET.get("page")
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    queries_without_page = request.GET.copy()
    if "page" in queries_without_page.keys():
        del queries_without_page["page"]

    return render(
        request,
        "control/messages.html",
        {
            "messages": messages,
            "categories": categories,
            "filter": filter,
            "filter_label": filter_label,
        },
    )


@staff_member_required(login_url="/login")
def categories(request):
    """Admin view - categories.

    Message categories are controlled with this view. Their name, display order
    and display type (public or logged in users) can be tweaked.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    categories = Category.objects.all()
    cforms = [CategoryForm(prefix=str(x), instance=x) for x in categories]
    nform = CategoryForm()
    if request.method == "POST":
        cforms = [
            CategoryForm(request.POST, prefix=str(x), instance=x) for x in categories
        ]
        if all([cf.is_valid() for cf in cforms]):
            for cf in cforms:
                category = cf.save()
                if category.title == "":
                    category.delete()
            return redirect("tiedotteet:categories")
    return render(
        request,
        "control/categories.html",
        {"categories": categories, "cforms": cforms, "nform": nform},
    )


@staff_member_required(login_url="/login")
def new_category(request):
    """Admin view - add categories.

    New categories are added with via this view.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django HttpResponseRedirect  object that redirects
        back to the main categories page.
    """

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("tiedotteet:categories")


@staff_member_required(login_url="/login")
def tags(request):
    """Admin view - tags.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template or an
        HttpResponseRedirect to the main tags page on valid TagForm submission.
    """

    tags = Tag.objects.all()
    form = TagForm()
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tiedotteet:tags")
    return render(request, "control/tags.html", {"tags": tags, "form": form})


@staff_member_required(login_url="/login")
def delete_tag(request, pk):
    """Admin view - delete tags.

    Tags can be deleted with this view.

    Args:
        request: HttpRequest object from Django.
        pk: Primary key for a Tag object

    Returns:
        A Django HttpResponseRedirect object that redirects
        back to the main tags page.
    """

    if request.method == "POST":
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
    return redirect("tiedotteet:tags")


@staff_member_required(login_url="/login")
def email(request):
    """Admin view - email.

    Not used currently.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    visible_messages = Message.visible_objects.order_by("end_date")
    categories = (
        Category.objects.filter(messages__in=visible_messages)
        .distinct()
        .order_by("order")
    )
    return render(request, "email.html", {"categories": categories})


def toc(request):
    """Public view - table of contents

    Display a list of all messages.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    visible_messages = Message.visible_objects.order_by("end_date")
    categories = (
        Category.objects.filter(messages__in=visible_messages)
        .distinct()
        .order_by("order")
    )
    return render(request, "toc.html", {"categories": categories})


@staff_member_required(login_url="/login")
def delete_message(request, pk):
    """Admin view - delete a message.

    Args:
        request: HttpRequest object from Django.
        pk: Primary key for a Message object.

    Returns:
        A Django HttpResponseRedirect object that redirects
        back to messages control page.
    """

    if request.method == "POST":
        message = get_object_or_404(Message, pk=pk)
        message.delete()

    return redirect("tiedotteet:control_messages", filter="all", category="all")


@staff_member_required(login_url="/login")
def hide_message(request, pk):
    """Admin view - hide a message.

    Args:
        request: HttpRequest object from Django.
        pk: Primary key for a Message object.

    Returns:
        A Django HttpResponseRedirect object that redirects
        back to messages control page.
    """

    if request.method == "POST":
        message = get_object_or_404(Message, pk=pk)
        if message.visible:
            message.visible = False
        else:
            message.visible = True
        message.save()
    return redirect("tiedotteet:control_messages", filter="all", category="all")


@staff_member_required(login_url="/login")
def edit_message(request, pk):
    """Admin view - edit a message.

    Args:
        request: HttpRequest object from Django.
        pk: Primary key for a Message object.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    form = EditForm(instance=get_object_or_404(Message, pk=pk))
    messages = {}
    if request.method == "POST":
        form = EditForm(request.POST, instance=get_object_or_404(Message, pk=pk))
        if form.is_valid():
            form.save()
            messages["success"] = _("Bulletin updated")

    return render(request, "control/editor.html", {"form": form, "messages": messages})


@staff_member_required(login_url="/login")
def control_panel_email(request):
    """Admin view - email.

    Not used currently.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    config, created = MailConfiguration.objects.get_or_create(pk=1)
    config_form = MailConfigurationForm(instance=config)
    send_form = SendEmailForm()
    if request.method == "POST":
        config_form = MailConfigurationForm(request.POST, instance=config)
        if config_form.is_valid():
            config_form.save()
            return redirect(control_panel_email)
    return render(
        request,
        "control/email.html",
        {"config": config, "config_form": config_form, "send_form": send_form},
    )


@staff_member_required(login_url="/login")
def send_email(request):
    """Admin view - email.

    Not used currently.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    if request.method == "POST":
        form = SendEmailForm(request.POST)
        if form.is_valid():
            # create html body
            visible_messages = Message.visible_objects.order_by("end_date")
            categories = (
                Category.objects.filter(messages__in=visible_messages)
                .distinct()
                .order_by("order")
            )
            config = MailConfiguration.objects.get(pk=1)
            template = get_template("email.html")
            context = Context({"categories": categories})
            text_content = strip_tags(template.render(context))
            html_content = template.render(context)
            # backend configuration
            backend = EmailBackend(
                host=config.host,
                port=config.port,
                username=config.username,
                password=config.password,
                use_tls=config.use_tls,
                fail_silently=config.fail_silently,
            )
            # create the email
            email = EmailMultiAlternatives(
                subject=form.cleaned_data["subject"],
                body=text_content,
                from_email=config.username,
                to=form.cleaned_data["to"].split(","),
                connection=backend,
            )
            # attach html content
            email.attach_alternative(html_content, "text/html")
            # send
            try:
                email.send()
                return JsonResponse({"success": True})
            except Exception as e:
                return JsonResponse(
                    {"success": False, "errors": {"mail": "failed to send"}}
                )
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
