$(document).ready(function() {

    $("input[name='login']").click(function(){login();});
    $("input[name='pw']").keydown(function (key) {
        var e = window.event || arguments.callee.caller.arguments[0];
        if (e && e.keyCode == 13) {
            login();
        }
    })
});

function login() { //登录按钮
    $.ajax({
        type:"post",
        url:"/library/ajax_index_/",
        async: false,
        data: {
            username: $("input[name='id']").val(),
            password: $("input[name='pw']").val()
        },
        dataType: "text",
        error: function() {
            alert('登录失败');
        },
        success: function(data) {
            if (data == 0) {
                alert('登录成功');
                window.location.assign('/library/nav/');
            } else {
                if (data == 1) {alert('用户未认证或密码错误')}
                else {
                    if (data == 2) {alert('用户名不存在')}
                    else {
                        if (data == 3) {alert('内部错误')}
                        //else alert('登录失败')
                    }
                }
            }
        }
    })
}
