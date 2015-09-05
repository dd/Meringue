.. _quickstart:

.. role:: strike
        :class: strike


Быстрый старт
=============

Так как пакет развивается для личных нужд и пока ещё не вышло ни одной стабильной верии, все зависимости рекомендуется ставить исключительно последних версий, основная зависиомость это `Django <http://www.djangoproject.com>`_ - для текущей версии (|version|) требуется Django не ниже версии 1.7 (на самом деле точно сложно сказать какая версия нужна, логика очень простая  обновляй по возможности обновляй зависимости в проектах).


Установка Meringue
------------------

Установка производится с использованием популярного инструмента ``pip``::

    pip install meringue

Все сопуствиующие зависимости установятся автоматически.


Базовая настройка
-----------------

For a more detailed guide on how to configure django-admin-tools, please
consult :ref:`the configuration section <configuration>`.

Prerequisite
~~~~~~~~~~~~

In order to use django-admin-tools you obviously need to have configured
your Django admin site. If you didn't, please refer to the
`relevant django documentation <https://docs.djangoproject.com/en/dev/intro/tutorial02/>`_.

Configuration
~~~~~~~~~~~~~

First make sure you have the ``django.core.context_processors.request``
template context processor in your ``TEMPLATE_CONTEXT_PROCESSORS``.

.. note::
    Starting from django 1.8, ``TEMPLATE_CONTEXT_PROCESSORS`` is deprecated,
    you must add the request context processor in your ``TEMPLATES`` variable
    instead, please refer to the
    `relevant django documentation <https://docs.djangoproject.com/en/1.8/ref/templates/upgrading/>`_.

Then, add admin_tools and its modules to the ``INSTALLED_APPS`` like this::

    INSTALLED_APPS = (
        'admin_tools',
        'admin_tools.theming',
        'admin_tools.menu',
        'admin_tools.dashboard',
        'django.contrib.auth',
        'django.contrib.sites',
        'django.contrib.admin'
        # ...other installed applications...
    )

.. important::
    it is very important that you put the admin_tools modules **before**
    the ``django.contrib.admin module``, because django-admin-tools
    overrides the default Django admin templates, and this will not work
    otherwise.

Then, just add django-admin-tools to your urls.py file::

    urlpatterns = patterns('',
        url(r'^admin_tools/', include('admin_tools.urls')),
        #...other url patterns...
    )

Finally simply run::

    python manage.py migrate

To collect static files run::

    python manage.py collectstatic

.. important::
    it is very important that ``django.contrib.staticfiles.finders.AppDirectoriesFinder''
    be there in your ``STATICFILES_FINDERS``.


.. Testing your new shiny admin interface
.. --------------------------------------

.. Congrats! At this point you should have a working installation of
.. django-admin-tools. Now you can just login to your admin site and see what
.. changed.

.. django-admin-tools is fully customizable, but this is out of the scope of
.. this quickstart. To learn how to customize django-admin-tools modules
.. please read :ref:`the customization section<customization>`.
