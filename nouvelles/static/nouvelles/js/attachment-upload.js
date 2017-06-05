// Generate 32 char random uuid 
function getUuid() {
    var uuid = "";
    for (var i = 0; i < 32; i++) {
        uuid += Math.floor(Math.random() * 16).toString(16);
    }
    return uuid
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function formatBytes(bytes, decimals) {
    if (bytes == 0) return '0 Bytes';
    var k = 1000,
        dm = decimals + 1 || 3,
        sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
        i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function addAttachment(fileId, fileName) {
    var file_url = download_url.replace('0000', fileId);

    var $file_line = $('<li id="attach_' + fileId + '">' +
        '      <p>' +
        '          <a href="' + file_url + '" class="i-attach">' + fileName + '</a> - <small>[<a href="javascript:removeAttachment(' + fileId + ')">remove</a>]</small>' +
        '      </p>' +
        '  </li>');

    if (!$('#js-attachments').find('#attach_' + fileId).length) {
        $file_line.appendTo('#js-attachments');
    }

    return $file_line;
}

function removeAttachment(fileId) {
    $('#attach_' + fileId).remove();
    $('#id_attachments').find('option[value="' + fileId +'"]').removeAttr("selected");
}

$(function () {
    $('#id_file').change(function (e) {
        $(attachment_form).submit()
    });

    $('form[enctype="multipart/form-data"]').submit(function (e) {
        e.stopPropagation(); // Stop stuff happening
        e.preventDefault(); // Totally stop stuff happening

        var files = $('#id_file').prop('files');
        $.each(files, function (key, value) {
            // Create a formdata object and add the files
            var data = new FormData();

            var uuid = getUuid(); // id for this upload so we can fetch progress info.

            data.append('file', value);

            $('#js-attachments-label').show();

            var $file_upload_line = $('<li>' +
                '      <p>' +
                '          <span class="i-attach">' + value.name + ' </span>' +
                '          <progress id="' + uuid + '" value="0" max="100" class="attachment"></progress>' +
                '      </p>' +
                '  </li>').appendTo('#js-attachments');

            var progress = $(document.getElementById(uuid))[0];

            $.ajax({
                url: upload_url,
                type: 'post',
                data: data,
                cache: false,
                dataType: 'json',
                processData: false, // Don't process the files
                contentType: false, // Set content type to false as jQuery will tell the server its a query string request
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                },
                xhr: function () {
                    var xhrobj = $.ajaxSettings.xhr();
                    if (xhrobj.upload) {
                        xhrobj.upload.addEventListener('progress', function (event) {
                            var percent = 0;
                            var position = event.loaded || event.position;
                            var total = event.total || event.totalSize;
                            if (event.lengthComputable) {
                                percent = Math.ceil(position / total * 100);
                            }
                            progress.value = percent;
                        }, false);
                    }

                    return xhrobj;
                },
                success: function (data, textStatus, jqXHR) {
                    console.info('Uploaded file :', data);
                    $file_upload_line.remove();
                    $('#id_attachments').append($('<option>', {
                        value: data.id,
                        text: data.file_name,
                        selected: true
                    }));
                    addAttachment(data.id, data.file_name);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.error(textStatus);
                }
            });
        });

        return true;
    });
});

$("#id_attachments").find(":selected").each(function() {
    addAttachment(this.value, this.text)
});