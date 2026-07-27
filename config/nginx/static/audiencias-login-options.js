(function () {
  'use strict';

  function providerButton(provider, label, nextUrl) {
    var button = document.createElement('a');
    var styleProvider = provider === 'google-oauth2' ? 'google' : provider;
    button.className = 'edem-button -social -' + styleProvider;
    button.href = '/accounts/login/' + provider + '/?next=' +
      encodeURIComponent(nextUrl);

    if (provider === 'govbr') {
      button.innerHTML =
        '<span class="govbr-signin__icon" aria-hidden="true">' +
        '<i class="icon icon-user"></i></span>' +
        '<span class="govbr-signin__label">' + label + '</span>';
    } else {
      button.textContent = label;
    }

    return button;
  }

  function addProviderButtons(content, options, nextUrl) {
    var oldSocial = content.querySelectorAll('.social');
    oldSocial.forEach(function (element) {
      element.remove();
    });

    if (!options.govbr && !options.google) {
      return;
    }

    var social = document.createElement('div');
    social.className = 'social audiencias-auth-social';

    if (options.govbr) {
      social.appendChild(
        providerButton('govbr', 'Entrar com Gov.br', nextUrl)
      );
    }

    if (options.google) {
      social.appendChild(
        providerButton('google-oauth2', 'Continuar com Google', nextUrl)
      );
    }

    var form = content.querySelector('form.access');
    if (form) {
      content.insertBefore(social, form);
    } else {
      content.appendChild(social);
    }
  }

  function showFallback(content) {
    var message = document.createElement('p');
    message.className = 'audiencias-auth-error';
    message.innerHTML =
      'Não foi possível carregar as formas de acesso. ' +
      '<a href="/">Entre pela página inicial.</a>';
    content.appendChild(message);
  }

  function applyOptions(options) {
    var sidebar = document.querySelector('.edem-sidebar');
    if (!sidebar) {
      return;
    }

    sidebar.classList.toggle('auth-email-enabled', Boolean(options.email));

    var nextUrl = window.location.pathname + window.location.search;
    var contents = sidebar.querySelectorAll(
      '.JS-signinContent, .JS-signupContent'
    );
    contents.forEach(function (content) {
      addProviderButtons(content, options, nextUrl);
    });
    sidebar.classList.add('auth-options-ready');
  }

  function loadOptions() {
    fetch('/accounts/login-options/', {
      credentials: 'same-origin',
      headers: {'Accept': 'application/json'}
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error('HTTP ' + response.status);
        }
        return response.json();
      })
      .then(applyOptions)
      .catch(function () {
        document.querySelectorAll(
          '.JS-signinContent, .JS-signupContent'
        ).forEach(showFallback);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadOptions);
  } else {
    loadOptions();
  }
}());
