$(function () {
    var $content_textarea = $('#id_content');
    var $content_panel = $('#article_content_panel');
    var $editor_tabs = $('#editor-tabs');
    var $tags = $('#id_tags');

    // Enable select2
    $tags.select2({width: '100%', theme: 'spectre'});

    enableEditorFocus();
    enableEditorTabs();
    attachmentsEvents();

    /**
     * Turn on editor focus stylesheet
     */
    function enableEditorFocus() {
        $content_textarea.focus(function (e) {
            $content_panel.addClass('focused')
        });

        $content_textarea.blur(function (e) {
            $content_panel.removeClass('focused')
        });
    }

    /**
     * Define actions on editor tabs
     */
    function enableEditorTabs() {
        $editor_tabs.tabs(function (tabName) {
            if (tabName === 'preview') {
                $('#md_preview').height($('#editor').height());
                $.ajax({
                    url: window.preview_url,
                    type: 'post',
                    data: {"text": $content_textarea.val()},
                    success: function (data) {
                        $('#md_preview').html(data);
                    }
                });
            }

            if (tabName === 'editor') {
                $('#md_preview').html('<div class="loading" style="height: 100%;"></div>');
                $content_textarea.focus();
            }
        });
    }

    /**
     * Enable attachments events like Add and Delete.
     */
    function attachmentsEvents() {
        var attachment_pending = '<div id="id_attachments-__id__-tile" class="column col-4 col-xs-12 d-hide">\n' +
            '                    <div class="d-hide">\n' +
            '                        __formset__\n' +
            '                    </div>\n' +
            '                    <div class="tile tile-centered tile-attachment"\n' +
            '                         title="This file will be uploaded when the article will be saved">\n' +
            '                        <div class="tile-icon">\n' +
            '                            <a class="btn btn-action btn-primary btn-lg" disabled>\n' +
            '                                <i class="icon icon-upload centered"></i>\n' +
            '                            </a>\n' +
            '                        </div>\n' +
            '                        <div class="tile-content">\n' +
            '                            <div id="id_attachments-__id__-name" class="tile-title">__name__</div>\n' +
            '                            <div class="tile-subtitle">Ready to be uploaded</div>\n' +
            '                        </div>\n' +
            '                        <div class="tile-action">\n' +
            '                            <button id="id_attachments-__id__-delete-btn"\n' +
            '                                    type="button" class="btn btn-link"\n' +
            '                                    title="Cancel file upload">\n' +
            '                                <i class="icon icon-cross"></i>\n' +
            '                            </button>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>';

        // Enable events on "Add Attachments" buttons
        $('.js-add-attachment-btn').on('click', function (e) {
            var $empty_form = $("#js-attachments-empty-form");
            var $total_forms = $("#id_attachments-TOTAL_FORMS");

            var totalForms = parseInt($total_forms.val());
            $total_forms.val(totalForms + 1);

            var compiledFormset = $empty_form.html().replace(/__prefix__/g, totalForms);
            // Creates a new attachment
            var new_attach = attachment_pending
                .replace(/__formset__/g, compiledFormset)
                .replace(/__id__/g, totalForms);
            $('#js-attachments').append(new_attach);

            var $fileInput = $('#id_attachments-' + totalForms + '-file');
            var $deleteButton = $('#id_attachments-' + totalForms + '-delete-btn');

            $fileInput.change(function (e) {
                // Add the file in the list after user select a file from his disk.
                $target = $(e.target);
                var files = $target.prop('files');
                if (files.length > 0) {
                    var name = files[0].name;
                    $('#id_attachments-' + totalForms + '-name').text(name);
                    $('#js-attachments-empty').addClass('d-hide');
                    $('#id_attachments-' + totalForms + '-tile').removeClass('d-hide');
                }
            });

            $deleteButton.click(function (e) {
                // Removes the file from the list and cancel pending upload.
                var $target = $(e.target);
                var $tile = $target.parents().eq(2);

                $tile.remove()
            });

            // Allow users to select a file.
            $fileInput.click();
        });

        $('.js-delete-button').find('input[type="checkbox"]').change(function (e) {
            // Hides the visual attachment if the user wants to delete it.
            var $target = $(e.target);
            var $tile = $target.parents().eq(2);
            $tile.addClass('d-hide');
        });
    }
});
