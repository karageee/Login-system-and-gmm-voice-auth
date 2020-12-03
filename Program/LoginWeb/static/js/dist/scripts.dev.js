"use strict";

$("form[name=signup_form").submit(function (e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();
  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function success(resp) {
      window.location.href = "/voice_signup/";
    },
    error: function error(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });
  e.preventDefault();
});
$("form[name=login_form").submit(function (e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();
  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function success(resp) {
      window.location.href = "/voice_signin/";
    },
    error: function error(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });
  e.preventDefault();
});