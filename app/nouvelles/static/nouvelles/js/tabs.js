(function ($) {
    $.fn.tabs = function (onSwitch) {
        var $tabsContainer = $(this);
        $tabsContainer.find('.tab > a').each(function () {
            var $tab = $(this);
            $(this).on('click', function (e) {
                e.preventDefault();
                var targetName = $(e.target).data('target');

                if (onSwitch) {
                    onSwitch(targetName);
                }

                $tabsContainer.find('.tab.active').removeClass('active');
                $tabsContainer.find('.tab-content.active').removeClass('active');

                $(e.target).parent().addClass('active');
                $('#' + targetName).addClass('active');
            });
        });
        return this;
    }
})(jQuery);
