import re

from .base import RegexFilth


class UrlFilth(RegexFilth):

    # This allows you to keep the domain
    keep_domain = False

    url_placeholder = r'URL'

    # this regular expression is convenient for captures the domain name
    # and the path separately, which is useful for keeping the domain name
    # but sanitizing the path altogether
    regex = re.compile(r'''
        (?P<domain>
            (https?:\/\/(www\.)?|www\.)          # protocol http://, etc
            [\-\w@:%\.\+~\#=]{2,256}\.[a-z]{2,6} # domain name
            /?                                   # can have a trailing slash
        )(?P<path>
            [\-\w@:%\+\.~\#?&/=]*                # rest of path, query, & hash
        )
    ''', re.VERBOSE)

    @property
    def placeholder(self):
        if self.keep_domain:
            return self.match.group('domain') + self.url_placeholder
        return self.url_placeholder