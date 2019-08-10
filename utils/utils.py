def get_question_type(predicted_array):
    type_key = None
    for i in range(len(predicted_array)):
        if predicted_array[i] == 1:
            type_key = i

    question_type_dict = {
        0: 'BIRTHPLACE',
        1: 'LOYALTY',
        2: 'LIFESPAN',
        3: 'GENDER',
        4: 'CHARACTER_INFO',
        5: 'CHAPTER',
        6: 'EVENT_INFO',
        7: 'EVENT_HISTORY',
        8: 'EVENT_LOCATION',
        9: 'EVENT_DATE',
        10: 'EVENT_INVOLVED',
        11: 'FICTIONAL'
    }

    return question_type_dict[type_key]
