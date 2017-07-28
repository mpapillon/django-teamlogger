TeamLogger / Changelog
=====================

0.2.2
-----

### New features 

* In the archives, the "date" field is no longer available as a filter.
* A search field is available in the archives.
* The LDAP connection has been reviewed, it supports groups.

### Correctives

* Some optimisations.

0.2.1
-----

### New features 

* Header with dates is shown on the _Archive_ page.
* Code blocks have syntax highlighting.
* Creation of _About_ and _Licence_ pages.
* Some design improvements.

### Correctives

* Static files was not collected in the right directory if the environment variable `APP_MEDIA_ROOT` was not set.
* The screen scrolling was not retained after clicking on _Preview_ tab in the article form.
* Prevent infinite loops on article.
* Minor bug fixes.

0.2.0
-----

* New application structure and docker container (uses gunicorn instead of nginx).
* Use 12factor url syntax for Database, Email and LDAP connection.
* Fix Headlines ordering ([#1](https://github.com/mpapillon/django-teamlogger/issues/1)).
* Corrects an issue that prevented access to the detail page of an article.

0.1.0
-----

First release, not ready for production.
