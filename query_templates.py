from queries import Queries


def get_template(template_type, keywords_dict):
    queries = Queries()
    try:
        character = keywords_dict['CHARACTER']
    except KeyError:
        character = None
    try:
        place = keywords_dict['PLACE']
    except KeyError:
        place = None
    try:
        loyalty = keywords_dict['LOYALTY']
    except KeyError:
        loyalty = None
    try:
        gender = keywords_dict['GENDER']
    except KeyError:
        gender = None
    try:
        fictional = keywords_dict['FICTIONAL']
    except KeyError:
        fictional = None
    try:
        event = keywords_dict['EVENT']
    except KeyError:
        event = None
    try:
        chapter = keywords_dict['CHAPTER']
    except KeyError:
        chapter = None
    try:
        time = keywords_dict['TIME']
    except KeyError:
        time = None

    if template_type == 'BIRTHPLACE':
        queries.birthplace(character, place)
    elif template_type == 'LOYALTY':
        queries.loyalty(character, loyalty)
    elif template_type == 'LIFESPAN':
        queries.lifespan(character)
    elif template_type == 'GENDER':
        queries.gender(character, gender)
    elif template_type == 'CHARACTER_INFO':
        queries.about_character(character)
    elif template_type == 'CHAPTER':
        queries.which_chapter(event, chapter)
    elif template_type == 'EVENT_INFO':
        queries.event_info(event)
    elif template_type == 'EVENT_HISTORY':
        queries.event_history(event)
    elif template_type == 'EVENT_LOCATION':
        queries.event_location(event, place)
    elif template_type == 'EVENT_DATE':
        queries.event_time(event, time)
    elif template_type == 'EVENT_INVOLVED':
        queries.event_involved(event, character)
