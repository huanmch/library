$(document).ready(function() {

    $("input[name='register']").click(function(){
        var b=1;
        if (isChineseChar($("input[name='name']").val())==0 ) {
            $("div[name='jspointout']").empty().append("姓名必须填写且为中文").css("color","red");
            b=0;
        }
        else {register();}
     });

    $("input[name='name']").focus(function(){
        $("div[name='jspointout']").empty().append("姓名必须为中文").css("color","red");
    });
    $("input[name='name']").blur(function(){
        a=$("input[name='name']").val();
        if(a){
            if (isChineseChar(a)){
                $("div[name='jspointout']").empty();
            }
            else{
                $("div[name='jspointout']").empty().append("姓名必须为中文").css("color","red");
            };
        }
        else{
            $("div[name='jspointout']").empty().append("姓名必须填写").css("color","red");
        }
    })
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
            group: $("select[name='group']").val()
        },
        dataType: "text",
        error: function() {
            alert('失败');
        },
        success: function(data) {
            if (data=='usernamesame'){$("div[name='jspointout']").empty().append("用户名已存在").css("color","red") ;}
            else if (data=='pwnull'){$("div[name='jspointout']").empty().append("密码不能为空").css("color","red") ;}
            else if (data=='telnull'){$("div[name='jspointout']").empty().append("联系方式不能为空").css("color","red") ;}
            else if (data=='namenull'){$("div[name='jspointout']").empty().append("姓名不能为空").css("color","red") ;}
            else if (data=='groupnull'){$("div[name='jspointout']").empty().append("请选择部门").css("color","red") ;}
            else if (data=='T'){window.location.assign('/library/nav/');}
        }
    })
}

function isChineseChar(str){   //检测是否为中文
   var reg = /^[\u4E00-\u9FA5\uF900-\uFA2D]+$/;
   return reg.test(str);
}
