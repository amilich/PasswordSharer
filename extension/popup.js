/* attach a submit handler to the form */
$("#login-form").submit(function(event) {

  /* stop form from submitting normally */
  event.preventDefault();

  /* get some values from elements on the page: */
  var $form = $( this ),
  url = $form.attr( 'action' );

  /* Send the data using post */
  var posting = $.post( url, { authURL: $('#authURL').val(), email: $('#name2').val(), password: $('#password').val(), RememberMe: $('#RememberMe').val() } );

  /* Alerts the results */
  posting.done(function( data ) {
    alert('success');
  });
});