from django_hosts import host
from django_hosts import patterns


host_patterns = patterns(
    "",
    host("", "test_project.urls", name="default"),
    host("sub", "test_project.urls_sub", name="sub"),
)
