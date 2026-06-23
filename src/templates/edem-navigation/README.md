# edem-navigation
Core navigation Django component for e-Democracia.

It's a topbar and an off-canvas sidebar, made into this "generic" submodule because Audiências-Públicas don't work in our proxy solution used in e-Democracia, Colab. In the future this would be discarted whenever Audiências-Públicas is truly inside our proxy solution (One can hope).


## Overall Instructions
In order for this to work properly in a Django project, you gotta follow some steps:

### Call the submodule 
- Call this repo as a submodule alongside the template structure (usually inside a folder named `/templates` in our projects) with:
```
git submodule add -b master https://github.com/labhackercd/edem-navigation.git
```

### Install django-macros
- Add it to the `requirements.txt` file and/or install it with:
```
pip install django-macros>=0.4.0
```
- Add `macros` to your`INSTALLED_APPS` list.

### Prepare your macros
- Using macros was our easiest solution to add dynamic content to the edem-navigation only by modyfing template files.
Right at the beggining of our `edem-navigation.html` template, is a list of macros with blocks in them that are to be rendered in various places. In order for this to work you need to create a template file outside the edem-navigation structure containing your custom values inside the blocks. Consequently this file has to extend the `edem-navigation.html` template.

- So, here is an example of how the content of your file should be:
```django
{% extends "edem-navigation/edem-navigation.html" %}
{% load staticfiles %}

{# Whitespace is added when defining these blocks, so DO NOT ident them! #}
{% block edem_facebook_url %}/account/social/login/facebook/?next={{ request.path }}{% endblock %}
{% block edem_google_url %}/account/social/login/google-oauth2/?next={{ request.path }}{% endblock %}
{% block edem_profile_url %}/profile{% endblock %}
{% block edem_logout_url %}/account/logout{% endblock %}
...
```
- Remember to fill all the necessary blocks referenced in `edem-navigation.html`.
- Don't add spaces or identation in these blocks, or whitespace will be rendered as a result.

### Add a new entry in your static_dirs
- Since this submodule consists also of static files like images, SCSS and JS files, you should add the `/edem-navigation/static` directory under your project `STATICFILES_DIRS` list.

### Call the static files in your main project
- Add references to the JS and SCSS files in the proper places of the base of your project with:
```django
<link rel="stylesheet" href="{% static 'edem-navigation/scss/edem.scss' %} type="text/x-scss""/>
<script type="text/javascript" src="{% static 'edem-navigation/js/edem-navigation.js' %}"></script>
```
- Include the file you created with the macro/blocks and with `edem-navagtion.html` extended inside a .edem-content-wrapper div under the body:

```django
<div class="edem-content-wrapper">

  {# edem-navigtaion #}
  {% include "your-file-name.html" %}
 
  {# Your project Content #}
  <main class="main">
    Whatever goes here
  </main>

</div>
```


## Updating changes
- If you modify this repo, make sure it won't break the aforementioned structure. If you really need to change this, document it!
- Whenever any changes are made here, just push them to `master` and update this submodule inside your project with `git submodule update --remote`. We usually commit this updating process directly on the project current working branch (we don't bother creating a new branch just for this).
