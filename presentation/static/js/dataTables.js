$(document).ready(function() {
  $('table').not('#test-results').DataTable({
    language: {
        url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/ru.json',
    },
  });
});