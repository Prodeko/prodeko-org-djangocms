import csv as csv
import math
import os
import random
import string
from datetime import datetime, timedelta
from io import StringIO, TextIOWrapper
from itertools import chain
from shutil import make_archive
from wsgiref.util import FileWrapper

import unicodecsv as unicodecsv
from django.contrib import messages
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.cache import cache
from django.db.models import F, Q, Value
from django.http import (
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
    StreamingHttpResponse,
)
from django.shortcuts import (
    HttpResponse,
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
    render,
)
from django.template.loader import render_to_string
from django.urls import reverse

from alumnirekisteri.auth2.forms import LoginForm, PasswordChangeForm
from alumnirekisteri.rekisteri.forms import *
from alumnirekisteri.rekisteri.models import *
from prodekoorg import settings as project_settings


def sortByEndDate(x):
    return -(
        (x.end_year if x.end_year else 0) * 12
        + (x.end_month if hasattr(x, "end_month") and x.end_month else 0)
    )


def sortByYear(x):
    return -(x.year if x.year else 0)


def getAdminSearchQueryset(
    first_name, last_name, admin_note, member_until_type, member_until, user_type
):
    user_list = User.objects.all()

    if last_name:
        user_list = user_list.filter(
            Q(last_name__icontains=last_name)
            | Q(person__original_last_name__icontains=last_name)
        )
    if first_name:
        user_list = user_list.filter(
            Q(first_name__icontains=first_name)
            | Q(person__nickname__icontains=first_name)
            | Q(person__preferred_name__icontains=first_name)
        )

    if admin_note:
        user_list = user_list.filter(person__admin_note__icontains=admin_note)

    if member_until:
        if member_until_type == "after":
            user_list = user_list.filter(person__member_until__gt=member_until)
        else:
            user_list = user_list.filter(person__member_until__lt=member_until)

    if user_type:
        if user_type == "alumni":
            user_list = user_list.filter(person__is_alumni=True)
        if user_type == "member":
            user_list = user_list.filter(person__is_alumni=False)

    return user_list


def delete_user(user):
    if user.person:
        for x in user.person.phones.all():
            """ x.audit_log.disable_tracking() """
            x.delete()
        for x in user.person.emails.all():
            """ x.audit_log.disable_tracking() """
            x.delete()
        for x in user.person.skills.all():
            """ x.audit_log.disable_tracking() """
            x.delete()
        for x in user.person.languages.all():
            """ x.audit_log.disable_tracking() """
            x.delete()
        for x in user.person.educations.all():
            """ x.audit_log.disable_tracking() """
            x.delete()
        for x in user.person.work_experiences.all():
            """ x.audit_log.disable_tracking() """
            x.delete()
        for x in user.person.positions_of_trust.all():
            """ x.audit_log.disable_tracking() """
            x.delete()
        for x in user.person.student_organizational_activities.all():
            """ x.audit_log.disable_tracking() """
            x.delete()
        for x in user.person.volunteers.all():
            """ x.audit_log.disable_tracking() """
            x.delete()
        for x in user.person.honors.all():
            """ x.audit_log.disable_tracking() """
            x.delete()
        for x in user.person.interests.all():
            """ x.audit_log.disable_tracking() """
            x.delete()
        for x in user.person.family_members.all():
            """ x.audit_log.disable_tracking() """
            x.delete()
        """ user.person.audit_log.disable_tracking() """
        user.person.delete()
    user.delete()


@staff_member_required(login_url="/login/")
def admin(request):
    heading = "Admin: Users"

    first_name = request.GET.get("first_name", None)
    last_name = request.GET.get("last_name", None)
    admin_note = request.GET.get("admin_note", None)
    member_until_type = request.GET.get("member_until_type", None)
    member_until = request.GET.get("member_until", None)
    user_type = request.GET.get("member_type", None)

    user_list = getAdminSearchQueryset(
        first_name, last_name, admin_note, member_until_type, member_until, user_type
    )

    paginator = Paginator(user_list, 100)  # Show 100 users per page
    page = request.GET.get("page")
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        users = paginator.page(paginator.num_pages)
    if request.method == "POST" and "action" in request.POST:
        user = User.objects.get(pk=request.POST.get("user_id"))
        if user == request.user:  # Admin cannot edit own role
            return HttpResponseForbidden()
        if request.POST.get("action") == "make-admin":
            user.is_active = True
            user.is_staff = True
            user.is_hidden = False
            user.save()
        elif request.POST.get("action") == "make-user":
            user.is_active = True
            user.is_staff = False
            user.is_hidden = False
            user.save()
        elif request.POST.get("action") == "make-inactive":
            user.is_active = False
            user.is_staff = False
            user.is_hidden = False
            user.save()
        elif request.POST.get("action") == "make-hidden":
            user.is_hidden = True
            user.is_staff = False
            user.is_active = False
            user.save()
        elif request.POST.get("action") == "delete-user":
            delete_user(user)
        else:
            return HttpResponseForbidden()
        if (
            request.POST.get("action") != "delete-user"
            and (user.last_login is None)
            and user.is_active
        ):
            # inform user about activation of credentials
            subject = "Käyttäjätunnus aktivoitu"
            text_content = "Käyttäjätunnuksesi {} on aktivoitu ja voit nyt kirjautua alumnirekisteriin.".format(
                user.email
            )
            html_content = '<p>Käyttäjätunnuksesi <strong>{}</strong> on aktivoitu ja voit nyt kirjautua alumnirekisteriin.</p><br><p><a href="https://matrikkeli.prodeko.org">https://matrikkeli.prodeko.org</a></p>'.format(
                user.email
            )
            email_to = user.email
            from_email = "alumnirekisteri.no.reply@prodeko.org"
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [email_to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    elif request.method == "POST" and "admin_note" in request.POST:
        user = User.objects.get(pk=request.POST.get("user_id"))
        user.person.admin_note = request.POST.get("admin_note")
        user.person.save()

    return render(request, "admin.html", {"users": users, "heading": heading})


@staff_member_required(login_url="/login/")
def admin_member_requests(request):
    heading = "Admin: Pending member requests"
    user_list = User.objects.filter(is_active=False)
    if user_list is not None:
        paginator = Paginator(user_list, 100)  # Show 100 users per page
        page = request.GET.get("page")
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            users = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            users = paginator.page(paginator.num_pages)
        if request.method == "POST" and "action" in request.POST:
            user = User.objects.get(pk=request.POST.get("user_id"))
            if user == request.user:  # Admin cannot edit own role
                return HttpResponseForbidden()
            if request.POST.get("action") == "make-admin":
                user.is_active = True
                user.is_staff = True
                user.save()
            elif request.POST.get("action") == "make-user":
                user.is_active = True
                user.is_staff = False
                user.save()
            elif request.POST.get("action") == "make-inactive":
                user.is_active = False
                user.is_staff = False
                user.save()
            elif request.POST.get("action") == "delete-user":
                delete_user(user)
            else:
                return HttpResponseForbidden()
        return render(request, "admin.html", {"users": users, "heading": heading})
    return render("")


@staff_member_required(login_url="/login/")
def admin_export_matrikkeli(request):
    if request.GET.get("vuosikurssi", False):
        persons = (
            Person.objects.all()
            .filter(dont_publish_in_book=False)
            .filter(is_alumni=True)
            .order_by("class_of_year", "user__last_name")
        )
        response = HttpResponse(content_type="text/tex")
        response["charset"] = "utf-8"
        response["Content-Disposition"] = 'attachment; filename="vuosikurssit.tex"'
        response.write(render_to_string(
            "vuosikurssit.tex", {"persons": persons}))
        return response

    persons = (
        Person.objects.all()
        .select_related()
        .filter(is_alumni=True)
        .order_by("user__last_name", "user__first_name")
    )
    category = "alumni"
    if request.GET.get("type", False) == "kunniajasen":
        persons = persons.filter(member_type=5)
        category = "kunniajäsenet"
    if request.GET.get("type", False) == "tohtori":
        persons = filter(lambda person: person.is_tuta_doctor(), persons)
        category = "tohtorit"
    if request.GET.get("type", False) == "lisensiaatti":
        persons = filter(lambda person: person.is_tuta_lisensiaatti(), persons)
        category = "lisensiaatit"

    if not request.GET.get("images", False):
        response = HttpResponse(content_type="text/tex")
        response["charset"] = "utf-8"
        response["Content-Disposition"] = 'attachment; filename="' + \
            category + '.tex"'
        response.write(
            render_to_string(
                "matrikkeli.tex", {"persons": persons, "category": category}
            )
        )
        return response
    else:
        file_path = project_settings.MEDIA_ROOT + "/profiles"
        print("making zip")
        path_to_zip = make_archive(file_path, "zip", file_path)
        print("zip made")
        chunk_size = 8192
        response = StreamingHttpResponse(
            FileWrapper(open(path_to_zip, "rb"), chunk_size),
            content_type="application/zip",
        )
        response["Content-Length"] = os.path.getsize(path_to_zip)
        response["Content-Disposition"] = "attachment; filename=profile_pictures.zip"
        return response


@staff_member_required(login_url="/login/")
def admin_export_data(request):
    if request.method == "POST":
        response = HttpResponse(content_type="text/csv")
        response["charset"] = "utf-8"
        response.write("\ufeff")
        writer = unicodecsv.writer(response, delimiter="\t", encoding="utf-8")

        queryset = getAdminSearchQueryset(
            request.POST.get("first_name_search"),
            request.POST.get("last_name_search"),
            request.POST.get("admin_note_search"),
            request.POST.get("member_until_type"),
            request.POST.get("member_until_search"),
            request.POST.get("member_type_search"),
        )
        queryset = queryset.exclude(
            person__is_hidden=True).exclude(is_active=False)

        if request.POST.get("alive"):
            queryset = queryset.exclude(person__is_dead=True)

        def make_row(u):
            row = []

            if request.POST.get("email"):
                row.append(u.email)
            if request.POST.get("first_name"):
                row.append(u.first_name)
            if request.POST.get("last_name"):
                row.append(u.last_name)

            if hasattr(u, "person"):
                p = u.person
            else:
                return row

            if request.POST.get("middle_names"):
                row.append(p.middle_names)
            if request.POST.get("nickname"):
                row.append(p.nickname)
            if request.POST.get("preferred_name"):
                row.append(p.preferred_name)
            if request.POST.get("address"):
                row.append(p.address)
                row.append(p.postal_code)
                row.append(p.city)
                row.append(p.country)
            if request.POST.get("is_dead"):
                row.append(p.is_dead)
            if request.POST.get("birthdate"):
                row.append(p.birthdate)
            if request.POST.get("place_of_birth"):
                row.append(p.place_of_birth)
            if request.POST.get("gender"):
                row.append(p.get_gender_display())
            if request.POST.get("marital_status"):
                row.append(p.get_marital_status_display())
            if request.POST.get("military_rank"):
                row.append(p.military_rank)
                row.append(p.promotion_year)
            if request.POST.get("class_of_year"):
                row.append(p.class_of_year)
            if request.POST.get("member_until"):
                row.append(p.member_until)
            if request.POST.get("member_type"):
                row.append(p.get_member_type_display())
            if request.POST.get("student_number"):
                row.append(p.student_number)
            if request.POST.get("dont_publish_in_book"):
                row.append(p.dont_publish_in_book)
            if request.POST.get("mentoring"):
                row.append(p.mentoring)
                row.append(p.upper_management_mentoring)
                row.append(p.ventures)
            if request.POST.get("alumni_partners"):
                row.append(p.partner_contact)
            if request.POST.get("is_alumni"):
                row.append(p.is_alumni)
            if request.POST.get("subscribe_alumnimail"):
                row.append(p.subscribe_alumnimail)
            if request.POST.get("homepage"):
                row.append(p.homepage)
            if request.POST.get("linkedin_profile"):
                row.append(p.linkedin_profile)
            if request.POST.get("last_login"):
                row.append(p.user.last_login)
            if request.POST.get("admin_note"):
                row.append(p.admin_note)
            if request.POST.get("tuta_info"):
                row.append(p.get_starting_year())
                row.append(p.get_graduation_year())


            def displayPosition(x):
                return (
                    x.position
                    + " @ "
                    + x.organisation
                    + " ("
                    + (str(x.start_year) if x.start_year else "")
                    + "-"
                    + (str(x.end_year) if x.end_year else "")
                    + ")"
                )

            def displayEducation(x):
                return (
                    x.field
                    + ", "
                    + (x.get_degree_level_display() if x.degree_level else "")
                    + ": "
                    + (x.major if x.major else "")
                    + (x.minor if x.minor else "")
                    + (x.description if x.description else "")
                    + " @ "
                    + (x.school if x.school else "")
                    + " ("
                    + (str(x.start_year) if x.start_year else "")
                    + "-"
                    + (str(x.end_year) if x.end_year else "")
                    + ")"
                )

            if request.POST.get("phones"):
                row.append(
                    "§".join(map(lambda x: x.phone_number, p.phones.all())))
            if request.POST.get("work_experiences"):
                experiences = sorted(
                    p.work_experiences.all(), key=sortByEndDate)
                current_positions = filter(
                    lambda e: not e.end_year, experiences)
                current_position = ""
                current_organisation = ""
                row.append("§".join(map(displayPosition, current_positions)))
                row.append("§".join(map(displayPosition, experiences)))

            if request.POST.get("founded_companies"):
                founded_companies = sorted(p.work_experiences.filter(is_founding_member=True), key=sortByEndDate)
                row.append("§".join((x.organisation for x in founded_companies)))

            if request.POST.get("educations"):
                row.append(
                    "§".join(
                        map(
                            displayEducation,
                            sorted(p.educations.all(), key=sortByEndDate),
                        )
                    )
                )
            if request.POST.get("positions_of_trust"):
                row.append(
                    "§".join(
                        map(
                            displayPosition,
                            sorted(p.positions_of_trust.all(),
                                   key=sortByEndDate),
                        )
                    )
                )
            if request.POST.get("student_organizational_activities"):
                row.append(
                    "§".join(
                        map(
                            displayPosition,
                            sorted(
                                p.student_organizational_activities.all(),
                                key=sortByEndDate,
                            ),
                        )
                    )
                )
            if request.POST.get("volunteers"):
                row.append(
                    "§".join(
                        map(
                            displayPosition,
                            sorted(p.volunteers.all(), key=sortByEndDate),
                        )
                    )
                )
            if request.POST.get("honors"):
                row.append(
                    "§".join(
                        map(
                            lambda x: x.title
                            + ", "
                            + x.organisation
                            + (" (" + str(x.year) + ")" if x.year else ""),
                            sorted(p.honors.all(), key=sortByYear),
                        )
                    )
                )
            if request.POST.get("interests"):
                row.append("§".join(map(lambda x: x.title, p.interests.all())))
            if request.POST.get("family_members"):
                row.append(
                    "§".join(
                        map(
                            lambda x: x.first_name
                            + " "
                            + x.last_name
                            + "("
                            + x.get_member_type_display()
                            + ")",
                            p.family_members.all(),
                        )
                    )
                )
            return row

        rows = map(make_row, queryset)

        legend = []
        if request.POST.get("email"):
            legend.append("Sähköposti")
        if request.POST.get("first_name"):
            legend.append("Etunimi")
        if request.POST.get("last_name"):
            legend.append("Sukunimi")
        if request.POST.get("middle_names"):
            legend.append("Toiset nimet")
        if request.POST.get("nickname"):
            legend.append("Lempinimi")
        if request.POST.get("preferred_name"):
            legend.append("Kutsumanimi")
        if request.POST.get("address"):
            legend.append("Osoite")
            legend.append("Postinumero")
            legend.append("Kaupunki")
            legend.append("Maa")
        if request.POST.get("is_dead"):
            legend.append("Kuollut")
        if request.POST.get("birthdate"):
            legend.append("Syntymäaika")
        if request.POST.get("place_of_birth"):
            legend.append("Syntymäpaikka")
        if request.POST.get("gender"):
            legend.append("Sukupuoli")
        if request.POST.get("marital_status"):
            legend.append("Siviilisääty")
        if request.POST.get("military_rank"):
            legend.append("Sotilasarvo")
            legend.append("Ylennysvuosi")
        if request.POST.get("class_of_year"):
            legend.append("Aloittanut")
        if request.POST.get("member_until"):
            legend.append("Jäsenyys loppuu")
        if request.POST.get("member_type"):
            legend.append("Jäsenyystyyppi")
        if request.POST.get("student_number"):
            legend.append("Opiskelijanumero")
        if request.POST.get("dont_publish_in_book"):
            legend.append("Älä julkaise matrikkelissa")
        if request.POST.get("mentoring"):
            legend.append("Kiltamentorointi")
            legend.append("Ylemmän johdon mentorointi")
            legend.append("Ventures neuvonanto")
        if request.POST.get("alumni_partners"):
            legend.append("Alumnin yhteistyökumppanit")
        if request.POST.get("is_alumni"):
            legend.append("On alumni")
        if request.POST.get("subscribe_alumnimail"):
            legend.append("Vastaanota alumnikirje")
        if request.POST.get("homepage"):
            legend.append("Kotisivu")
        if request.POST.get("linkedin_profile"):
            legend.append("LinkedIn")
        if request.POST.get("last_login"):
            legend.append("Viimeksi kirjautunut")
        if request.POST.get("admin_note"):
            legend.append("Muistiinpano")

        if request.POST.get("phones"):
            legend.append("Puhelimet")
        if request.POST.get("work_experiences"):
            legend.append("Nykyiset toimenkuvat")
            legend.append("Kaikki työkokemukset")
        if request.POST.get("founded_companies"):
            legend.append("Perustetut yritykset")
        if request.POST.get("educations"):
            legend.append("Koulutus")
        if request.POST.get("positions_of_trust"):
            legend.append("Kunniatehtävät")
        if request.POST.get("student_organizational_activities"):
            legend.append("Opiskelija-aktiivisuus")
        if request.POST.get("volunteers"):
            legend.append("Vapaaehtoistoiminta")
        if request.POST.get("honors"):
            legend.append("Kunniat")
        if request.POST.get("interests"):
            legend.append("Kiinnostuksen kohteet")
        if request.POST.get("family_members"):
            legend.append("Perheenjäsenet")


        response["Content-Disposition"] = 'attachment; filename="somefilename.csv"'
        writer.writerow(legend)
        for person in rows:
            writer.writerow(person)

        return response
    else:
        return render(request, "admin_export_data.html", {})


@staff_member_required(login_url="/login/")
def admin_log(request):
    """ Show database changes """
    person_log = Person.audit_log.annotate(
        action_user_name=F("action_user__email")
    ).annotate(target=Value("Person", output_field=models.CharField()))
    phone_log = Phone.audit_log.annotate(
        action_user_name=F("action_user__email")
    ).annotate(target=Value("Phone", output_field=models.CharField()))
    email_log = Email.audit_log.annotate(
        action_user_name=F("action_user__email")
    ).annotate(target=Value("Email", output_field=models.CharField()))
    skill_log = Skill.audit_log.annotate(
        action_user_name=F("action_user__email")
    ).annotate(target=Value("Skill", output_field=models.CharField()))
    language_log = Language.audit_log.annotate(
        action_user_name=F("action_user__email")
    ).annotate(target=Value("Language", output_field=models.CharField()))
    education_log = Education.audit_log.annotate(
        action_user_name=F("action_user__email")
    ).annotate(target=Value("Education", output_field=models.CharField()))
    work_experience_log = WorkExperience.audit_log.annotate(
        action_user_name=F("action_user__email")
    ).annotate(target=Value("WorkExperience", output_field=models.CharField()))
    position_of_trust_log = PositionOfTrust.audit_log.annotate(
        action_user_name=F("action_user__email")
    ).annotate(target=Value("PositionOfTrust", output_field=models.CharField()))
    student_organizational_activity_log = (
        StudentOrganizationalActivity.audit_log.annotate(
            action_user_name=F("action_user__email")
        ).annotate(
            target=Value(
                "StudentOrganizationalActivity", output_field=models.CharField()
            )
        )
    )
    volunteer_log = Volunteer.audit_log.annotate(
        action_user_name=F("action_user__email")
    ).annotate(target=Value("Volunteer", output_field=models.CharField()))
    honor_log = Honor.audit_log.annotate(
        action_user_name=F("action_user__email")
    ).annotate(target=Value("Honor", output_field=models.CharField()))
    interest_log = Interest.audit_log.annotate(
        action_user_name=F("action_user__email")
    ).annotate(target=Value("Interest", output_field=models.CharField()))
    family_member_log = FamilyMember.audit_log.annotate(
        action_user_name=F("action_user__email")
    ).annotate(target=Value("FamilyMember", output_field=models.CharField()))
    log_all = sorted(
        chain(
            person_log,
            phone_log,
            email_log,
            skill_log,
            language_log,
            education_log,
            work_experience_log,
            position_of_trust_log,
            student_organizational_activity_log,
            volunteer_log,
            honor_log,
            interest_log,
            family_member_log,
        ),
        key=lambda entry: entry.action_date,
        reverse=True,
    )
    paginator = Paginator(log_all, 100)  # Show 100 per page
    page = request.GET.get("page")
    try:
        log = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        log = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        log = paginator.page(paginator.num_pages)
    return render(request, "admin_log.html", {"log": log})


@staff_member_required(login_url="/login/")
def admin_stats(request):
    total_count = len(User.objects.all())
    logged_in = total_count - len(User.objects.all().filter(last_login=None))

    dont_publish_in_book = len(
        Person.objects.all().filter(dont_publish_in_book=True))
    dont_publish_in_book_logged_in = len(
        Person.objects.all()
        .filter(dont_publish_in_book=True)
        .exclude(user__last_login=None)
    )

    show_phones_category = len(
        Person.objects.all().filter(show_phones_category=True))
    show_emails_category = len(
        Person.objects.all().filter(show_emails_category=True))
    show_skills_category = len(
        Person.objects.all().filter(show_skills_category=True))
    show_languages_category = len(
        Person.objects.all().filter(show_languages_category=True)
    )
    show_educations_category = len(
        Person.objects.all().filter(show_educations_category=True)
    )
    show_work_experiences_category = len(
        Person.objects.all().filter(show_work_experiences_category=True)
    )
    show_positions_of_trust_category = len(
        Person.objects.all().filter(show_positions_of_trust_category=True)
    )
    show_volunteers_category = len(
        Person.objects.all().filter(show_volunteers_category=True)
    )
    show_honors_category = len(
        Person.objects.all().filter(show_honors_category=True))
    show_interests_category = len(
        Person.objects.all().filter(show_interests_category=True)
    )
    show_student_organizational_activities_category = len(
        Person.objects.all().filter(
            show_student_organizational_activities_category=True
        )
    )
    show_family_members_category = len(
        Person.objects.all().filter(show_family_members_category=True)
    )

    draw_logged = str(math.ceil(logged_in / total_count * 100)) + "%"
    draw_dont_publish_in_book = (
        str(math.ceil(dont_publish_in_book / total_count * 100)) + "%"
    )
    draw_dont_publish_in_book_logged = (
        str(
            math.ceil(dont_publish_in_book_logged_in /
                      (dont_publish_in_book + 1) * 100)
        )
        + "%"
    )

    return render(
        request,
        "admin_stats.html",
        {
            "draw_logged": draw_logged,
            "draw_dont_publish_in_book": draw_dont_publish_in_book,
            "draw_dont_publish_in_book_logged": draw_dont_publish_in_book_logged,
            "total_count": total_count,
            "logged_in": logged_in,
            "dont_publish_in_book": dont_publish_in_book,
            "dont_publish_in_book_logged_in": dont_publish_in_book_logged_in,
            "show_phones_category": show_phones_category,
            "show_emails_category": show_emails_category,
            "show_skills_category": show_skills_category,
            "show_languages_category": show_languages_category,
            "show_educations_category": show_educations_category,
            "show_work_experiences_category": show_work_experiences_category,
            "show_positions_of_trust_category": show_positions_of_trust_category,
            "show_volunteers_category": show_volunteers_category,
            "show_honors_category": show_honors_category,
            "show_interests_category": show_interests_category,
            "show_student_organizational_activities_category": show_student_organizational_activities_category,
            "show_family_members_category": show_family_members_category,
        },
    )


@staff_member_required(login_url="/login/")
def admin_set_notes(request):
    notes_output = ""
    membership_output = ""
    duplicate_output = ""
    datatype = ""

    if request.method == "POST":
        notes_file = request.FILES.get("notes_file")
        membership_file = request.FILES.get("membership_file")

        if notes_file:
            datafile = notes_file
            datatype = "note"
            notes_output += str(datafile)

        if membership_file:
            datafile = membership_file
            datatype = "membership"
            membership_output += str(datafile)

        if datafile:
            try:
                f = TextIOWrapper(
                    datafile.file, encoding="utf-8 ", errors="replace")
            except:
                f = StringIO(datafile.file.read().decode())
            dialect = csv.Sniffer().sniff(f.read(), delimiters=";,")
            f.seek(0)
            notes = csv.reader(f, dialect)

            for row in notes:
                print(row)
                names = row[1].split(" ", 1)
                try:
                    print(row)
                    user = User.objects.get(email__iexact=row[3])
                    membership_output += (
                        "User found: " + row[0] + ", " +
                        row[1] + ", " + row[3] + "<br>"
                    )
                except:
                    try:
                        # löyty nimellä, eri email
                        user = User.objects.get(
                            first_name__iexact=names[0], last_name__iexact=row[0]
                        )
                        duplicate_output += (
                            row[0]
                            + ", "
                            + row[1]
                            + ", "
                            + row[3]
                            + " != "
                            + user.email
                            + ";"
                        )
                        # print(user.email, row[2])
                        continue
                    except:
                        # ei löytynyt emaililla eikä nimellä
                        membership_output += (
                            "Didn't find person: "
                            + row[0]
                            + ", "
                            + row[1]
                            + ", "
                            + row[3]
                            + "<br/>"
                        )
                        if datatype == "membership":
                            membership_output += (
                                "creating user: "
                                + row[0]
                                + ", "
                                + row[1]
                                + ", "
                                + row[3]
                                + "<br/>"
                            )
                            u = User.objects.create_user(email=row[3])
                            u.email = row[3]

                            u.first_name = names[0]
                            u.last_name = row[0]
                            u.password = "".join(
                                random.choice(
                                    string.ascii_uppercase + string.digits)
                                for _ in range(32)
                            )
                            u.save()
                            p = u.person
                            if len(names) > 1:
                                p.middle_names = names[1]
                            p.city = row[2]
                            p.is_alumni = False
                            p.member_type = 1
                            p.ayy_member = True

                            if row[6]:
                                p.member_until = row[6]
                            if row[4]:
                                p.class_of_year = row[4]
                                if row[5]:
                                    p.xq_year = row[5]
                                else:
                                    p.xq_year = row[4]
                            p.save()
                        continue

                    # print(e, row[3] + " not found")

                p = user.person
                if hasattr(user, "person"):
                    if datatype == "note":
                        user.person.admin_note = row[3]
                        user.person.save()
                    elif datatype == "membership":
                        user.person.member_until = row[3]
                        user.first_name = names[0]
                        user.last_name = row[0]
                        if len(names) > 1:
                            p.middle_names = names[1]
                        if row[2]:
                            p.city = row[2]
                        if row[6]:
                            p.member_until = row[6]
                        if row[4]:
                            p.class_of_year = row[4]
                            if row[5]:
                                p.xq_year = row[5]
                            else:
                                p.xq_year = row[4]
                        user.save()
                        user.person.save()

    return render(
        request,
        "admin_set_notes.html",
        {
            "notes_output": notes_output,
            "membership_output": membership_output,
            "duplicate_output": duplicate_output,
        },
    )


@login_required(login_url="/login/")
def index(request):
    """ Index """
    return render(request, "ar_index.html")


@staff_member_required(login_url="/login/")
def admin_edit_person_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    person = user.person
    return edit_person(
        user,
        person,
        True,
        "admin_edit_person.html",
        reverse("alumnirekisteri:admin_edit_person_view", args=[pk]),
        request,
    )


@login_required(login_url="/login/")
def myprofile(request):
    user = request.user
    person = user.person
    return edit_person(
        user,
        person,
        False,
        "myprofile/myprofile.html",
        reverse("alumnirekisteri:myprofile"),
        request,
    )


@login_required(login_url="/login/")
def membership_status(request):    
    user = request.user
    person = user.person

    today = datetime.today().date()
    six_months_from_now = today + timedelta(days=182)  # approx. 6 months
    should_pay = today < person.member_until < six_months_from_now
    is_expired = person.member_until < today
    return render(
        request,
        "myprofile/myprofile_membership.html",
        {
            "name": f"{user.first_name} {user.last_name}",
            "person_id": person.pk,
            "email": user.email,
            "should_pay": should_pay,
            "is_expired": is_expired,
            "membership_data": [
                ("Member until", person.member_until),
                ("Member type", person.get_member_type_display()),
                ("AYY member", "Yes" if person.ayy_member else "No"),
                ("Class of year", person.class_of_year),
                ("XQ year (year you use to register to events)", person.xq_year),
            ]
        }
    )


def edit_person(user, person, adminview, template, form_action_url, request):
    # forms
    user_form = UserForm(instance=user, prefix="user_form")
    person_form = PersonForm(instance=person, prefix="person_form")
    if request.user.is_staff and adminview:
        admin_form = AdminPersonForm(instance=person, prefix="admin_form")
    else:
        admin_form = None
    # Submit Both Forms
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user, prefix="user_form")
        person_form = PersonForm(
            request.POST, instance=person, prefix="person_form")

        if request.user.is_staff and adminview:
            admin_form = AdminPersonForm(
                request.POST, instance=person, prefix="admin_form"
            )
            forms = [user_form, person_form, admin_form]
        else:
            forms = [user_form, person_form]

        image_file = request.FILES.get("crop_image_data")
        if image_file:
            if person.picture:
                person.picture.delete(False)
            person.picture = image_file
            person.save()
        if all([form.is_valid() for form in forms]):
            for form in forms:
                obj = form.save()
            messages.success(request, "Tiedot tallennettu")
            return JsonResponse({"success": True})
        else:
            return JsonResponse(
                {
                    "success": False,
                    "errors": {
                        "user_form": dict(user_form.errors.items()),
                        "person_form": dict(person_form.errors.items()),
                        "admin_form": dict(admin_form.errors.items())
                        if request.user.is_staff
                        else None,
                    },
                }
            )
    return render(
        request,
        template,
        {
            "person_pk": person.pk,
            "last_login": user.last_login,
            "form_action_url": form_action_url,
            "user_form": user_form,
            "person_form": person_form,
            "admin_form": admin_form,
            "image_url": person.get_picture_url(),
            # related information
            "phones": person.phones.all(),
            "emails": person.emails.all(),
            "skills": person.skills.all(),
            "languages": person.languages.all(),
            "educations": sorted(person.educations.all(), key=sortByEndDate),
            "work_experiences": sorted(
                person.work_experiences.all(), key=sortByEndDate
            ),
            "positions_of_trust": sorted(
                person.positions_of_trust.all(), key=sortByEndDate
            ),
            "student_organizational_activities": sorted(
                person.student_organizational_activities.all(), key=sortByEndDate
            ),
            "volunteers": sorted(person.volunteers.all(), key=sortByEndDate),
            "honors": sorted(person.honors.all(), key=sortByYear),
            "interests": person.interests.all(),
            "family_members": person.family_members.all(),
            # related information forms
            "phone_form": PhoneForm(),
            "email_form": EmailForm(),
            "skill_form": SkillForm(),
            "language_form": LanguageForm(),
            "education_form": EducationForm(),
            "experience_form": WorkExperienceForm(),
            "positions_of_trust_form": PositionOfTrustForm(),
            "student_activity_form": StudentActivityForm(),
            "volunteer_form": VolunteerForm(),
            "honor_form": HonorForm(),
            "interest_form": InterestForm(),
            "family_member_form": FamilyMemberForm(),
        },
    )


@login_required(login_url="/login/")
def settings(request):
    user_form = UserForm(instance=request.user, prefix="user_form")
    person_form = PersonForm(
        instance=request.user.person, prefix="person_form")
    if request.method == "POST":
        user_form = UserForm(
            request.POST, instance=request.user, prefix="user_form")
        person_form = PersonForm(
            request.POST, instance=request.user.person, prefix="person_form"
        )
        forms = [user_form, person_form]
        if all([form.is_valid() for form in forms]):
            for form in forms:
                form.save()
            messages.success(request, "Tiedot tallennettu")
            return JsonResponse({"success": True})
        else:
            return JsonResponse(
                {
                    "success": False,
                    "errors": {
                        "user_form": dict(user_form.errors.items()),
                        "person_form": dict(person_form.errors.items()),
                    },
                }
            )
    return render(
        request,
        "settings/settings.html",
        {
            "user_form": user_form,
            "form_action_url": reverse("alumnirekisteri:settings"),
            "person_form": person_form,
        },
    )


@login_required(login_url="/login/")
def add_phone(request, person_pk):
    """ Add a new phone number object """
    form = PhoneForm()
    if request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = Person.objects.get(pk=person_pk)
            obj.save()
            messages.success(request, "Uusi puhelinnumero lisätty")
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return HttpResponseForbidden()


@login_required(login_url="/login/")
def edit_phone(request, pk):
    """ Edit an existing phone object """
    obj = get_object_or_404(Phone, pk=pk)
    form = PhoneForm(instance=obj)
    if request.method == "POST":
        form = PhoneForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Puhelinnumero päivitetty")
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/edit_modal.html",
        {
            "title": "Muokkaa",
            "form": form,
            "url": reverse("alumnirekisteri:edit_phone", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def delete_phone(request, pk):
    """ Delete an existing phone object """
    obj = get_object_or_404(Phone, pk=pk)
    form = PhoneForm(instance=obj)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Puhelinnumero poistettu")
        return JsonResponse({"success": True})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista puhelinnumero",
            "text": "Poistetaanko {}?".format(obj.phone_number),
            "url": reverse("alumnirekisteri:delete_phone", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def add_email(request, person_pk):
    """ Add a new email object """
    form = EmailForm()
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = Person.objects.get(pk=person_pk)
            obj.save()
            messages.success(request, "Uusi sähköpostiosoite lisätty")
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return HttpResponseForbidden()


@login_required(login_url="/login/")
def edit_email(request, pk):
    """ Edit an existing email object """
    obj = get_object_or_404(Email, pk=pk)
    form = EmailForm(instance=obj)
    if request.method == "POST":
        form = EmailForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Sähköposti päivitetty")
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/edit_modal.html",
        {
            "title": "Muokkaa",
            "form": form,
            "url": reverse("alumnirekisteri:edit_phone", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def delete_email(request, pk):
    """ Delete an existing email object """
    obj = get_object_or_404(Email, pk=pk)
    form = EmailForm(instance=obj)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Sähköpostiosoite poistettu")
        return JsonResponse({"success": True})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista sähköpostiosoite",
            "text": "Poistetaanko {}?".format(obj.address),
            "url": reverse("alumnirekisteri:delete_email", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def add_skill(request, person_pk):
    """ Add a new skill object """
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = Person.objects.get(pk=person_pk)
            obj.save()
            messages.success(request, "Uusi skilli lisätty")
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return HttpResponseForbidden()


@login_required(login_url="/login/")
def edit_skill(request, pk):
    """ Edit an existing skill object """
    obj = get_object_or_404(Skill, pk=pk)
    form = SkillForm(instance=obj)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Skilli päivitetty")
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/edit_modal.html",
        {
            "title": "Muokkaa",
            "form": form,
            "url": reverse("alumnirekisteri:edit_skill", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def delete_skill(request, pk):
    """ Delete an existing skill object """
    obj = get_object_or_404(Skill, pk=pk)
    form = SkillForm(instance=obj)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Skilli poistettu")
        return JsonResponse({"success": True})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista skilli",
            "text": "Poistetaanko {}?".format(obj.title),
            "url": reverse("alumnirekisteri:delete_skill", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def add_language(request, person_pk):
    """ Add a new language object """
    form = LanguageForm()
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = Person.objects.get(pk=person_pk)
            obj.save()
            messages.success(request, "Uusi kieli lisätty")
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return HttpResponseForbidden()


@login_required(login_url="/login/")
def edit_language(request, pk):
    """ Edit an existing language object """
    obj = get_object_or_404(Language, pk=pk)
    form = LanguageForm(instance=obj)
    if request.method == "POST":
        form = LanguageForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Kielitieto päivitetty")
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/edit_modal.html",
        {
            "title": "Muokkaa",
            "form": form,
            "url": reverse("alumnirekisteri:edit_language", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def delete_language(request, pk):
    """ Delete an existing language object """
    obj = get_object_or_404(Language, pk=pk)
    form = LanguageForm(instance=obj)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Kieli poistettu")
        return JsonResponse({"success": True})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista kieli",
            "text": "Poistetaanko {}?".format(obj.language),
            "url": reverse("alumnirekisteri:delete_language", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def add_education(request, person_pk):
    """ Add a new education object """
    form = EducationForm()
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = Person.objects.get(pk=person_pk)
            obj.save()
            messages.success(request, "Uusi koulutus lisätty")
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return HttpResponseForbidden()


@login_required(login_url="/login/")
def edit_education(request, pk):
    """ Edit an existing education object """
    obj = get_object_or_404(Education, pk=pk)
    form = EducationForm(instance=obj)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Koulutustieto päivitetty")
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/edit_modal.html",
        {
            "title": "Muokkaa koulutusta",
            "form": form,
            "url": reverse("alumnirekisteri:edit_education", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def delete_education(request, pk):
    """ Delete an existing education object """
    obj = get_object_or_404(Education, pk=pk)
    form = EducationForm(instance=obj)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Koulutustieto poistettu")
        return JsonResponse({"success": True})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista koulutus",
            "text": "Poistetaanko {}?".format(obj.school),
            "url": reverse("alumnirekisteri:delete_education", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def add_work_experience(request, person_pk):
    """ Add a new work experience object """
    form = WorkExperienceForm()
    if request.method == "POST":
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = Person.objects.get(pk=person_pk)
            obj.save()
            messages.success(request, "Uusi työkokemus lisätty")
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return HttpResponseForbidden()


@login_required(login_url="/login/")
def edit_work_experience(request, pk):
    """ Edit an existing work eperience object """
    obj = get_object_or_404(WorkExperience, pk=pk)
    form = WorkExperienceForm(instance=obj)
    if request.method == "POST":
        form = WorkExperienceForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Työkokemus päivitetty")
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/edit_modal.html",
        {
            "title": "Muokkaa työkokemusta",
            "form": form,
            "url": reverse("alumnirekisteri:edit_work_experience", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def delete_work_experience(request, pk):
    """ Delete an existing work experinece object """
    obj = get_object_or_404(WorkExperience, pk=pk)
    form = EducationForm(instance=obj)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Työkokemus poistettu")
        return JsonResponse({"success": True})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista työkokemus",
            "text": "Poistetaanko {}?".format(obj.organisation),
            "url": reverse("alumnirekisteri:delete_work_experience", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def add_position_of_trust(request, person_pk):
    """ Add a new position of trust object """
    form = PositionOfTrustForm()
    if request.method == "POST":
        form = PositionOfTrustForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = Person.objects.get(pk=person_pk)
            obj.save()
            # messages.success(request, 'Uusi työkokemus lisätty')
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return HttpResponseForbidden()


@login_required(login_url="/login/")
def edit_position_of_trust(request, pk):
    """ Edit an existing position of trust object """
    obj = get_object_or_404(PositionOfTrust, pk=pk)
    form = PositionOfTrustForm(instance=obj)
    if request.method == "POST":
        form = PositionOfTrustForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Työkokemus päivitetty')
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/edit_modal.html",
        {
            "title": "Muokkaa",
            "form": form,
            "url": reverse("alumnirekisteri:edit_position_of_trust", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def delete_position_of_trust(request, pk):
    """ Delete an existing position of trust object """
    obj = get_object_or_404(PositionOfTrust, pk=pk)
    form = PositionOfTrustForm(instance=obj)
    if request.method == "POST":
        obj.delete()
        # messages.success(request, 'Luottamustehtävä poistettu')
        return JsonResponse({"success": True})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista",
            "text": "Poistetaanko {}?".format(obj.organisation),
            "url": reverse("alumnirekisteri:delete_position_of_trust", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def add_student_activity(request, person_pk):
    """ Add a new student activity object """
    form = StudentActivityForm()
    if request.method == "POST":
        form = StudentActivityForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = Person.objects.get(pk=person_pk)
            obj.save()
            # messages.success(request, 'Uusi työkokemus lisätty')
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return HttpResponseForbidden()


@login_required(login_url="/login/")
def edit_student_activity(request, pk):
    """ Edit an existing student activity object """
    obj = get_object_or_404(StudentOrganizationalActivity, pk=pk)
    form = StudentActivityForm(instance=obj)
    if request.method == "POST":
        form = StudentActivityForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Työkokemus päivitetty')
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/edit_modal.html",
        {
            "title": "Muokkaa",
            "form": form,
            "url": reverse("alumnirekisteri:edit_student_activity", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def delete_student_activity(request, pk):
    """ Delete an existing student activity object """
    obj = get_object_or_404(StudentOrganizationalActivity, pk=pk)
    form = StudentActivityForm(instance=obj)
    if request.method == "POST":
        obj.delete()
        # messages.success(request, 'Luottamustehtävä poistettu')
        return JsonResponse({"success": True})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista",
            "text": "Poistetaanko {}?".format(obj.organisation),
            "url": reverse("alumnirekisteri:delete_student_activity", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def add_volunteer(request, person_pk):
    """ Add a new volunteer object """
    form = VolunteerForm()
    if request.method == "POST":
        form = VolunteerForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = Person.objects.get(pk=person_pk)
            obj.save()
            # messages.success(request, 'Uusi työkokemus lisätty')
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return HttpResponseForbidden()


@login_required(login_url="/login/")
def edit_volunteer(request, pk):
    """ Edit an existing volunteer object """
    obj = get_object_or_404(Volunteer, pk=pk)
    form = VolunteerForm(instance=obj)
    if request.method == "POST":
        form = VolunteerForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Työkokemus päivitetty')
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/edit_modal.html",
        {
            "title": "Muokkaa",
            "form": form,
            "url": reverse("alumnirekisteri:edit_volunteer", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def delete_volunteer(request, pk):
    """ Delete an existing volunteer object """
    obj = get_object_or_404(Volunteer, pk=pk)
    form = VolunteerForm(instance=obj)
    if request.method == "POST":
        obj.delete()
        # messages.success(request, 'Luottamustehtävä poistettu')
        return JsonResponse({"success": True})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista",
            "text": "Poistetaanko {}?".format(obj.organisation),
            "url": reverse("alumnirekisteri:delete_volunteer", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def add_honor(request, person_pk):
    """ Add a new honor object """
    form = HonorForm()
    if request.method == "POST":
        form = HonorForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = Person.objects.get(pk=person_pk)
            obj.save()
            # messages.success(request, 'Uusi työkokemus lisätty')
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return HttpResponseForbidden()


@login_required(login_url="/login/")
def edit_honor(request, pk):
    """ Edit an existing honor object """
    obj = get_object_or_404(Honor, pk=pk)
    form = HonorForm(instance=obj)
    if request.method == "POST":
        form = HonorForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Työkokemus päivitetty')
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/edit_modal.html",
        {
            "title": "Muokkaa",
            "form": form,
            "url": reverse("alumnirekisteri:edit_honor", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def delete_honor(request, pk):
    """ Delete an existing honor object """
    obj = get_object_or_404(Honor, pk=pk)
    form = HonorForm(instance=obj)
    if request.method == "POST":
        obj.delete()
        # messages.success(request, 'Luottamustehtävä poistettu')
        return JsonResponse({"success": True})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista",
            "text": "Poistetaanko {}?".format(obj.title),
            "url": reverse("alumnirekisteri:delete_honor", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def add_interest(request, person_pk):
    """ Add a new interest object """
    form = InterestForm()
    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = Person.objects.get(pk=person_pk)
            obj.save()
            # messages.success(request, 'Uusi työkokemus lisätty')
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return HttpResponseForbidden()


@login_required(login_url="/login/")
def edit_interest(request, pk):
    """ Edit an existing interest object """
    obj = get_object_or_404(Interest, pk=pk)
    form = InterestForm(instance=obj)
    if request.method == "POST":
        form = InterestForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Työkokemus päivitetty')
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/edit_modal.html",
        {
            "title": "Muokkaa",
            "form": form,
            "url": reverse("alumnirekisteri:edit_interest", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def delete_interest(request, pk):
    """ Delete an existing interest object """
    obj = get_object_or_404(Interest, pk=pk)
    form = InterestForm(instance=obj)
    if request.method == "POST":
        obj.delete()
        # messages.success(request, 'Luottamustehtävä poistettu')
        return JsonResponse({"success": True})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista",
            "text": "Poistetaanko {}?".format(obj.title),
            "url": reverse("alumnirekisteri:delete_interest", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def add_family_member(request, person_pk):
    """ Add a new family member object """
    form = FamilyMemberForm()
    if request.method == "POST":
        form = FamilyMemberForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = Person.objects.get(pk=person_pk)
            obj.save()
            # messages.success(request, 'Uusi työkokemus lisätty')
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return HttpResponseForbidden()


@login_required(login_url="/login/")
def edit_family_member(request, pk):
    """ Edit an existing family member object """
    obj = get_object_or_404(FamilyMember, pk=pk)
    form = FamilyMemberForm(instance=obj)
    if request.method == "POST":
        form = FamilyMemberForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Työkokemus päivitetty')
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/edit_modal.html",
        {
            "title": "Muokkaa",
            "form": form,
            "url": reverse("alumnirekisteri:edit_family_member", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def delete_family_member(request, pk):
    """ Delete an existing family member object """
    obj = get_object_or_404(FamilyMember, pk=pk)
    form = FamilyMemberForm(instance=obj)
    if request.method == "POST":
        obj.delete()
        # messages.success(request, 'Luottamustehtävä poistettu')
        return JsonResponse({"success": True})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista",
            "text": "Poistetaanko {}?".format(obj.get_full_name()),
            "url": reverse("alumnirekisteri:delete_family_member", args=[obj.pk]),
        },
    )


@login_required(login_url="/login/")
def new_password(request):
    """ New password page """
    password_form = PasswordChangeForm(user=request.user)
    return render(request, "new_password.html", {"password_form": password_form})


@login_required(login_url="/login/")
def change_password(request):
    """ Post change password form """
    if request.method == "POST":
        user = request.user
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Salasana vaihdettu")
        else:
            for key in form.errors:
                messages.warning(
                    request, form.fields[key].label +
                    ": " + form.errors[key][0]
                )
    return redirect("rekisteri.views.new_password")


@login_required(login_url="/login/")
def public_profile(request, slug):
    """ Profile """
    profile = get_object_or_404(Person, slug=slug)
    # if not request.user.is_staff and (profile.is_alumni != request.user.person.is_alumni):
    #    return HttpResponseNotFound('<h1>Person not found</h1>')

    return render(request, "public_profile.html", {"profile": profile})


@login_required(login_url="/login/")
def search(request):
    """ Search persons """
    queryset = Person.objects.exclude(
        is_hidden=True).exclude(user__is_active=False)
    first_name = request.GET.get("search_first_name", None)
    last_name = request.GET.get("search_last_name", None)
    class_of_year = request.GET.get("search_start_year", None)
    if last_name:
        queryset = queryset.filter(
            Q(user__last_name__icontains=last_name)
            | Q(original_last_name__icontains=last_name)
        )
    if first_name:
        queryset = queryset.filter(
            Q(user__first_name__icontains=first_name)
            | Q(nickname__icontains=first_name)
            | Q(preferred_name__icontains=first_name)
        )
    if class_of_year is not None and class_of_year.isdigit():
        queryset = queryset.filter(class_of_year__contains=class_of_year)

    # if not request.user.is_staff:
    # queryset = queryset.filter(is_alumni=request.user.person.is_alumni)

    queryset = queryset.order_by("user__last_name")
    paginator = Paginator(queryset, 50)  # Show 50 users per page
    page = request.GET.get("page")
    try:
        persons = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        persons = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        persons = paginator.page(paginator.num_pages)

    return render(
        request,
        "search.html",
        {
            "persons": persons,
            "first_name": first_name,
            "last_name": last_name,
            "class_of_year": class_of_year,
            "page": page,
        },
    )


@staff_member_required(login_url="/login/")
def register(request):
    """ Page for sign up """
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user, person = form.save()
            user.is_active = True
            user.save()
            form = RegisterForm()
    return render(request, "register.html", {"form": form})


@staff_member_required(login_url="/login/")
def confirmation(request):
    """ Confirmation page after sign up """
    return render(request, "confirmation.html", {})


@login_required(login_url="/login/")
def delete_profile(request):
    """ Delete the currently logged in user """
    form = LoginForm(request, data=request.POST)
    if request.method == "POST":
        if not (
            form.data["username"] == request.user.username
            or form.data["username"] == request.user.email
        ):
            form.add_error("username", "Ei kelpaa")
        if form.is_valid():
            user = request.user
            delete_user(user)
            """
            person = Person.objects.get(user=user)
            person.delete()
            user.delete()
            """
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": dict(form.errors.items())})
    return render(
        request,
        "modals/delete_modal.html",
        {
            "title": "Poista",
            "text": "Tämä toiminto poistaa profiilisi ja kaikki tietosi pysyvästi alumnirekisteristä. Varmista toiminto antamalla käyttäjätunnuksesi.",
            "form": form,
            "url": reverse("alumnirekisteri:delete_profile"),
        },
    )
