$(document).ready(function() {

    $("input[name='register']").click(function(){register();});

})

function register() {//注册按钮
    $.ajax({
        type:"post",
        url:"/library/ajax_register_/",
        async:false,
        data: {
            name: $("input[name='name']").val(),
            username: $("input[name='id']").val(),
            password: $("input[name='pw']").val(),
            tel: $("input[name='tel']").val(),
            group: $("input[name='group']").val()
        },
        dataType: "text",
        error: function() {
            alert('失败');
        },
        success: function() {
            window.location.assign('/library/nav/');
        }
    })
}
