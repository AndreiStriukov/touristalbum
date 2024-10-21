$(document).ready(function(){

    $('div.main_text').hide().show(1500);

    
    // отображение кнопок управления формой при задании фильтрации непосредственно в элементе фильтрации
    function button_vis(event){
        $('#a_filter').find('.alb_filter_apply').remove();
        $(this).parents('.alb_filter_list_checkbox').after(search_button);
    }

    var search_button = $('.alb_filter_apply').clone();

    $('#j_place').keyup(button_vis);
    $('.checked').change(button_vis);


    //Сворачивание/разворачивание элементов

    $('.header_burger').click(function(event){
        $('.header_burger, .header_menu').toggleClass('active')
    });

    $('body').toggleClass('lock');


    // Окно фильтра
    $("#filter_link").click(function(event){
        event.preventDefault();
        $('.filter_block').toggleClass('active');
    })

    $(".alb_filter_label").click(function(){
            // console.log('!!!filter-- help!!!');
            $(this).next('.alb_filter_list_checkbox').toggleClass("active");
            $(this).toggleClass("active");
        });

    // Подсчет количества выбранных чекбоксов и обнуление при кнопке "Сбросить"

    $('#a_filter input:checkbox').click(function(){ 
        var count1 = $('#f1 :checkbox:checked').length;
        $('#result1 span').html(count1);

        var count3 = $('#f3 :checkbox:checked').length;
        $('#result3 span').html(count3);

        var count4 = $('#f4 :checkbox:checked').length;
        $('#result4 span').html(count4); 
    }); 
    
    $('#reset_btn').click(function(){ 
        $('#result1 span').html(0);
        $('#result3 span').html(0);
        $('#result4 span').html(0); 
    });

    // Отпрвка формы

    // var form_filter = $("#a_filter");
    var form_filter = $("#a_filter");
    form_filter.on('submit', function(event){
        event.preventDefault();
        let url = this.action;
        let params = $(this).serialize();
        // console.log(params);

        $.get(url, params, function(data){
            if ($(window).width() <= '820'){
                $('.filter_block').toggleClass('active');
            }
            $('#filter_link').toggleClass('yellow');
            $('#post_a_filter').html(data);
        })
        
    })


    // Модальное окно

    var formModal = $('.cd-user-modal'),
        mainNav = $('.main-nav');

    //open modal
    $('#window').on('click', function(event){
        $('.cd-user-modal').toggleClass('is-visible');
        $(".form_email").after('<i class="fa fa-at" aria-hidden="true"></i>');
        // $(".form_password").after('<a href="#0" class="show-password"><i class="fa fa-unlock-alt" aria-hidden="true"></i></a>');
        // $(".form_username").after('<i class="fa fa-fa-user" aria-hidden="true"></i>');
        $('.header_burger, .header_menu').toggleClass('active') // спрятать меню
    });


    //close modal
    formModal.on('click', function(event){
        if( $(event.target).is(formModal) ) {
            formModal.removeClass('is-visible');
        }   
    });

    //hide or show password
    $('.show_password').on('click', function(event){
        var togglePass = $(this),
            passwordField = togglePass.prev('input');

        if ($('.form_password').attr('type') == 'password'){

            $('.form_password').attr('type', 'text');
            $('#lock').removeClass('fa-lock').addClass('fa-unlock');

        } else {

            $('.form_password').attr('type', 'password');
            $('#lock').removeClass('fa-unlock').addClass('fa-lock');
        }

    });


    // Отправка формы входа пользователя из модального окна
    $('#login_form').submit(function(event){
        event.preventDefault();
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                console.log('ok - ', response)
                if (response.status===201)
                {
                    location.reload();
                }
                else if (response.status===202){
                    $('.form_message').html(response.error).removeClass('message_non')
                }
                else {
                    $('.form_message').html(response.error).removeClass('message_non')
                }
            },
            error: function (response) {
                console.log('err - ', response)
            }

        })

    })

    // Выбор файла в форме

    $('.label_avatar_file').click(function(){
        $(".input_avatar").click();
    });
     
    $('.input_avatar').change(function() {
        $('#selected_filename').text($('.input_avatar')[0].files[0].name);
    });


});