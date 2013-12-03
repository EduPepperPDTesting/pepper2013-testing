window.PollCompare = function (el) {
    RequireJS.require(['PollCompareMain','logme'], function (PollCompareMain,logme) {
    	logme("PollCompare in...")
        new PollCompareMain(el);
    });
};
