$(function() {
  $('#upload-file-btn').click(function() {
      var form_data = new FormData($('#upload-file')[0]);
      $.ajax({
          type: 'POST',
          url: '/upload',
          data: form_data,
          contentType: false,
          cache: false,
          processData: false,
          success: function(data) {
            $('#file').val('');
            $('#upload-message').text('File uploaded successfully');
          },
      });
  });
});
