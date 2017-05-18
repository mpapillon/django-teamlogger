# django-nouvelles-app

Nouvelles is a [Django](https://www.djangoproject.com/) application that allows you to create and collect
information within a team.

> The word *Nouvelles* comes from French, it means "News".

## Quick setup for development

1. Create a new Django project if you need it :

   ```sh
   # Replace <mysite> by the name you want
   django-admin startproject <mystite>
   ```
2. Clone the repo into the `nouvelles` directory :

   ```sh
   git clone https://mapapill@gitlab.com/mapapill/django-nouvelles-app.git nouvelles
   ```

3. Install requirements :

   ```sh
   pip install -r nouvelles/requirements.txt
   ```
   
4. Add theses lines into `INSTALLED_APPS` of `<myapp>/settings.py` :
 
   ```
   'nouvelles.apps.NouvellesConfig',
   'markdown_deux',
   ```

5. Don't forget to add essentials urls into `<myapp>/urls.py` :

   ```python
   from django.conf.urls import include, url
   from django.contrib import admin

   urlpatterns = [
        # ex: /
        url('^', include('django.contrib.auth.urls')),
    
        # ex: /nouvelles/
        url(r'^nouvelles/', include('nouvelles.urls')),
    
        # ex: /admin
        url(r'^admin/', admin.site.urls),
    ]
   ```

> View more on [Django website](https://docs.djangoproject.com/)

## Available settings

You can add the following settings into your `<myapp>/settings.py` to customize some features :

| Setting name   | Detail                               | Default                   |
| -------------- | ------------------------------------ | ------------------------- |
| HEADLINES_DAYS | Number of days of the Headlines view | 7                         |
| SITE_NAME      | Name shown in the header             | Nouvelles                 |
| SITE_FOOTER    | Text shown in the footer             | A newspaper for your team |

## Todo

 - [ ] Email sending : new article, weekly news
 - [ ] Add permissions
 - [ ] Use Bower or something else for dependencies (select2, github-mardown.css, etc...)
 - [ ] Add tests
 - [X] Better README with installation instructions and avalaible settings

## Third parties

   * [Silk Icons](http://www.famfamfam.com/lab/icons/silk/) by famfamfam
   * [Silk Icons Companion](https://github.com/damieng/silk-companion) by damieng
   * [github-markdown-css](https://github.com/sindresorhus/github-markdown-css) by sindresorhus
   * [select2](https://github.com/select2/select2) by select2

## Licence

django-nouvelles-app is under GPL v3, see LICENCE file.
