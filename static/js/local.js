function make_notice (picture_id) {
    html = '<div class="modal" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">  <div class="modal-header">    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>    <h3 id="myModalLabel">Добавить заметку</h3>  </div>  <div class="modal-body">    <p><textarea id="input_notice" style="width: 95%"/></p>  </div>  <div class="modal-footer">    <button class="btn" data-dismiss="modal" aria-hidden="true">Закрыть</button>    <button class="btn btn-primary" onclick="save_notice(' + picture_id + ');">Сохранить</button>  </div></div>'
    $('html').append(html)
    $('#myModal').modal('show')
}

function save_notice (picture_id) {
    $.ajax({
        url: '/notice/notice/',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({ text: $('#input_notice').val(), picture: picture_id })
    }).done( function(data) {
        document.location = '/';
    }).fail( function(data) {
        alert('Что-то пошло не так, попробуйте позже');
    });
    $('#myModal').remove()
}

function del_picture (picture_id) {
    $.ajax({
        url: '/picture/picture/' + picture_id + '/',
        type: "DELETE",
    }).done( function(data) {
        document.location = '/';
    }).fail( function(data) {
        alert('Что-то пошло не так, возможно у Вас недостаточно прав на это действие');
    });
};

function edit_picture (picture_id) {
    html = '<div class="modal" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">  <div class="modal-header">    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>    <h3 id="myModalLabel">Редактировать заголовок</h3>  </div>  <div class="modal-body">    <p><textarea id="input_title_edit" style="width: 95%"/></p>  </div>  <div class="modal-footer">    <button class="btn" data-dismiss="modal" aria-hidden="true">Закрыть</button>    <button class="btn btn-primary" onclick="edit_picture_save(' + picture_id + ');">Сохранить</button>  </div></div>'
    $('html').append(html)
    $('#myModal').modal('show')
}

function edit_picture_save (picture_id) {
    $.ajax({
        url: '/picture/picture/' + picture_id + '/',
        type: "PATCH",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({ title: $('#input_title_edit').val() })
    }).done( function(data) {
        console.log(data);
        $('#myModal').remove()
    }).fail( function(data) {
        if (data.status == 400) {
            $('.form_error').remove();
            errors = $.parseJSON(data.responseText)
            console.log(errors)
            $.each(Object.keys(errors), function( index, value ) {
                $('#input_title_edit').after('<span class="form_error">' + errors[value].join(' ') + '</span>')
            });
        };
    });
}

function pictures_to_email(page) {
    $.ajax({
        url: '/picture/picture/',
        type: "GET",
        data: { page: page, format: 'email'}
    }).done( function(data) {
        alert(data);
    }).fail( function(data) {
        alert('Что-то пошло не так, попробуйте позже');
    });
}

function load_pictures (page) {
    $.ajax({
        url: '/picture/picture/',
        type: "GET",
        dataType: "json",
        data: { page: page }
    }).done( function(data) {
        res = '<div class="row-fluid"><button type="button" class="btn btn-primary pull-right" onclick="pictures_to_email(' + page + ')">Отправить на email</button></div><hr>'
        $.each(data.results, function( index, value ) {
            if (value.notice == undefined | value.notice == '') {
                note = '<a href="#" onclick="make_notice(' + value.id + ');">Добавить заметку</a>'
            } else {
                note = '<span>' + value.notice + '</span>'
            };

            if (value.is_owner) {
                edit_ctr = '<p><a href="#" onclick="del_picture(' + value.id + ')">[Удалить]</a><a href="#" onclick="edit_picture(' + value.id + ')">[Редактировать]</a></p>'
            } else {
                edit_ctr = ''
            };

            res += '<div class="row-fluid" style="margin-top: 15px;"><div class="span4"><img class="img-rounded" width="400px" src="' + value.picture.url + '"/></div><div class="hero-unit span8"><h2>' + value.title + '</h2>' + edit_ctr + note + '</div></div>'
        });

        if (data.previous) {
            ppage = data.previous.split('?page=')[1]
            res += '<button type="button" class="btn btn-primary" onclick="load_pictures(' + ppage + ')">Предыдущая страница</button>' 
        };

        if (data.next) {
            npage = data.next.split('?page=')[1]
            res += '<button type="button" class="btn btn-primary pull-right" onclick="load_pictures(' + npage + ')">Следующая страница</button>' 
        };

        $('#pictures_block').html(res);
    });
}


$(document).ready(function(){

     $.ajax({
        url: '/account/login',
        type: "GET",
        dataType: "json",
     }).done( function(data) {
         $('#login_and_registration').hide();
         $('#create_picture_block').show();
         $('#username_block').html('Пользователь: ' + data['verbose_name'] + ' <a href="/" onclick="$.post(\'/account/logout\')">[Выйти]</a>');
         console.log(data)
     }).fail( function(data) {
         $('#create_picture_block').hide();
     });

    load_pictures ();

    $('#login_btn').click(function() {
        data = {
            username: $('#input_username').val(),
            password: $('#input_password').val()
        }

        $.ajax({
            url: '/account/login',
            type: "POST",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(data)
        }).done( function(data) {
            document.location = '/';
        }).fail( function(data) {
            if (data.status == 400) {
                $('.form_error').remove();
                errors = $.parseJSON(data.responseText)
                $.each(Object.keys(errors), function( index, value ) {
                    $('#input_' + value).after('<span class="form_error">' + errors[value].join(' ') + '</span>')
                });
                if (errors['non_field_errors'] != undefined) {
                    $('#input_username').parent().parent().before('<span class="form_error">'+ errors['non_field_errors'].join(' ') + '</span>');
                };
            };
        });
    });


    $('#registration_btn').click(function() {
        data = {
            email: $('#input_email').val(),
            new_password1: $('#input_new_password1').val(),
            new_password2: $('#input_new_password2').val()
        }

        $.ajax({
            url: '/account/registration',
            type: "POST",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(data)
        }).done( function(data) {
            alert('Вы успешно зарегистрировались и теперь можете залогиниться');
            document.location = '/'
        }).fail( function(data) {
            if (data.status == 400) {
                $('.form_error').remove();
                errors = $.parseJSON(data.responseText)
                $.each(Object.keys(errors), function( index, value ) {
                    $('#input_' + value).after('<span class="form_error">' + errors[value].join(' ') + '</span>')
                });
            };
        });
    });

    $.extend( true, jQuery.fn, {        
        imagePreview: function( options ){          
            var defaults = {};
            if( options ){
                $.extend( true, defaults, options );
            }
            $.each( this, function(){
                var $this = $( this );              
                $this.bind( 'change', function( evt ){

                    var files = evt.target.files; // FileList object
                    // Loop through the FileList and render image files as thumbnails.
                    for (var i = 0, f; f = files[i]; i++) {
                        // Only process image files.
                        if (!f.type.match('image.*')) {
                        continue;
                        }
                        var reader = new FileReader();
                        // Closure to capture the file information.
                        reader.onload = (function(theFile) {
                            return function(e) {
                                // Render thumbnail.
                                    $('#imageURL').attr('src',e.target.result);                         
                            };
                        })(f);
                        // Read in the image file as a data URL.
                        reader.readAsDataURL(f);
                    }

                });
            });
        }   
    });

    $('#input_picture').imagePreview();

    $('#picture_btn').click(function() {
        data = {
            title: $('#input_title').val(),
            picture: { url: $('#imageURL').attr('src')},
        }

        $.ajax({
            url: '/picture/picture/',
            type: "POST",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(data)
        }).done( function(data) {
            document.location = '/';
        }).fail( function(data) {
            if (data.status == 400) {
                $('.form_error').remove();
                errors = $.parseJSON(data.responseText)
                $.each(Object.keys(errors), function( index, value ) {
                    $('#input_' + value).after('<span class="form_error">' + errors[value].join(' ') + '</span>')
                });
            };
        });
    });
});
