function closeEdemSidebar() {
  $('.JS-openSidebar').removeClass('-active');
  $('body').removeClass('-sidebaropen');
}

function openEdemSidebar(option) {
  var contentSelector = '.JS-' + option + 'Content';
  var linkSelector = '.JS-openSidebar[data-sidebar-content="' + option + '"]';

  $('body').addClass('-sidebaropen');
  $('.JS-sidebarContent').removeClass('-show');
  $('.JS-openSidebar').removeClass('-active');
  $(linkSelector).addClass('-active');
  $(contentSelector).addClass('-show');
  resizeRecaptcha();
}

function resizeRecaptcha() {
  if (!$('.JS-signupContent').hasClass('JS-signupFinished')){ // Only run if signup is not completed
    var accessWidth = $('.JS-signUpForm')[0].getBoundingClientRect().width; // Get value with decimals
    var captchaWidth = 302;
    var captchaHeight = 78;
    var captchaDynamicHeight = $('.g-recaptcha')[0].getBoundingClientRect().height;
    var scaleRatio = accessWidth / captchaWidth;
    var scaleHeight = captchaHeight * scaleRatio;

    $('.g-recaptcha').css({
      'transform' : 'scale('+scaleRatio+')',
      '-webkit-transform' : 'scale('+scaleRatio+')',
      '-ms-transform' : 'scale('+scaleRatio+')',
      '-o-transform' : 'scale('+scaleRatio+')',
      'transform-origin' : '0 0',
      '-webkit-transform-origin' : '0 0',
      '-ms-transform-origin' : '0 0',
      '-o-transform-origin' : '0 0',
      'height' : scaleHeight
    });
  }
}

function ensureEdemOverlay() {
  var wrapper = document.querySelector('.edem-content-wrapper');
  var overlay = document.querySelector('.edem-overlay');

  if (!overlay && wrapper) {
    overlay = document.createElement('div');
    overlay.className = 'edem-overlay';
    wrapper.appendChild(overlay);
  }

  return overlay;
}

function nativeCloseEdemSidebar() {
  var sidebarLinks = document.querySelectorAll('.JS-openSidebar');
  for (var i = 0; i < sidebarLinks.length; i++) {
    sidebarLinks[i].classList.remove('-active');
  }

  document.body.classList.remove('-sidebaropen');
}

function nativeOpenEdemSidebar(option) {
  var contentSelector = '.JS-' + option + 'Content';
  var linkSelector = '.JS-openSidebar[data-sidebar-content="' + option + '"]';
  var contents = document.querySelectorAll('.JS-sidebarContent');
  var sidebarLinks = document.querySelectorAll('.JS-openSidebar');
  var activeContent = document.querySelector(contentSelector);
  var activeLink = document.querySelector(linkSelector);

  document.body.classList.add('-sidebaropen');

  for (var i = 0; i < contents.length; i++) {
    contents[i].classList.remove('-show');
  }

  for (var j = 0; j < sidebarLinks.length; j++) {
    sidebarLinks[j].classList.remove('-active');
  }

  if (activeLink) {
    activeLink.classList.add('-active');
  }

  if (activeContent) {
    activeContent.classList.add('-show');
  }

  try {
    resizeRecaptcha();
  } catch (error) {
    // Some proxied apps load the navigation before external captcha code finishes.
  }
}

function nativeToggleTopbarMenu() {
  var toggles = document.querySelectorAll('.JS-toggleTopbarMenu');
  var menuHandlers = document.querySelectorAll('.JS-topbarMenuHandler');
  var shouldOpen = true;

  for (var i = 0; i < toggles.length; i++) {
    if (toggles[i].classList.contains('-active')) {
      shouldOpen = false;
      break;
    }
  }

  for (var j = 0; j < toggles.length; j++) {
    toggles[j].classList.toggle('-active', shouldOpen);
  }

  for (var k = 0; k < menuHandlers.length; k++) {
    menuHandlers[k].classList.toggle('-menuopen', shouldOpen);
  }
}

function closestNavigationTarget(target, selector) {
  if (target && target.nodeType !== 1) {
    target = target.parentElement;
  }

  if (!target || !target.closest) {
    return null;
  }

  return target.closest(selector);
}

function bindNativeNavigationEvents() {
  if (window.edemNativeNavigationBound) {
    return;
  }

  window.edemNativeNavigationBound = true;
  ensureEdemOverlay();

  document.addEventListener('click', function(event) {
    var toggle = closestNavigationTarget(event.target, '.JS-toggleTopbarMenu');
    var openLink = closestNavigationTarget(event.target, '.JS-openSidebar');
    var closeLink = closestNavigationTarget(event.target, '.JS-closeSidebar');
    var overlay = closestNavigationTarget(event.target, '.edem-overlay');

    if (toggle) {
      event.preventDefault();
      event.stopImmediatePropagation();
      nativeCloseEdemSidebar();
      nativeToggleTopbarMenu();
      return;
    }

    if (openLink) {
      event.preventDefault();
      event.stopImmediatePropagation();

      if (openLink.classList.contains('-active') && document.body.classList.contains('-sidebaropen')) {
        nativeCloseEdemSidebar();
      } else {
        nativeOpenEdemSidebar(openLink.getAttribute('data-sidebar-content'));
      }
      return;
    }

    if (closeLink || overlay) {
      event.preventDefault();
      event.stopImmediatePropagation();
      nativeCloseEdemSidebar();
    }
  }, true);
}

function showError(errorMessage) {
  $('.JS-accessErrorBox').removeAttr('hidden');
  $('.JS-accessError').text(errorMessage);
}

function showSuccessSignupMessage(message) {
// Replace signup content html with our success message.
  var userEmail = $('#mail').val();
  var successMessage = message || "Cadastro realizado. Você já pode entrar com o email que você forneceu (<span class='highlight'>" + userEmail + "</span>).";
  var thanksElement = $('<p/>').addClass('success').text('Obrigado por se cadastrar!')
  var successElement = $('<p/>').addClass('success').html(successMessage);

  $('.JS-signupContent').addClass('JS-signupFinished').html(thanksElement).append(successElement);
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfHeaders() {
  var token = getCookie('csrftoken');
  return token ? {'X-CSRFToken': token} : {};
}

function updateCsrfToken(token) {
  if (token) {
    $('input[name="csrfmiddlewaretoken"]').val(token);
  }
}

function refreshCsrfToken() {
  return $.ajax({
    type: 'GET',
    url: '/accounts/ajax/csrf/',
    cache: false,
    dataType: 'json'
  }).then(function(response) {
    updateCsrfToken(response.csrfToken);
    return response.csrfToken;
  });
}

function syncExternalSessions() {
  $.ajax({
    type: 'GET',
    url: '/accounts/ajax/sync-sessions/',
    cache: false,
    dataType: 'json',
    success: function(response) {
      var synced = response.synced || [];
      if (synced.length && location.pathname.match(/^\/(audiencias|wikilegis|expressao)(\/|$)/)) {
        location.reload();
      }
    }
  });
}

// Resize reCAPTCHA on window resize
$(window).resize(function(){
  if ($('body').hasClass('-sidebaropen')) {
    resizeRecaptcha();
  }
});

// Create and append to body an overlay div for when the sidebar is opened
if (!$('.edem-overlay').length) {
  $('<div/>', {class: 'edem-overlay'}).appendTo('.edem-content-wrapper');
}

bindNativeNavigationEvents();

// Open sidebar via the topbar
$('.JS-openSidebar').click(function() {
  if ($(this).hasClass('-active') && $('body').hasClass('-sidebaropen')) {
    closeEdemSidebar();
  } else {
    openEdemSidebar($(this).data('sidebarContent'));
  }
});

// eDemocracia sidebar close button
$('.JS-closeSidebar').click(function(){
  closeEdemSidebar();
});

// Close sidebar if click on the overlay
$('.edem-overlay').click(function(){
  closeEdemSidebar();
});

// Toggle topbar items when on mobile
$('.JS-toggleTopbarMenu').click(function(){
  if ($(this).hasClass('-active')){
    $(this).removeClass('-active');
    $('.JS-topbarMenuHandler').removeClass('-menuopen');
  } else {
    $(this).addClass('-active');
    $('.JS-topbarMenuHandler').addClass('-menuopen');
  }
});

// Detect when input is filled
$('.JS-formInput').focus(function() {
  $(this).closest('.form-field').addClass('-filled');
});

$('.JS-formInput').blur(function() {
  if (!$(this).val() == '') {
    $(this).closest('.form-field').addClass('-filled');
  } else {
    $(this).closest('.form-field').removeClass('-filled');
  }
});

// Toggle country/state input
$('.JS-inputActionState').on('mousedown', function(e){
  e.preventDefault();
  $(this).closest('.form-field').attr('hidden','').removeClass('-filled');
  $(this).siblings('.JS-formInput').val('');
  $('.JS-inputActionCountry').closest('.form-field').removeAttr('hidden');
});

$('.JS-inputActionCountry').on('mousedown', function(e){
  e.preventDefault();
  $(this).closest('.form-field').attr('hidden','').removeClass('-filled');
  $(this).siblings('.JS-formInput').val('');
  $('.JS-inputActionState').closest('.form-field').removeAttr('hidden');
});

// Toggle show password
$('.JS-fieldActionPassword').on('mousedown', function(e){
  var input = $(this).siblings('.JS-formInput');
  e.preventDefault();
  if (input.attr('type') === 'text') {
    input.attr('type', 'password');
    $(this).text('Mostrar Senha');
  } else {
    input.attr('type', 'text');
    $(this).text('Esconder Senha');
  }
});

// Close error message
$('.JS-closeAccessError').click(function(){
  $('.JS-accessErrorBox').attr('hidden', '');
});

$('.JS-logoutForm').submit(function(event) {
  event.preventDefault();
  var logoutForm = this;
  var submitButton = $(logoutForm).find('button[type="submit"]');

  submitButton.addClass('-loading');
  refreshCsrfToken()
    .done(function() {
      logoutForm.submit();
    })
    .fail(function() {
      submitButton.removeClass('-loading');
      showError("Ocorreu um erro no servidor, tente novamente em alguns instantes.");
    });
});

// Ajax calls for login and signup
$('.JS-loginForm').submit(function(event) {
  event.preventDefault();
  var loginForm = $(this);
  var submitButton = $('.JS-loginForm .JS-sendForm');

  if (loginForm.hasClass('JS-submitting')) {
    return false;
  } else {
    loginForm.addClass('JS-submitting');
    submitButton.addClass('-loading');

    refreshCsrfToken().done(function() {
      $.ajax({
        type:"POST",
        url: '/accounts/ajax/login/',
        headers: csrfHeaders(),
        data: $(event.target).serialize(),
        success: function(response){
          location.reload();
        },
        error: function(jqXRH){
          loginForm.removeClass('JS-submitting');
          submitButton.removeClass('-loading');

          if (jqXRH.status == 0) {
            showError("Verifique sua conexão com a internet.")
          } else if (jqXRH.status == 401) {
            $('.JS-inputError').text('');
            $(event.target)
              .find('.JS-inputError')
              .text(jqXRH.responseJSON['data'])
              .removeAttr('hidden');
          } else {
            showError("Ocorreu um erro no servidor, tente novamente em alguns instantes.");
          }
        }
      });
    }).fail(function() {
        loginForm.removeClass('JS-submitting');
        submitButton.removeClass('-loading');
        showError("Ocorreu um erro no servidor, tente novamente em alguns instantes.");
    });
  }

});

$('.JS-signUpForm').submit(function(event) {
  event.preventDefault();
  var signUpForm = $(this);
  var submitButton = $('.JS-signUpForm .JS-sendForm');
  var hasRecaptcha = typeof grecaptcha !== 'undefined' && $('.g-recaptcha').length;

  if (hasRecaptcha && grecaptcha.getResponse() == "") {
    showError("Por favor preencha o reCAPTCHA.");

  } else if (signUpForm.hasClass('JS-submitting')) {
    return false;

  } else {
    signUpForm.addClass('JS-submitting');
    submitButton.addClass('-loading');

    refreshCsrfToken().done(function() {
      $.ajax({
        type:"POST",
        url: '/accounts/ajax/signup/',
        headers: csrfHeaders(),
        data: $(event.target).serialize(),
        success: function(response){
          showSuccessSignupMessage(response.data);
        },

        error: function(jqXRH) {
          signUpForm.removeClass('JS-submitting');
          submitButton.removeClass('-loading');

          if (hasRecaptcha) {
            grecaptcha.reset();
            $("#g-recaptcha-response").val("");
          }
          if (jqXRH.status == 0) {
            showError('Verifique sua conexão com a internet.');
          } else if (jqXRH.status == 400) {
            $('.JS-inputError').text('');
            $.each(jqXRH.responseJSON["data"], function(key, value) {
              if (key != '__all__') {
                $(event.target)
                  .find('[data-input-name="'+key+'"]')
                  .text(value)
                  .removeAttr('hidden');
              } else {
                showError(value);
              }
            });
          } else if (jqXRH.status == 401) {
            showError(jqXRH.responseJSON["data"])
          } else {
            showError("Ocorreu um erro no servidor, tente novamente em alguns instantes.");
          }
        }
      });
    }).fail(function() {
        signUpForm.removeClass('JS-submitting');
        submitButton.removeClass('-loading');
        showError("Ocorreu um erro no servidor, tente novamente em alguns instantes.");
    });
  }
});

syncExternalSessions();

// XXX This should be exclusively on Audiencias Plugin whenever is possible
if (location.href.match(/audiencias/)) {
  $(document).on('click', 'a[href^="/home/?next="]', function(e){
    e.preventDefault();
    openEdemSidebar('signin');
  });
}
