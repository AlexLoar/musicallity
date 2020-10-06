from config.settings.base import *

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('SECRET_KEY', default='iq8IaIwiuIEK37Pfr6rzIpRB6eEs6HqLIhfPcqPVADuAyCChaI5ZZpWO6It5npVi')
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"
