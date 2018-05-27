//=../../../staticfiles/bower_components/jquery/dist/jquery.js
//=../libs/uikit.js
//=../libs/uikit-icons.js
//=../libs/slick.js

$(function () {
    $('#sign-up').on('click', function () {
        $('.menu > div').hide();
    });

    $('.lesson_slider').slick({
        infinite: false,
        speed: 500,
        fade: true,
        nextArrow: '<i class="zmdi zmdi-chevron-right arrow_right"></i>',
        prevArrow: '<i class="zmdi zmdi-chevron-left arrow_left"></i>',
        cssEase: 'linear'
    });

    $('.pause-button').on('click', function () {
        $('#video_frame')[0].contentWindow.postMessage('{"event":"command","func":"' + 'pauseVideo' + '","args":""}', '*');
        // $('.video_slide').get(0).pause();
    });

    $('.pause-btn').on('click', function () {
        $('#vi_frame')[0].contentWindow.postMessage('{"event":"command","func":"' + 'pauseVideo' + '","args":""}', '*');
        // $('#p_video').get(0).pause();

    });
});







