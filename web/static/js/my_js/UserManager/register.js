// 用户名预校验
$(function () {
    var $username = $("#username") ;
    $username.change(function(){
        var username = $username.val().trim() ;
        if(username.length < 6) {
            $("#username_info").text("用户名字数过少").css('color', 'red') ;
        }
        if(username.length >= 6) {
            $.getJSON("/checkusername/", {'username':username}, function(data){
//                console.log(data) ; // 调试用
                var $username_info = $("#username_info") ;
                if(data['status'] === 200) {
                    $username_info.text("用户名可用").css('color', 'green') ;
                } else if(data['status'] === 901) {
                    $username_info.text("用户名不可用").css('color','red') ;
                }
            })
        }
    })
})

// 限制表单提交条件 （用户名合法等）
function check(){
    var $username_info = $("#username_info") ;
    var username = $("#username").val().trim() ;
    if(username.length < 6) return false ;
    if($username_info.css('color') == 'red') return false ;
    return true ;
}