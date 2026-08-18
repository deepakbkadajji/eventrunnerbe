from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_datetime
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models.deletion import ProtectedError
from api.models import ParticipantTable
from api.models import ParticipantEventTable
from api.models import EventDetailTable
from api.models import EventSubDetailTable
from api.models import EventCategoryTable
from api.models import EventSponsorTable
from api.models import EventNotificationTable
from api.models import EventInformationTable
from api.models import EventImages
from api.models import OrganisationTable
from api.models import OrganisationMemberTable
from api.models import AthleticAssociationTable
from api.models import AthleticsCategoryTable
from api.models import AthleticOrganisationTable
from api.models import AthleticOrganisationMemberTable
from api.models import AthleticOrganisationCategoryTable
from api.models import SubscriptionPlanTable
from api.models import SubscriptionTable
from api.models import AppReleaseVersionTable
from api.models import TermsAndConditionsTable
from api.util import OrganisationMemberRole, OrganisationMemberStatus, OrganisationType
from api.util import EventStatus, SponsorCategory, Gender
from api.util import SubscriberType, BillingFrequency, SubscriptionStatus
from api.subscription_validation import (
    validate_club_can_create_event,
    new_event_status_choices,
    is_allowed_new_event_status,
)
from api.views import (
    _athletic_organisation_kwargs,
    _move_athletic_organisation,
    _update_athletic_organisation_fields,
    _validate_athletic_organisation_required_fields,
)
from api.serializers import EventSubDetailSerializer , EventDetailSerializer

# Create your views here.
def home(request):
    return render(request, 'website/home.html')

def about(request):
    return render(request, 'website/about.html')

@login_required
def userhome(request):
    return render(request, 'website/userhome.html')


def _optional_int(value):
    if value in (None, ""):
        return None
    return int(value)


def _administrator_section_for_action(action):
    section_map = {
        "add_category": "event-categories",
        "edit_category": "event-categories",
        "delete_category": "event-categories",
        "add_plan": "subscription-plans",
        "edit_plan": "subscription-plans",
        "delete_plan": "subscription-plans",
        "add_subscription": "subscriptions",
        "edit_subscription": "subscriptions",
        "delete_subscription": "subscriptions",
        "add_app_release_version": "app-release-versions",
        "edit_app_release_version": "app-release-versions",
        "delete_app_release_version": "app-release-versions",
        "add_terms": "terms-and-conditions",
        "edit_terms": "terms-and-conditions",
        "delete_terms": "terms-and-conditions",
    }
    return section_map.get(action, "event-categories")


@login_required
@require_http_methods(["GET", "POST"])
def administrator(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_category":
            name = request.POST.get("categoryname", "").strip()
            if not name:
                messages.error(request, "Category name is required.")
            elif EventCategoryTable.objects.filter(categoryname=name).exists():
                messages.error(request, "This category already exists.")
            else:
                EventCategoryTable.objects.create(categoryname=name)
                messages.success(request, "Event category added.")

        elif action == "edit_category":
            category = EventCategoryTable.objects.filter(id=request.POST.get("category_id")).first()
            name = request.POST.get("categoryname", "").strip()
            if not category:
                messages.error(request, "Category not found.")
            elif not name:
                messages.error(request, "Category name is required.")
            elif EventCategoryTable.objects.filter(categoryname=name).exclude(id=category.id).exists():
                messages.error(request, "Another category with this name already exists.")
            else:
                category.categoryname = name
                category.save()
                messages.success(request, "Event category updated.")

        elif action == "delete_category":
            category = EventCategoryTable.objects.filter(id=request.POST.get("category_id")).first()
            if category:
                category.delete()
                messages.success(request, "Event category deleted.")
            else:
                messages.error(request, "Category not found.")

        elif action == "add_plan":
            plancode = request.POST.get("plancode", "").strip()
            planname = request.POST.get("planname", "").strip()
            if not plancode or not planname:
                messages.error(request, "Plan code and name are required.")
            elif SubscriptionPlanTable.objects.filter(plancode=plancode).exists():
                messages.error(request, "A plan with this code already exists.")
            else:
                SubscriptionPlanTable.objects.create(
                    plancode=plancode,
                    planname=planname,
                    subscribertype=int(request.POST.get("subscribertype", SubscriberType.Participant)),
                    billingfrequency=int(request.POST.get("billingfrequency", BillingFrequency.Monthly)),
                    price=request.POST.get("price") or 0,
                    currencycode=request.POST.get("currencycode", "ZAR") or "ZAR",
                    maximummembers=_optional_int(request.POST.get("maximummembers")),
                    maximumevents=_optional_int(request.POST.get("maximumevents")),
                    isactive=request.POST.get("isactive") == "true",
                )
                messages.success(request, "Subscription plan added.")

        elif action == "edit_plan":
            plan = SubscriptionPlanTable.objects.filter(id=request.POST.get("plan_id")).first()
            if not plan:
                messages.error(request, "Subscription plan not found.")
            else:
                plancode = request.POST.get("plancode", "").strip()
                planname = request.POST.get("planname", "").strip()
                if not plancode or not planname:
                    messages.error(request, "Plan code and name are required.")
                elif SubscriptionPlanTable.objects.filter(plancode=plancode).exclude(id=plan.id).exists():
                    messages.error(request, "Another plan with this code already exists.")
                else:
                    plan.plancode = plancode
                    plan.planname = planname
                    plan.subscribertype = int(request.POST.get("subscribertype", plan.subscribertype))
                    plan.billingfrequency = int(request.POST.get("billingfrequency", plan.billingfrequency))
                    plan.price = request.POST.get("price") or plan.price
                    plan.currencycode = request.POST.get("currencycode", plan.currencycode) or "ZAR"
                    plan.maximummembers = _optional_int(request.POST.get("maximummembers"))
                    plan.maximumevents = _optional_int(request.POST.get("maximumevents"))
                    plan.isactive = request.POST.get("isactive") == "true"
                    plan.save()
                    messages.success(request, "Subscription plan updated.")

        elif action == "delete_plan":
            plan = SubscriptionPlanTable.objects.filter(id=request.POST.get("plan_id")).first()
            if not plan:
                messages.error(request, "Subscription plan not found.")
            else:
                try:
                    plan.delete()
                    messages.success(request, "Subscription plan deleted.")
                except Exception:
                    messages.error(request, "Cannot delete plan while subscriptions reference it.")

        elif action == "add_subscription":
            plan_id = request.POST.get("subscriptionplan")
            start_date = request.POST.get("subscriptionstartdate")
            if not plan_id or not start_date:
                messages.error(request, "Plan and start date are required.")
            else:
                participant_id = request.POST.get("participant") or None
                org_id = request.POST.get("athleticorganisation") or None
                SubscriptionTable.objects.create(
                    subscriptionplan_id=plan_id,
                    participant_id=participant_id,
                    athleticorganisation_id=org_id,
                    subscriptionstartdate=start_date,
                    subscriptionenddate=request.POST.get("subscriptionenddate") or None,
                    nextbillingdate=request.POST.get("nextbillingdate") or None,
                    subscriptionstatus=int(
                        request.POST.get("subscriptionstatus", SubscriptionStatus.Pending)
                    ),
                    autorenew=request.POST.get("autorenew") == "true",
                    externalcustomerid=request.POST.get("externalcustomerid") or None,
                    externalpaymentid=request.POST.get("externalpaymentid") or None,
                )
                messages.success(request, "Subscription added.")

        elif action == "edit_subscription":
            subscription = SubscriptionTable.objects.filter(
                id=request.POST.get("subscription_id"),
            ).first()
            if not subscription:
                messages.error(request, "Subscription not found.")
            elif not request.POST.get("subscriptionstartdate"):
                messages.error(request, "Start date is required.")
            else:
                subscription.subscriptionplan_id = request.POST.get(
                    "subscriptionplan", subscription.subscriptionplan_id,
                )
                subscription.participant_id = request.POST.get("participant") or None
                subscription.athleticorganisation_id = request.POST.get("athleticorganisation") or None
                subscription.subscriptionstartdate = request.POST.get("subscriptionstartdate")
                subscription.subscriptionenddate = request.POST.get("subscriptionenddate") or None
                subscription.nextbillingdate = request.POST.get("nextbillingdate") or None
                subscription.subscriptionstatus = int(
                    request.POST.get("subscriptionstatus", subscription.subscriptionstatus),
                )
                subscription.autorenew = request.POST.get("autorenew") == "true"
                subscription.externalcustomerid = request.POST.get("externalcustomerid") or None
                subscription.externalpaymentid = request.POST.get("externalpaymentid") or None
                subscription.save()
                messages.success(request, "Subscription updated.")

        elif action == "delete_subscription":
            subscription = SubscriptionTable.objects.filter(
                id=request.POST.get("subscription_id"),
            ).first()
            if subscription:
                subscription.delete()
                messages.success(request, "Subscription deleted.")
            else:
                messages.error(request, "Subscription not found.")

        elif action == "add_app_release_version":
            release_version = request.POST.get("releaseVersionNumber", "").strip()
            if not release_version:
                messages.error(request, "Release version number is required.")
            elif AppReleaseVersionTable.objects.filter(
                releaseVersionNumber=release_version,
            ).exists():
                messages.error(request, "This release version number already exists.")
            else:
                AppReleaseVersionTable.objects.create(
                    releaseVersionNumber=release_version,
                    optionUpgradeVersionNumber=request.POST.get(
                        "optionUpgradeVersionNumber", "",
                    ).strip() or None,
                    mandatoryUpgradeVersionNumber=request.POST.get(
                        "mandatoryUpgradeVersionNumber", "",
                    ).strip() or None,
                )
                messages.success(request, "App release version added.")

        elif action == "edit_app_release_version":
            release = AppReleaseVersionTable.objects.filter(
                id=request.POST.get("release_id"),
            ).first()
            release_version = request.POST.get("releaseVersionNumber", "").strip()
            if not release:
                messages.error(request, "App release version not found.")
            elif not release_version:
                messages.error(request, "Release version number is required.")
            elif AppReleaseVersionTable.objects.filter(
                releaseVersionNumber=release_version,
            ).exclude(id=release.id).exists():
                messages.error(request, "Another record with this release version number already exists.")
            else:
                release.releaseVersionNumber = release_version
                release.optionUpgradeVersionNumber = request.POST.get(
                    "optionUpgradeVersionNumber", "",
                ).strip() or None
                release.mandatoryUpgradeVersionNumber = request.POST.get(
                    "mandatoryUpgradeVersionNumber", "",
                ).strip() or None
                release.save()
                messages.success(request, "App release version updated.")

        elif action == "delete_app_release_version":
            release = AppReleaseVersionTable.objects.filter(
                id=request.POST.get("release_id"),
            ).first()
            if release:
                release.delete()
                messages.success(request, "App release version deleted.")
            else:
                messages.error(request, "App release version not found.")

        elif action == "add_terms":
            document_type = request.POST.get("document_type", "app").strip() or "app"
            version_number = request.POST.get("version_number", "").strip()
            title = request.POST.get("title", "").strip()
            content = request.POST.get("content", "").strip()
            if not version_number or not title or not content:
                messages.error(request, "Version number, title, and content are required.")
            elif TermsAndConditionsTable.objects.filter(
                document_type=document_type,
                version_number=version_number,
            ).exists():
                messages.error(request, "This document type and version number already exists.")
            else:
                effective_from_raw = request.POST.get("effective_from", "").strip()
                TermsAndConditionsTable.objects.create(
                    document_type=document_type,
                    version_number=version_number,
                    title=title,
                    content=content,
                    effective_from=parse_datetime(effective_from_raw) if effective_from_raw else None,
                    is_current=request.POST.get("is_current") == "true",
                )
                messages.success(request, "Terms and conditions version added.")

        elif action == "edit_terms":
            terms = TermsAndConditionsTable.objects.filter(id=request.POST.get("terms_id")).first()
            document_type = request.POST.get("document_type", "app").strip() or "app"
            version_number = request.POST.get("version_number", "").strip()
            title = request.POST.get("title", "").strip()
            content = request.POST.get("content", "").strip()
            if not terms:
                messages.error(request, "Terms and conditions record not found.")
            elif not version_number or not title or not content:
                messages.error(request, "Version number, title, and content are required.")
            elif TermsAndConditionsTable.objects.filter(
                document_type=document_type,
                version_number=version_number,
            ).exclude(id=terms.id).exists():
                messages.error(request, "Another record with this document type and version already exists.")
            else:
                effective_from_raw = request.POST.get("effective_from", "").strip()
                terms.document_type = document_type
                terms.version_number = version_number
                terms.title = title
                terms.content = content
                terms.effective_from = parse_datetime(effective_from_raw) if effective_from_raw else None
                terms.is_current = request.POST.get("is_current") == "true"
                terms.save()
                messages.success(request, "Terms and conditions updated.")

        elif action == "delete_terms":
            terms = TermsAndConditionsTable.objects.filter(id=request.POST.get("terms_id")).first()
            if not terms:
                messages.error(request, "Terms and conditions record not found.")
            else:
                try:
                    terms.delete()
                    messages.success(request, "Terms and conditions deleted.")
                except ProtectedError:
                    messages.error(
                        request,
                        "Cannot delete this version because participants have already accepted it.",
                    )

        section = _administrator_section_for_action(action)
        return redirect(f"{reverse('administrator')}?section={section}")

    valid_sections = {
        "event-categories",
        "subscription-plans",
        "subscriptions",
        "app-release-versions",
        "terms-and-conditions",
    }
    active_section = request.GET.get("section", "event-categories")
    if active_section not in valid_sections:
        active_section = "event-categories"

    return render(
        request,
        "website/administrator.html",
        {
            "active_section": active_section,
            "event_categories": EventCategoryTable.objects.all().order_by("categoryname"),
            "subscription_plans": SubscriptionPlanTable.objects.all().order_by("planname"),
            "subscriptions": SubscriptionTable.objects.select_related(
                "subscriptionplan", "participant", "athleticorganisation",
            ).order_by("-subscriptionstartdate"),
            "subscriber_types": SubscriberType.choices(),
            "billing_frequencies": BillingFrequency.choices(),
            "subscription_statuses": SubscriptionStatus.choices(),
            "participants": ParticipantTable.objects.all().order_by("surname", "firstname"),
            "athletic_organisations": AthleticOrganisationTable.objects.all().order_by("name"),
            "app_release_versions": AppReleaseVersionTable.objects.all().order_by("-created"),
            "terms_and_conditions": TermsAndConditionsTable.objects.all().order_by("-created"),
        },
    )


@login_required
def events(request):
    event_list = EventDetailTable.objects.only(
        'id', 'eventname', 'eventdate', 'eventenddate', 'eventstatus',
        'eventtype', 'contactpersonname', 'contactpersonemailaddr',
    ).order_by('-eventdate')

    filter_statuses = {
        'upcoming': [EventStatus.RegistrationOpen, EventStatus.RegistrationClosed],
        'past': [EventStatus.Completed, EventStatus.Closed],
        'new-planning': [EventStatus.Created, EventStatus.Planning],
    }
    filter_labels = {
        'all': 'All Events',
        'upcoming': 'Upcoming',
        'past': 'Past',
        'new-planning': 'New & Planning',
    }
    filter_descriptions = {
        'all': 'Browse and manage all events. Newest events are shown first.',
        'upcoming': 'Events with registration open or closed.',
        'past': 'Completed and closed events.',
        'new-planning': 'Events that are newly created or in planning.',
    }

    active_filter = request.GET.get('filter', 'upcoming')
    if active_filter not in filter_labels:
        active_filter = 'all'

    if active_filter in filter_statuses:
        event_list = event_list.filter(
            eventstatus__in=[status.value for status in filter_statuses[active_filter]],
        )

    return render(
        request,
        'website/events.html',
        {
            'events': event_list,
            'active_filter': active_filter,
            'filter_labels': filter_labels,
            'filter_descriptions': filter_descriptions,
            'filter_title': filter_labels[active_filter],
            'filter_description': filter_descriptions[active_filter],
        },
    )

@login_required
def organisations(request):
    organisations = OrganisationTable.objects.all().order_by('-created')
    return render(
        request,
        'website/organisations.html',
        {
            'organisations': organisations,
        }
    )


@login_required
@require_http_methods(["GET", "POST"])
def athletic_associations(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_root":
            category_id = request.POST.get("athleticscategory")
            name = request.POST.get("name", "").strip()
            if not name or not category_id:
                messages.error(request, "Name and athletics category are required.")
            else:
                AthleticAssociationTable.add_root(
                    name=name,
                    description=request.POST.get("description", ""),
                    registrationnumber=request.POST.get("registrationnumber") or None,
                    athleticscategory_id=category_id,
                )
                messages.success(request, "Root athletic association added.")

        elif action == "add_child":
            parent_id = request.POST.get("parent_id")
            name = request.POST.get("name", "").strip()
            parent = AthleticAssociationTable.objects.filter(id=parent_id).first()
            if not parent:
                messages.error(request, "Parent association not found.")
            elif not name:
                messages.error(request, "Name is required.")
            else:
                parent.add_child(
                    name=name,
                    description=request.POST.get("description", ""),
                    registrationnumber=request.POST.get("registrationnumber") or None,
                    athleticscategory=parent.athleticscategory,
                )
                messages.success(request, "Child athletic association added.")

        elif action == "edit":
            association_id = request.POST.get("association_id")
            name = request.POST.get("name", "").strip()
            association = AthleticAssociationTable.objects.filter(id=association_id).first()
            if not association:
                messages.error(request, "Athletic association not found.")
            elif not name:
                messages.error(request, "Name is required.")
            else:
                parent = association.get_parent()
                association.name = name
                association.description = request.POST.get("description", "")
                association.registrationnumber = request.POST.get("registrationnumber") or None
                if parent is None:
                    category_id = request.POST.get("athleticscategory")
                    if not category_id:
                        messages.error(request, "Athletics category is required for root associations.")
                        return redirect("athletic_associations")
                    association.athleticscategory_id = category_id
                association.save()
                if parent is None:
                    association.get_descendants().update(
                        athleticscategory_id=association.athleticscategory_id
                    )
                messages.success(request, "Athletic association updated.")

        elif action == "delete":
            association_id = request.POST.get("association_id")
            association = AthleticAssociationTable.objects.filter(id=association_id).first()
            if association:
                association.delete()
                messages.success(request, "Athletic association deleted.")
            else:
                messages.error(request, "Athletic association not found.")

        return redirect("athletic_associations")

    associations = AthleticAssociationTable.get_tree().select_related("athleticscategory")
    categories = AthleticsCategoryTable.objects.all().order_by("name")

    return render(
        request,
        "website/athletic-associations.html",
        {
            "associations": associations,
            "categories": categories,
        },
    )


def _build_athletic_organisation_tree():
    def build_node(organisation):
        return {
            'organisation': organisation,
            'children': [
                build_node(child)
                for child in organisation.get_children().order_by('name')
            ],
        }

    return [
        build_node(root)
        for root in AthleticOrganisationTable.get_root_nodes().order_by('name')
    ]


@login_required
@require_http_methods(["GET", "POST"])
def athletic_organisations(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_root":
            kwargs = _athletic_organisation_kwargs(request.POST)
            missing = _validate_athletic_organisation_required_fields(kwargs)
            if missing:
                messages.error(request, f"Required fields missing: {', '.join(missing)}.")
            elif AthleticOrganisationTable.objects.filter(code=kwargs["code"]).exists():
                messages.error(request, "An organisation with this code already exists.")
            else:
                AthleticOrganisationTable.add_root(**kwargs)
                messages.success(request, "Root athletic organisation added.")

        elif action == "add_child":
            parent_id = request.POST.get("parent_id")
            parent = AthleticOrganisationTable.objects.filter(id=parent_id).first()
            kwargs = _athletic_organisation_kwargs(request.POST)
            missing = _validate_athletic_organisation_required_fields(kwargs)
            if not parent:
                messages.error(request, "Parent organisation not found.")
            elif missing:
                messages.error(request, f"Required fields missing: {', '.join(missing)}.")
            elif AthleticOrganisationTable.objects.filter(code=kwargs["code"]).exists():
                messages.error(request, "An organisation with this code already exists.")
            else:
                parent.add_child(**kwargs)
                messages.success(request, "Child athletic organisation added.")

        elif action == "edit":
            organisation_id = request.POST.get("organisation_id")
            organisation = AthleticOrganisationTable.objects.filter(id=organisation_id).first()
            if not organisation:
                messages.error(request, "Athletic organisation not found.")
            elif not request.POST.get("name", "").strip():
                messages.error(request, "Name is required.")
            else:
                new_code = request.POST.get("code", "").strip()
                if new_code and new_code != organisation.code:
                    if AthleticOrganisationTable.objects.filter(code=new_code).exclude(id=organisation.id).exists():
                        messages.error(request, "An organisation with this code already exists.")
                        return redirect("athletic_organisations")
                    organisation.code = new_code
                _update_athletic_organisation_fields(organisation, request.POST)
                messages.success(request, "Athletic organisation updated.")

        elif action == "move":
            organisation_id = request.POST.get("organisation_id")
            target_parent_id = request.POST.get("target_parent_id")
            position = request.POST.get("position", "sorted-child")
            organisation = AthleticOrganisationTable.objects.filter(id=organisation_id).first()
            if not organisation:
                messages.error(request, "Athletic organisation not found.")
            else:
                target_parent = None
                if target_parent_id:
                    target_parent = AthleticOrganisationTable.objects.filter(id=target_parent_id).first()
                    if not target_parent:
                        messages.error(request, "Target parent organisation not found.")
                        return redirect("athletic_organisations")
                try:
                    _move_athletic_organisation(organisation, target_parent, position)
                    messages.success(request, "Athletic organisation moved.")
                except ValueError as exc:
                    messages.error(request, str(exc))

        elif action == "delete":
            organisation_id = request.POST.get("organisation_id")
            organisation = AthleticOrganisationTable.objects.filter(id=organisation_id).first()
            if organisation:
                organisation.delete()
                messages.success(request, "Athletic organisation deleted.")
            else:
                messages.error(request, "Athletic organisation not found.")

        return redirect("athletic_organisations")

    organisations = AthleticOrganisationTable.get_tree()
    move_targets = AthleticOrganisationTable.objects.all().order_by("name")

    return render(
        request,
        "website/athletic-organisations.html",
        {
            "organisations": organisations,
            "organisation_tree": _build_athletic_organisation_tree(),
            "organisation_types": OrganisationType.choices(),
            "move_positions": [
                ("sorted-child", "Sorted child"),
                ("first-child", "First child"),
                ("last-child", "Last child"),
                ("left", "Left sibling"),
                ("right", "Right sibling"),
            ],
            "move_targets": move_targets,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def athletic_organisation_details(request, id):
    organisation = get_object_or_404(AthleticOrganisationTable, id=id)
    parent = organisation.get_parent()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_organisation":
            new_code = request.POST.get("code", "").strip()
            if not new_code or not request.POST.get("name", "").strip():
                messages.error(request, "Code and name are required.")
            elif (
                new_code != organisation.code
                and AthleticOrganisationTable.objects.filter(code=new_code).exclude(id=organisation.id).exists()
            ):
                messages.error(request, "An organisation with this code already exists.")
            else:
                organisation.code = new_code
                _update_athletic_organisation_fields(organisation, request.POST)
                if request.FILES.get("logo"):
                    organisation.logo = request.FILES["logo"]
                if request.FILES.get("banner"):
                    organisation.banner = request.FILES["banner"]
                organisation.save()
                messages.success(request, "Athletic organisation updated.")

        elif action == "add_member":
            participant_id = request.POST.get("participant")
            if not participant_id:
                messages.error(request, "Please select a participant.")
            elif AthleticOrganisationMemberTable.objects.filter(
                athleticorganisation=organisation,
                participant_id=participant_id,
            ).exists():
                messages.error(request, "This participant is already a member.")
            else:
                membershipstartdate = request.POST.get("membershipstartdate") or None
                membershipenddate = request.POST.get("membershipenddate") or None
                AthleticOrganisationMemberTable.objects.create(
                    athleticorganisation=organisation,
                    participant_id=participant_id,
                    membershipnumber=request.POST.get("membershipnumber") or None,
                    membershiptype=request.POST.get("membershiptype") or None,
                    role=int(request.POST.get("role", OrganisationMemberRole.Member)),
                    status=int(request.POST.get("status", OrganisationMemberStatus.Pending)),
                    membershipstartdate=membershipstartdate,
                    membershipenddate=membershipenddate,
                    isprimary=_coerce_bool(request.POST.get("isprimary")) or False,
                )
                messages.success(request, "Member added.")

        elif action == "remove_member":
            member_id = request.POST.get("member_id")
            deleted, _ = AthleticOrganisationMemberTable.objects.filter(
                id=member_id,
                athleticorganisation=organisation,
            ).delete()
            if deleted:
                messages.success(request, "Member removed.")
            else:
                messages.error(request, "Member not found.")

        elif action == "edit_member":
            member_id = request.POST.get("member_id")
            member = AthleticOrganisationMemberTable.objects.filter(
                id=member_id,
                athleticorganisation=organisation,
            ).first()
            if not member:
                messages.error(request, "Member not found.")
            else:
                member.membershipnumber = request.POST.get("membershipnumber") or None
                member.membershiptype = request.POST.get("membershiptype") or None
                member.role = int(request.POST.get("role", member.role))
                member.status = int(request.POST.get("status", member.status))
                member.membershipstartdate = request.POST.get("membershipstartdate") or None
                member.membershipenddate = request.POST.get("membershipenddate") or None
                member.isprimary = _coerce_bool(request.POST.get("isprimary")) or False
                member.save()
                messages.success(request, "Member updated.")

        elif action == "add_category":
            category_id = request.POST.get("athleticscategory")
            if not category_id:
                messages.error(request, "Please select an athletics category.")
            elif AthleticOrganisationCategoryTable.objects.filter(
                athleticorganisation=organisation,
                athleticscategory_id=category_id,
            ).exists():
                messages.error(request, "This category is already linked.")
            else:
                isprimary = _coerce_bool(request.POST.get("isprimary")) or False
                if isprimary:
                    AthleticOrganisationCategoryTable.objects.filter(
                        athleticorganisation=organisation,
                    ).update(isprimary=False)
                AthleticOrganisationCategoryTable.objects.create(
                    athleticorganisation=organisation,
                    athleticscategory_id=category_id,
                    isprimary=isprimary,
                    isactive=bool(request.POST.get("isactive")),
                )
                messages.success(request, "Athletics category added.")

        elif action == "remove_category":
            category_link_id = request.POST.get("category_link_id")
            deleted, _ = AthleticOrganisationCategoryTable.objects.filter(
                id=category_link_id,
                athleticorganisation=organisation,
            ).delete()
            if deleted:
                messages.success(request, "Athletics category removed.")
            else:
                messages.error(request, "Category link not found.")

        elif action == "edit_category":
            category_link_id = request.POST.get("category_link_id")
            category_link = AthleticOrganisationCategoryTable.objects.filter(
                id=category_link_id,
                athleticorganisation=organisation,
            ).first()
            if not category_link:
                messages.error(request, "Category link not found.")
            else:
                isprimary = _coerce_bool(request.POST.get("isprimary")) or False
                if isprimary:
                    AthleticOrganisationCategoryTable.objects.filter(
                        athleticorganisation=organisation,
                    ).exclude(id=category_link.id).update(isprimary=False)
                category_link.isprimary = isprimary
                category_link.isactive = bool(request.POST.get("isactive"))
                category_link.save()
                messages.success(request, "Athletics category updated.")

        return redirect("athletic_organisation_details", id=organisation.id)

    organisation_members = AthleticOrganisationMemberTable.objects.filter(
        athleticorganisation=organisation,
    ).select_related("participant").order_by("-created")
    organisation_categories = AthleticOrganisationCategoryTable.objects.filter(
        athleticorganisation=organisation,
    ).select_related("athleticscategory").order_by("-isprimary", "athleticscategory__name")

    member_participant_ids = organisation_members.values_list("participant_id", flat=True)
    linked_category_ids = organisation_categories.values_list("athleticscategory_id", flat=True)

    return render(
        request,
        "website/athletic-organisation-details.html",
        {
            "organisation": organisation,
            "parent": parent,
            "organisation_members": organisation_members,
            "organisation_categories": organisation_categories,
            "available_participants": ParticipantTable.objects.exclude(
                id__in=member_participant_ids,
            ).order_by("surname", "firstname"),
            "available_categories": AthleticsCategoryTable.objects.exclude(
                id__in=linked_category_ids,
            ).order_by("name"),
            "member_roles": OrganisationMemberRole.choices(),
            "member_statuses": OrganisationMemberStatus.choices(),
            "organisation_types": OrganisationType.choices(),
        },
    )


def _coerce_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    return str(value).lower() in ("1", "true", "yes", "on")


@login_required
@require_http_methods(["GET", "POST"])
def organisation_details(request, id):
    organisation = get_object_or_404(
        OrganisationTable.objects.select_related(
            "athleticassociation",
            "athleticassociation__athleticscategory",
        ),
        id=id,
    )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_athletic_association":
            association_id = request.POST.get("athleticassociation")
            if association_id:
                association = AthleticAssociationTable.objects.filter(id=association_id).first()
                if not association:
                    messages.error(request, "Athletic association not found.")
                else:
                    organisation.athleticassociation = association
                    organisation.save(update_fields=["athleticassociation"])
                    messages.success(request, "Athletic association updated.")
            else:
                organisation.athleticassociation = None
                organisation.save(update_fields=["athleticassociation"])
                messages.success(request, "Athletic association removed.")

        elif action == "add_member":
            participant_id = request.POST.get("participant")
            if not participant_id:
                messages.error(request, "Please select a participant.")
            elif OrganisationMemberTable.objects.filter(organisation=organisation, participant_id=participant_id).exists():
                messages.error(request, "This participant is already an organisation member.")
            else:
                OrganisationMemberTable.objects.create(
                    organisation=organisation,
                    participant_id=participant_id,
                    role=int(request.POST.get("role", OrganisationMemberRole.Member)),
                    status=int(request.POST.get("status", OrganisationMemberStatus.Pending)),
                )
                messages.success(request, "Organisation member added.")

        elif action == "remove_member":
            member_id = request.POST.get("member_id")
            deleted, _ = OrganisationMemberTable.objects.filter(
                id=member_id, organisation=organisation
            ).delete()
            if deleted:
                messages.success(request, "Organisation member removed.")
            else:
                messages.error(request, "Organisation member not found.")

        elif action == "edit_member":
            member_id = request.POST.get("member_id")
            member = OrganisationMemberTable.objects.filter(
                id=member_id, organisation=organisation
            ).first()
            if not member:
                messages.error(request, "Organisation member not found.")
            else:
                member.role = int(request.POST.get("role", member.role))
                member.status = int(request.POST.get("status", member.status))
                member.save()
                messages.success(request, "Organisation member updated.")

        elif action == "add_event":
            event_id = request.POST.get("event")
            if not event_id:
                messages.error(request, "Please select an event.")
            else:
                event = EventDetailTable.objects.filter(id=event_id).first()
                if not event:
                    messages.error(request, "Event not found.")
                elif event.organisation_id == organisation.id:
                    messages.error(request, "This event is already linked to the organisation.")
                else:
                    event.organisation = organisation
                    event.save(update_fields=["organisation"])
                    messages.success(request, "Event linked to organisation.")

        elif action == "remove_event":
            event_id = request.POST.get("event_id")
            event = EventDetailTable.objects.filter(
                id=event_id, organisation=organisation
            ).first()
            if event:
                event.organisation = None
                event.save(update_fields=["organisation"])
                messages.success(request, "Event removed from organisation.")
            else:
                messages.error(request, "Event not found for this organisation.")

        return redirect("organisation_details", id=organisation.id)

    organisation_members = OrganisationMemberTable.objects.filter(
        organisation=organisation
    ).select_related("participant").order_by("-created")
    organisation_events = EventDetailTable.objects.filter(
        organisation=organisation
    ).order_by("eventdate")

    member_participant_ids = organisation_members.values_list("participant_id", flat=True)

    return render(
        request,
        "website/organisation-details.html",
        {
            "organisation": organisation,
            "organisation_members": organisation_members,
            "organisation_events": organisation_events,
            "available_participants": ParticipantTable.objects.exclude(
                id__in=member_participant_ids
            ).order_by("surname", "firstname"),
            "available_events": EventDetailTable.objects.exclude(
                organisation=organisation
            ).order_by("-eventdate"),
            "member_roles": OrganisationMemberRole.choices(),
            "member_statuses": OrganisationMemberStatus.choices(),
            "athletic_associations": AthleticAssociationTable.get_tree().select_related(
                "athleticscategory"
            ),
        },
    )

@login_required
def new_event(request):
    return redirect("event_create")
    
@login_required
def event_details(request, id):
    event = get_object_or_404(
        EventDetailTable.objects.select_related(
            'organisation', 'athleticorganisation', 'athleticscategory',
        ),
        id=id,
    )

    event_image = EventImages.objects.filter(event=event).first()
    sponsors = EventSponsorTable.objects.filter(event=event).order_by("id")
    information_items = EventInformationTable.objects.filter(event=event).order_by("name")
    notifications = EventNotificationTable.objects.filter(event=event).order_by("-created")
    subevents = event.subevent_event.select_related("eventcategory").order_by("displaysequence", "name")

    subevents_by_category = {}
    for subevent in subevents:
        subevents_by_category.setdefault(subevent.eventcategory_id, []).append(subevent)

    event_categories = EventCategoryTable.objects.filter(
        id__in=subevents_by_category.keys(),
    ).order_by("categoryname")

    category_blocks = [
        {
            'category': category,
            'subevents': subevents_by_category.get(category.id, []),
        }
        for category in event_categories
    ]

    participant_events = ParticipantEventTable.objects.filter(event=event).select_related(
        'participant', 'subevent', 'paymref', 'subevent__eventcategory',
    ).order_by('participant__surname', 'participant__firstname', 'subevent__name')

    valid_sections = {
        "details", "image", "sponsors", "categories", "information", "notifications", "participants",
    }
    active_section = request.GET.get("section", "details")
    if active_section not in valid_sections:
        active_section = "details"

    return render(
        request,
        "website/event-details.html",
        {
            "event": event,
            "event_image": event_image,
            "sponsors": sponsors,
            "information_items": information_items,
            "notifications": notifications,
            "category_blocks": category_blocks,
            "participant_events": participant_events,
            "event_statuses": EventStatus.choices(),
            "active_section": active_section,
            "event_id": event.id,
        },
    )

def _event_edit_section_for_action(action):
    section_map = {
        "create_event": "details",
        "update_event": "details",
        "update_event_image": "image",
        "add_sponsor": "sponsors",
        "edit_sponsor": "sponsors",
        "remove_sponsor": "sponsors",
        "add_information": "information",
        "edit_information": "information",
        "remove_information": "information",
        "add_category": "categories",
        "add_subevent": "categories",
        "edit_subevent": "categories",
        "remove_subevent": "categories",
        "add_notification": "notifications",
        "edit_notification": "notifications",
        "remove_notification": "notifications",
    }
    return section_map.get(action, "details")


def _populate_event_from_post(event, post):
    event.eventid = post.get("eventid", event.eventid or "")
    event.eventname = post.get("eventname", event.eventname or "")
    event.eventdate = post.get("eventdate") or event.eventdate
    event.eventenddate = post.get("eventenddate") or event.eventenddate
    event.eventstatus = int(post.get("eventstatus", event.eventstatus or EventStatus.Created))
    event.eventtype = post.get("eventtype", event.eventtype or "")
    event.eventcategory = post.get("eventcategory", event.eventcategory or "")
    event.eventdescription = post.get("eventdescription", event.eventdescription or "")
    event.contactpersonname = post.get("contactpersonname", event.contactpersonname or "")
    event.contactpersonsurname = post.get("contactpersonsurname", event.contactpersonsurname or "")
    event.contactpersonothername = post.get("contactpersonothername") or ""
    event.contactpersonemailaddr = post.get("contactpersonemailaddr") or ""
    event.contactpersonphonenum = post.get("contactpersonphonenum") or ""
    event.contactpersoncitizenship = post.get("contactpersoncitizenship") or ""
    event.contactpersonnationality = post.get("contactpersonnationality") or ""
    event.contactpersonprovince = post.get("contactpersonprovince") or ""
    event.contactpersoncountry = post.get("contactpersoncountry") or ""
    event.contactpersonaddrtype = post.get("contactpersonaddrtype") or ""
    event.contactpersonaddr1 = post.get("contactpersonaddr1") or ""
    event.contactpersonaddr2 = post.get("contactpersonaddr2") or ""
    event.contactpersonaddr3 = post.get("contactpersonaddr3") or ""
    event.contactpersonaddr4 = post.get("contactpersonaddr4") or ""
    event.contactpersonaddrcode = post.get("contactpersonaddrcode") or ""
    event.terminationstatus = post.get("terminationstatus") or ""
    event.startPointLat = post.get("startPointLat") or None
    event.startPointLng = post.get("startPointLng") or None
    event.parkinglat = post.get("parkinglat") or None
    event.parkinglng = post.get("parkinglng") or None
    event.allowregistration = bool(post.get("allowregistration"))
    event.venuename = post.get("venuename") or None
    event.sanctionstatus = post.get("sanctionstatus") or "UNREGISTERED"
    event.sanctionreference = post.get("sanctionreference") or None
    max_participants = post.get("maximumparticipants")
    event.maximumparticipants = int(max_participants) if max_participants else None
    event.isactive = bool(post.get("isactive"))
    registration_open = post.get("registrationopendate")
    event.registrationopendate = parse_datetime(registration_open) if registration_open else None
    registration_close = post.get("registrationclosedate")
    event.registrationclosedate = parse_datetime(registration_close) if registration_close else None
    org_id = post.get("organisation")
    if org_id:
        event.organisation_id = org_id
    event.athleticorganisation_id = post.get("athleticorganisation") or None
    event.athleticscategory_id = post.get("athleticscategory") or None
    return event


def _build_event_edit_context(event, request, is_new=False):
    event_image = None if is_new else EventImages.objects.filter(event=event).first()
    sponsors = [] if is_new else EventSponsorTable.objects.filter(event=event).order_by("id")
    information_items = [] if is_new else EventInformationTable.objects.filter(event=event).order_by("name")
    notifications = [] if is_new else EventNotificationTable.objects.filter(event=event).order_by("-created")
    subevents = [] if is_new else event.subevent_event.select_related("eventcategory").order_by("displaysequence", "name")

    subevents_by_category = {}
    for subevent in subevents:
        subevents_by_category.setdefault(subevent.eventcategory_id, []).append(subevent)

    event_categories = EventCategoryTable.objects.filter(
        id__in=subevents_by_category.keys(),
    ).order_by("categoryname")
    all_categories = EventCategoryTable.objects.all().order_by("categoryname")

    category_blocks = [
        {
            'category': category,
            'subevents': subevents_by_category.get(category.id, []),
        }
        for category in event_categories
    ]

    valid_sections = {
        "details", "image", "sponsors", "information", "categories", "notifications",
    }
    active_section = request.GET.get("section", "details")
    if is_new and active_section != "details":
        active_section = "details"
    elif active_section not in valid_sections:
        active_section = "details"

    return {
        "event": event,
        "event_image": event_image,
        "sponsors": sponsors,
        "information_items": information_items,
        "notifications": notifications,
        "all_categories": all_categories,
        "category_blocks": category_blocks,
        "subevents": subevents,
        "active_section": active_section,
        "is_new": is_new,
        "event_statuses": new_event_status_choices() if is_new else EventStatus.choices(),
        "sponsor_categories": SponsorCategory.choices(),
        "organisations": OrganisationTable.objects.all().order_by("name"),
        "athletic_organisations": AthleticOrganisationTable.get_tree(),
        "athletics_categories": AthleticsCategoryTable.objects.all().order_by("name"),
    }


@login_required
@require_http_methods(["GET", "POST"])
def event_create(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create_event":
            org_id = request.POST.get("organisation")
            eventid = request.POST.get("eventid", "").strip()
            eventname = request.POST.get("eventname", "").strip()
            if not org_id:
                messages.error(request, "Organisation is required.")
            elif not eventid or not eventname:
                messages.error(request, "Event ID and name are required.")
            elif not request.POST.get("eventdate") or not request.POST.get("eventenddate"):
                messages.error(request, "Event start and end dates are required.")
            elif EventDetailTable.objects.filter(eventid=eventid).exists():
                messages.error(request, "An event with this Event ID already exists.")
            elif not is_allowed_new_event_status(request.POST.get("eventstatus", EventStatus.Created)):
                messages.error(
                    request,
                    "Invalid event status. New events may only use Created, Planning, "
                    "RegistrationOpen, or RegistrationClosed.",
                )
            else:
                subscription_error = validate_club_can_create_event(
                    request.POST.get("athleticorganisation"),
                    event_status=request.POST.get("eventstatus"),
                )
                if subscription_error:
                    messages.error(request, subscription_error)
                else:
                    event = EventDetailTable(
                        contactpersonname="",
                        contactpersonsurname="",
                        eventdescription="",
                        eventtype="",
                        eventcategory="",
                    )
                    _populate_event_from_post(event, request.POST)
                    event.save()
                    messages.success(
                        request,
                        "Event created. You can now add image, sponsors, information, and subevents.",
                    )
                    return redirect(f"{reverse('event_details_edit', kwargs={'id': event.id})}?section=image")

        event = EventDetailTable(
            eventstatus=EventStatus.Created,
            contactpersonname="",
            contactpersonsurname="",
            eventdescription="",
            eventtype="",
            eventcategory="",
        )
        _populate_event_from_post(event, request.POST)
        return render(
            request,
            "website/event-details-edit.html",
            _build_event_edit_context(event, request, is_new=True),
        )

    event = EventDetailTable(
        eventstatus=EventStatus.Created,
        contactpersonname="",
        contactpersonsurname="",
        eventdescription="",
        eventtype="",
        eventcategory="",
    )
    return render(
        request,
        "website/event-details-edit.html",
        _build_event_edit_context(event, request, is_new=True),
    )


@login_required
@require_http_methods(["GET", "POST"])
def event_details_edit(request, id):
    event = get_object_or_404(
        EventDetailTable.objects.select_related(
            'organisation', 'athleticorganisation', 'athleticscategory',
        ),
        id=id,
    )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_event":
            subscription_error = validate_club_can_create_event(
                request.POST.get("athleticorganisation"),
                event_status=request.POST.get("eventstatus"),
                exclude_event_id=event.id,
            )
            if subscription_error:
                messages.error(request, subscription_error)
                _populate_event_from_post(event, request.POST)
                return render(
                    request,
                    "website/event-details-edit.html",
                    _build_event_edit_context(event, request, is_new=False),
                )
            _populate_event_from_post(event, request.POST)
            event.save()
            messages.success(request, "Event details updated.")

        elif action == "update_event_image":
            event_image, _ = EventImages.objects.get_or_create(event=event)
            if request.FILES.get("eventMainImg"):
                event_image.eventMainImg = request.FILES["eventMainImg"]
                event_image.save()
                messages.success(request, "Event image updated.")

        elif action == "add_sponsor":
            EventSponsorTable.objects.create(
                event=event,
                companyname=request.POST.get("companyname") or None,
                description=request.POST.get("description") or None,
                externallink=request.POST.get("externallink") or None,
                sponsorcategory=int(request.POST.get("sponsorcategory", SponsorCategory.notDefined)),
                sponsorImg=request.FILES.get("sponsorImg"),
            )
            messages.success(request, "Sponsor added.")

        elif action == "edit_sponsor":
            sponsor = EventSponsorTable.objects.filter(id=request.POST.get("sponsor_id"), event=event).first()
            if sponsor:
                sponsor.companyname = request.POST.get("companyname") or None
                sponsor.description = request.POST.get("description") or None
                sponsor.externallink = request.POST.get("externallink") or None
                sponsor.sponsorcategory = int(request.POST.get("sponsorcategory", sponsor.sponsorcategory))
                if request.FILES.get("sponsorImg"):
                    sponsor.sponsorImg = request.FILES["sponsorImg"]
                sponsor.save()
                messages.success(request, "Sponsor updated.")

        elif action == "remove_sponsor":
            deleted, _ = EventSponsorTable.objects.filter(id=request.POST.get("sponsor_id"), event=event).delete()
            messages.success(request, "Sponsor removed.") if deleted else messages.error(request, "Sponsor not found.")

        elif action == "add_information":
            EventInformationTable.objects.create(
                event=event,
                name=request.POST.get("name", ""),
                infoImg=request.FILES.get("infoImg"),
            )
            messages.success(request, "Information item added.")

        elif action == "edit_information":
            info = EventInformationTable.objects.filter(id=request.POST.get("information_id"), event=event).first()
            if info:
                info.name = request.POST.get("name", info.name)
                if request.FILES.get("infoImg"):
                    info.infoImg = request.FILES["infoImg"]
                info.save()
                messages.success(request, "Information item updated.")

        elif action == "remove_information":
            deleted, _ = EventInformationTable.objects.filter(id=request.POST.get("information_id"), event=event).delete()
            messages.success(request, "Information item removed.") if deleted else messages.error(request, "Item not found.")

        elif action == "add_category":
            name = request.POST.get("categoryname", "").strip()
            if not name:
                messages.error(request, "Category name is required.")
            elif EventCategoryTable.objects.filter(categoryname=name).exists():
                messages.error(request, "This category already exists.")
            else:
                EventCategoryTable.objects.create(categoryname=name)
                messages.success(request, "Event category added.")

        elif action == "add_subevent":
            category_id = request.POST.get("eventcategory")
            if not category_id:
                messages.error(request, "Please select a category.")
            else:
                EventSubDetailTable.objects.create(
                    event=event,
                    eventcategory_id=category_id,
                    name=request.POST.get("name", ""),
                    eventsubdate=request.POST.get("eventsubdate"),
                    regfees=request.POST.get("regfees") or 0,
                    regfeescurrency=request.POST.get("regfeescurrency", "ZAR"),
                    displaysequence=int(request.POST.get("displaysequence") or 0),
                    elevationImg=request.FILES.get("elevationImg"),
                )
                messages.success(request, "Subevent added.")

        elif action == "edit_subevent":
            subevent = EventSubDetailTable.objects.filter(id=request.POST.get("subevent_id"), event=event).first()
            if subevent:
                subevent.name = request.POST.get("name", subevent.name)
                subevent.eventcategory_id = request.POST.get("eventcategory", subevent.eventcategory_id)
                subevent.eventsubdate = request.POST.get("eventsubdate") or subevent.eventsubdate
                subevent.regfees = request.POST.get("regfees") or subevent.regfees
                subevent.regfeescurrency = request.POST.get("regfeescurrency", subevent.regfeescurrency)
                subevent.displaysequence = int(request.POST.get("displaysequence") or subevent.displaysequence)
                if request.FILES.get("elevationImg"):
                    subevent.elevationImg = request.FILES["elevationImg"]
                subevent.save()
                messages.success(request, "Subevent updated.")

        elif action == "remove_subevent":
            deleted, _ = EventSubDetailTable.objects.filter(id=request.POST.get("subevent_id"), event=event).delete()
            messages.success(request, "Subevent removed.") if deleted else messages.error(request, "Subevent not found.")

        elif action == "add_notification":
            EventNotificationTable.objects.create(
                event=event,
                title=request.POST.get("title") or None,
                message=request.POST.get("message") or None,
                notificationImg=request.FILES.get("notificationImg"),
                notificationPdf=request.FILES.get("notificationPdf"),
            )
            messages.success(request, "Notification added.")

        elif action == "edit_notification":
            notification = EventNotificationTable.objects.filter(
                id=request.POST.get("notification_id"), event=event,
            ).first()
            if notification:
                notification.title = request.POST.get("title") or None
                notification.message = request.POST.get("message") or None
                if request.FILES.get("notificationImg"):
                    notification.notificationImg = request.FILES["notificationImg"]
                if request.FILES.get("notificationPdf"):
                    notification.notificationPdf = request.FILES["notificationPdf"]
                notification.save()
                messages.success(request, "Notification updated.")

        elif action == "remove_notification":
            deleted, _ = EventNotificationTable.objects.filter(
                id=request.POST.get("notification_id"), event=event,
            ).delete()
            messages.success(request, "Notification removed.") if deleted else messages.error(request, "Notification not found.")

        section = _event_edit_section_for_action(action)
        return redirect(f"{reverse('event_details_edit', kwargs={'id': event.id})}?section={section}")

    return render(
        request,
        "website/event-details-edit.html",
        _build_event_edit_context(event, request, is_new=False),
    )

@login_required
def event_details_editpage(request, id):


    event = EventDetailTable.objects.get(
        id=id
    )

    subevents = event.subevent_event.all()
    subeventsSerializer = EventSubDetailSerializer(
        subevents,
        many=True
    )

    eventDetailSerializer = EventDetailSerializer(event , many=False) 

    return render(
        request,
        "website/event_details_edit_new.html",
        {
            "event": eventDetailSerializer.data,
            "sub_events": subeventsSerializer.data 
        }
    )

@login_required
def event_details_newpage(request):

    return render(
        request,
        "website/event_details_edit_new.html",
        {
            "event": None
        }
    )

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        return render(
            request,
            "website/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "website/login.html")

@login_required
def logout_view(request):

    logout(request)

    return redirect('/login')

@login_required
def participants(request):

    participants = ParticipantTable.objects.all()

    return render(
        request,
        "website/participants.html",
        {
            "participants": participants
        }
    )

@login_required
def participant_details(request, id):
    participant = get_object_or_404(
        ParticipantTable.objects.select_related('user').prefetch_related('events'),
        id=id,
    )

    return render(
        request,
        "website/participant-details.html",
        {
            "participant": participant,
        },
    )


def _populate_participant_from_post(participant, post, files=None):
    user_id = post.get("user")
    if user_id:
        participant.user_id = user_id

    participant.title = post.get("title") or None
    participant.surname = post.get("surname") or None
    participant.firstname = post.get("firstname") or None
    participant.othernames = post.get("othernames") or None
    participant.initials = post.get("initials") or None
    participant.preferredname = post.get("preferredname") or None
    participant.homelanguage = post.get("homelanguage") or None
    participant.preferredlanguage = post.get("preferredlanguage") or None
    participant.maidenname = post.get("maidenname") or None
    participant.countryofissue = post.get("countryofissue") or None
    participant.typefld = post.get("typefld") or None
    participant.disabled = bool(post.get("disabled"))
    participant.gender = int(post.get("gender", Gender.notDefined))
    participant.dateOfBirth = post.get("dateOfBirth") or None
    participant.emailaddress = post.get("emailaddress", participant.emailaddress or "")
    participant.usrphonenum = post.get("usrphonenum") or None
    participant.authid = post.get("authid", participant.authid or "")
    participant.identitynumber = post.get("identitynumber") or None
    participant.passportnumber = post.get("passportnumber") or None
    participant.nationalitycode = post.get("nationalitycode") or None
    participant.emergencycontactname = post.get("emergencycontactname") or None
    participant.emergencycontactphone = post.get("emergencycontactphone") or None
    participant.isverified = bool(post.get("isverified"))
    participant.isactive = bool(post.get("isactive"))

    if files and files.get("profilepic"):
        participant.profilepic = files["profilepic"]

    return participant


@login_required
@require_http_methods(["GET", "POST"])
def participant_details_edit(request, id):
    participant = get_object_or_404(
        ParticipantTable.objects.select_related('user').prefetch_related('events'),
        id=id,
    )

    if request.method == "POST":
        email = request.POST.get("emailaddress", "").strip()
        authid = request.POST.get("authid", "").strip()
        user_id = request.POST.get("user")

        if not user_id:
            messages.error(request, "User is required.")
        elif not email:
            messages.error(request, "Email address is required.")
        elif not authid:
            messages.error(request, "Auth ID is required.")
        elif ParticipantTable.objects.filter(emailaddress=email).exclude(pk=participant.pk).exists():
            messages.error(request, "A participant with this email address already exists.")
        else:
            _populate_participant_from_post(participant, request.POST, request.FILES)
            participant.save()
            participant.events.set(request.POST.getlist("events"))
            messages.success(request, "Participant updated successfully.")
            return redirect("participant_details", id=participant.id)

        _populate_participant_from_post(participant, request.POST, request.FILES)

    selected_event_ids = set(participant.events.values_list("id", flat=True))

    return render(
        request,
        "website/participant-details-edit.html",
        {
            "participant": participant,
            "users": User.objects.order_by("username"),
            "genders": Gender.choices(),
            "events": EventDetailTable.objects.order_by("-eventdate", "eventname"),
            "selected_event_ids": selected_event_ids,
        },
    )


@login_required
def event_participants(request, id):

    return render(
        request,
        "website/event-participants.html",
        {
            "event_id": id
        }
    )

@login_required
def whoami(request):
    return JsonResponse({
        "authenticated": request.user.is_authenticated,
        "username": request.user.username if request.user.is_authenticated else None
    })