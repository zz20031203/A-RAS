# views.py
from django.shortcuts import render
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

def room(request, room_name):
    # 获取模板查找路径
    template_name = 'chat.html'
    try:
        template = get_template(template_name)
    except TemplateDoesNotExist:
        from django.conf import settings
        print("Template directories:", settings.TEMPLATES[0]['DIRS'])
        raise
    return render(request, template_name, {'room_name': room_name})

