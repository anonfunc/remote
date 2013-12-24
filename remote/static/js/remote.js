$(function(){
// Adding callback on remote actions.
  $("a[action]").click(function() {
    url = $(this).attr('action');
    $.get(url);
  });
});
