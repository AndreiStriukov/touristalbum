$(document).ready(function(){

    // Основной слайдер
    $('.main-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: false, // Изначально автоплей выключен
        autoplaySpeed: 1500, // Скорость автопрокрутки в миллисекундах
        arrows: true,                // Показываем стрелки для прокрутки
        prevArrow: '<button type="button" class="slick-prev"> </button>', // Задаем свою кнопку "Prev" без текста
        nextArrow: '<button type="button" class="slick-next"> </button>', // Задаем свою кнопку "Next" без текста
        fade: true,                  // Эффект плавного перехода
        asNavFor: '.nav-slider',      // Связываем с навигационным слайдером
        responsive: [
            {
              breakpoint: 1024, // - от какой ширины изменять настройки(1024 и ниже)
              settings: {
                // вносим изменения на ширине 1024 и ниже 
                arrows: false,
                swipe: true,                     // Включаем свайп
                swipeToSlide: true,              // Позволяет пользователю переходить к слайду при свайпе
                touchThreshold: 5,               // Чувствительность свайпа (чем меньше значение, тем быстрее реагирует)
              }
            },
            {
              breakpoint: 480, 
              settings: {
                arrows: false,
                swipe: true,                     // Включаем свайп
                swipeToSlide: true,              // Позволяет пользователю переходить к слайду при свайпе
                touchThreshold: 5,               // Чувствительность свайпа (чем меньше значение, тем быстрее реагирует)
              }
            }
          ]
    });

    $('.main-slider').off('touchstart').on('touchstart', function() {
        $(this).slick('slickNext');
    });

    // Старт автоплей
    $('.play-button').click(function(e) {
        e.preventDefault(); // Предотвращаем переход по ссылке
        $('.main-slider').slick('slickPlay'); // Включаем автоплей
        $('.play-button').addClass('play-on').removeAttr('href');
        $('.stop-button').removeClass('play-on').addClass('icon-ref').attr('href', '#');
    });

    // Остановка автоплей
    $('.stop-button').click(function(e) {
        e.preventDefault(); // Предотвращаем переход по ссылке
        $('.main-slider').slick('slickPause'); // Останавливаем автоплей
        $('.play-button').removeClass('play-on').attr('href', '#');
        $('.stop-button').removeClass('icon-ref').addClass('play-on').removeAttr('href');
    });

    // Навигационный слайдер
    $('.nav-slider').slick({
        // vertical: true,              // Вертикальная прокрутка
        // verticalSwiping: true,       // Поддержка вертикального свайпа
        slidesToShow: 3,             // Количество миниатюр, видимых одновременно
        slidesToScroll: 1,
        asNavFor: '.main-slider',    // Связываем с основным слайдером
        focusOnSelect: true,         // Переключение на слайд по клику на миниатюру
        arrows: false,               // Убираем стрелки навигации, чтобы не дублировать их с навигацией
        centerMode: true,            // Центрируем активный слайд
        centerPadding: '0px',        // Убираем отступы, чтобы миниатюры плотно прилегали друг к другу
        adaptiveHeight: true         // Адаптация высоты слайдера под текущий слайд
    });

    // бургер-меню

    // Показ/скрытие бургер-меню
    $('.burger-menu-btn').click(function() {
        $('.burger-nav').toggle();
    });

    // Закрытие меню при клике на обычные ссылки
    $('.burger-nav a').not('.has-submenu > a').click(function() {
        $('.burger-nav').hide();
    });


    // Показ/скрытие подменю при клике на иконку треугольника
    $('.submenu-toggle-a, submenu-toggle').click(function(e) {
        e.stopPropagation(); // Останавливаем всплытие события
        $(this).parent().toggleClass('submenu-open');
    });

    // Показ/скрытие описания альбома
    $('.descr-ref').click(function(e) {
      e.preventDefault();
      $('.description').toggleClass('description-open');
      $('.descr-ref').toggleClass('ref-open');
    });

    // Показ описания фото
    $('.info-photo a').click(function(e) {
      e.preventDefault();
      $('.ph-descr').addClass('ph-descr-open');
      $('.info-photo').hide()
    });

      // Скрытие описания фото
      $('.close-win').click(function(e) {
      e.preventDefault();
      $('.ph-descr').removeClass('ph-descr-open');
      $('.info-photo').show()
    });
        
})