from django import template
from re import sub  # Регулярные выраженя

register = template.Library()  # если мы не зарегистрируем наши фильтры, то Django никогда не узнает, где именно
# их искать, и фильтры потеряются


@register.filter(name='censor')  # регистрируем наш фильтр под именем censor, чтоб django понимал,
# что это именно фильтр, а не простая функция
def censor(value, arg):
    no_censorship = str(value)
    curse_words = ['идиот', 'мудак', 'дурак']

    for word in curse_words:
        no_censorship = sub(word, str(arg), no_censorship)
    return no_censorship