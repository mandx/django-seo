import re

from django.core.urlresolvers import get_resolver, LocaleRegexURLResolver
from django.utils import translation


language_code_prefix_re = re.compile(r'^/([\w-]+)(/.*|$)')


def is_language_prefix_patterns_used():
    """
    Returns `True` if the `LocaleRegexURLResolver` is used
    at root level of the urlpatterns, else it returns `False`.
    """
    for url_pattern in get_resolver(None).url_patterns:
        if isinstance(url_pattern, LocaleRegexURLResolver):
            return True
    return False


def i18n_unprefix_path(path):
    if not is_language_prefix_patterns_used():
        return path

    language = translation.get_language_from_path(path)
    if not language:
        return path

    regex_match = language_code_prefix_re.match(path)
    if not regex_match:
        return path

    return regex_match.group(2)
