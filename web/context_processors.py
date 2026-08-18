PAGE_BACKGROUNDS = {
    'userhome': 'Website_Background.png',
    'home': 'Website_Background.png',
    'events': 'Website_Background_Female2.png',
    'event_create': 'Website_Background_Female2.png',
    'event_details': 'Website_Background_Female2.png',
    'event_details_edit': 'Website_Background_Female2.png',
    'event_details_editpage': 'Website_Background_Female2.png',
    'event_details_newpage': 'Website_Background_Female2.png',
    'event_participants': 'Website_Background_Female2.png',
    'new_event': 'Website_Background_Female2.png',
    'participants': 'Website_Background_Male.png',
    'participant_details': 'Website_Background_Male.png',
    'participant_details_edit': 'Website_Background_Male.png',
    'athletic_organisations': 'Website_Background_Male2_Coastal.png',
    'athletic_organisation_details': 'Website_Background_Male2_Coastal.png',
    'athletic_associations': 'Website_Background_Male2_Coastal.png',
    'organisations': 'Website_Background_Female_DB.png',
    'organisation_details': 'Website_Background_Female_DB.png',
    'administrator': 'Website_Background_Female_DB.png',
    'login': 'Website_Background_Male.png',
    'about': 'Website_Background_Male2_Coastal.png',
}

DEFAULT_BACKGROUND = 'Website_Background.png'


def page_background(request):
    url_name = getattr(getattr(request, 'resolver_match', None), 'url_name', None)
    filename = PAGE_BACKGROUNDS.get(url_name, DEFAULT_BACKGROUND)
    return {'page_background_image': f'website/images/{filename}'}
