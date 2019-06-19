from datetime import timedelta

from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _
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
    """ the public main page """
    return render(request, "index.html")


def control_panel(request):
    """ site for publishing new messages """
    if not request.user.is_superuser:
        return HttpResponseForbidden(_("Admin login required"))
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


def control_messages(request, filter, category):
    """ control panel - list messages """
    if not request.user.is_superuser:
        return HttpResponseForbidden(_("Admin login required"))
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

    paginator = Paginator(messages, 100)  # 100 messages per page
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


def categories(request):
    """ control panel - edit categories """
    if not request.user.is_superuser:
        return HttpResponseForbidden(_("Admin login required"))
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


def new_category(request):
    """ control panel - add new category """
    if not request.user.is_superuser:
        return HttpResponseForbidden(_("Admin login required"))
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("tiedotteet:categories")


def tags(request):
    """ control panel - edit tags """
    if not request.user.is_superuser:
        return HttpResponseForbidden(_("Admin login required"))
    tags = Tag.objects.all()
    form = TagForm()
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tiedotteet:tags")
    return render(request, "control/tags.html", {"tags": tags, "form": form})


def delete_tag(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden(_("Admin login required"))
    if request.method == "POST":
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
    return redirect("tiedotteet:tags")


def email(request):
    """ email template """
    if not request.user.is_superuser:
        return HttpResponseForbidden(_("Admin login required"))
    visible_messages = Message.visible_objects.order_by("end_date")
    categories = (
        Category.objects.filter(messages__in=visible_messages)
        .distinct()
        .order_by("order")
    )
    return render(request, "email.html", {"categories": categories})


def toc(request):
    """ toc """
    visible_messages = Message.visible_objects.order_by("end_date")
    categories = (
        Category.objects.filter(messages__in=visible_messages)
        .distinct()
        .order_by("order")
    )
    return render(request, "toc.html", {"categories": categories})


def delete_message(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden(_("Admin login required"))
    if request.method == "POST":
        message = get_object_or_404(Message, pk=pk)
        message.delete()

    return redirect("tiedotteet:control_messages", filter="all", category="all")


def hide_message(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden(_("Admin login required"))
    if request.method == "POST":
        message = get_object_or_404(Message, pk=pk)
        if message.visible:
            message.visible = False
        else:
            message.visible = True
        message.save()
    return redirect("tiedotteet:control_messages", filter="all", category="all")


def edit_message(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden(_("Admin login required"))
    form = EditForm(instance=get_object_or_404(Message, pk=pk))
    messages = {}
    if request.method == "POST":
        form = EditForm(request.POST, instance=get_object_or_404(Message, pk=pk))
        if form.is_valid():
            form.save()
            messages["success"] = _("Bulletin updated")

    return render(request, "control/editor.html", {"form": form, "messages": messages})


def control_panel_email(request):
    """ control panel - send email page for sending emails and editing mail configurations """
    if not request.user.is_superuser:
        return HttpResponseForbidden(_("Admin login required"))
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


def send_email(request):
    """ send infro letter via email """
    if not request.user.is_superuser:
        return HttpResponseForbidden(_("Admin login required"))
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
        return HttpResponseForbidden(_("Admin login required"))
