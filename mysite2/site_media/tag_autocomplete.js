$(document).ready(function () {
  $("#id_tags").autocomplete(
     '/ajax/tag/autocomplete/',
     {multiple: true, multipleSeparator: ' '}
  );
});