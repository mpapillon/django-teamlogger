$(function () {
    var $btnSelectAll = $('.js-btn-select-all');
    var $btnDelete = $('.js-btn-delete');
    var $drafts = $('input[name="delete"]');

    function changeSelectButton(checked) {
        if (checked) {
            $btnSelectAll.removeClass('btn-default');
            $btnSelectAll.addClass('btn-primary');
        } else {
            $btnSelectAll.addClass('btn-default');
            $btnSelectAll.removeClass('btn-primary');
        }
    }

    $drafts.change(function () {
        var $checkedDrafts = $('input[name="delete"]:checked');
        if ($btnSelectAll.hasClass('btn-primary')) {
            changeSelectButton(false);
        }

        if ($checkedDrafts.length) {
            $btnDelete.prop('disabled', false);
        } else {
            $btnDelete.prop('disabled', true);
        }

        if ($checkedDrafts.length === $drafts.length) {
            changeSelectButton(true);
        }
    });

    $btnSelectAll.click(function (e) {
        if ($btnSelectAll.hasClass('btn-default')) {
            // Toggle button visual
            changeSelectButton(true);
            // Select all elements
            $drafts.prop('checked', true);
            $btnDelete.prop('disabled', false);
        } else {
            // Toggle button visual
            changeSelectButton(false);
            // Un-select all elements
            $drafts.prop('checked', false);
            $btnDelete.prop('disabled', true);
        }
    })
});