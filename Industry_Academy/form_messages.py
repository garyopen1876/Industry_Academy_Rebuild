from django.contrib import messages


def push_form_errors(request, form, error_dict):
    for field, error_list in error_dict.items():
        for error in error_list:
            if 'message' in error:
                messages.error(request, form.fields.get(field).label + '：' + error['message'])
            else:
                messages.info(request, form.fields.get(field).label+'：'+error)
