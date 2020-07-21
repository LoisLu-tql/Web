/*
$(function() {
    // 添加新的用户标签
    var $label_button = $("#add_label_button");
    var lid = 0 ;
    $label_button.click(function () {
        var label_name = $("#label_name").val().trim();
        if (label_name.length > 15) {
            $("#add_label_info").text("标签字数过多!").css('color', 'red');
        } else if (!label_name.length) {
            $("#add_label_info").text("标签不能为空!").css('color', 'red');
        } else {
            $.getJSON("/addlabel/", {'labelname': label_name}, function (data) {
                var $add_label_info = $("#add_label_info");
                if (data['status'] === 200) {
                    $add_label_info.text("标签添加成功").css('color', 'green');
                    $("#label_name").val('');
                    $("#ulabels").append('<li>'+label_name+'</li>') ;
                    $("#ulabels").children("li:last-child").click(function () {
                        $("#selectedlabels").append('<li>' + this.innerHTML + '</li>');
                        $("#formlist").append('<input class="ilabel" name="'+(++lid)+'" type="hidden" value="'+this.innerHTML+'">') ;
                        this.remove() ;

                        // 撤销添加的标签
                        $("#selectedlabels").children("li:last-child").click(function () {
                            $("#ulabels").append('<li>'+this.innerHTML+'</li>') ;
                            $("#ulabels").children("li:last-child").click(function () {
                                $("#selectedlabels").append('<li>' + this.innerHTML + '</li>');
                                this.remove() ;
                            })
                            $(".ilabel").each(function () {
                                console.log(this.val) ;
                            })
                        })

                    })
                } else if (data['status'] === 901) {
                    $add_label_info.text("该标签已存在").css('color', 'red');
                }
            })
        }
    })

    // 为博客添加标签
    var ulabels = document.getElementsByClassName("userlabels");
    var $slabels = $("#selectedlabels");   //  这里必须要写jquery,因为原生js中没有append()函数
    // console.log(ulabels.length) ;
    for (var i = 0; i < ulabels.length; i++) {
        // console.log(ulabels[i].innerHTML) ;
        ulabels[i].onclick = function () {
            console.log(this.innerHTML);
            $slabels.append('<li>' + this.innerHTML + '</li>');
            $("#formlist").append('<input name="'+(++lid)+'" type="hidden" value="'+this.innerHTML+'">') ;
            // var $newlabel = $slabels.children()[$slabels.length-1] ;
            // console.log($newlabel) ;
            this.parentNode.removeChild(this);

            // 撤销添加的标签
            $slabels.children("li:last-child").click(function () {
                $("#ulabels").append('<li>'+this.innerHTML+'</li>') ;
                $("#ulabels").children("li:last-child").click(function () {
                    $("#selectedlabels").append('<li>' + this.innerHTML + '</li>');
                    this.parentNode.removeChild(this);
                })
                this.remove() ;
            })
        }
    }

    // 撤销添加的博客标签
    // $("#backout").click(function () {
    //     console.log($slabels.children("li:last-child").text()) ;
    //     $slabels.children("li:last-child").remove() ;
    // })
});
*/

$(function() {
    // 添加新的用户标签
    var $label_button = $("#add_label_button");
    var lid = 0 ;
    $label_button.click(function () {
        var label_name = $("#label_name").val().trim();
        if (label_name.length > 15) {
            $("#add_label_info").text("标签字数过多!").css('color', 'red');
        } else if (!label_name.length) {
            $("#add_label_info").text("标签不能为空!").css('color', 'red');
        } else {
            $.getJSON("/addlabel/", {'labelname': label_name}, function (data) {
                var $add_label_info = $("#add_label_info");
                if (data['status'] === 200) {
                    $add_label_info.text("标签添加成功").css('color', 'green');
                    $("#label_name").val('');
                    $("#ulabels").append('<li class="userlabels not_selected">'+label_name+'</li>') ;
                    $("#ulabels").children("li:last-child").click(function () {
                        console.log($(this).css("border-bottom")) ;
                        if($(this).css("border-bottom") == "0px none rgb(51, 51, 51)"){
                            $(this).css("border-bottom","1px solid rgb(51, 51, 51)") ;
                        } else{
                            $(this).css("border-bottom","0px none rgb(51, 51, 51)") ;
                        }
                    })
                } else if (data['status'] === 901) {
                    $add_label_info.text("该标签已存在").css('color', 'red');
                }
            })
        }
    })
});

$(".userlabels").each(function () {
    $(this).click(function () {
        console.log($(this).css("border-bottom")) ;
        if($(this).css("border-bottom") == "0px none rgb(51, 51, 51)"){
            $(this).css("border-bottom","1px solid rgb(51, 51, 51)") ;
        } else{
            $(this).css("border-bottom","0px none rgb(51, 51, 51)") ;
        }
    })
})

function check() {
    var tot_label = 0 ;
    $(".userlabels").each(function () {
        if($(this).css("border-bottom") == "1px solid rgb(51, 51, 51)"){
            var l_content = $(this).text() ;
            var l_name = "ulabel"+(++tot_label) ;
            $("#formlist").append('<input type="text">') ;
            $("#formlist").children("input:last-child").val(l_content) ;
            $("#formlist").children("input:last-child").attr('name',l_name) ;
        }
    })
    $("#formlist").append('<input type="text" value=tot_label name="tot_label">') ;
    $("#formlist").children("input:last-child").val(tot_label) ;
    $("#formlist").children("input:last-child").attr('name','tot_label') ;
    return true ;
}


