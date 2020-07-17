$(function(){
   $("#like").click(function () {
       var $like = $(this);
       var star_id = $like.attr("star_id");
       var fan_id = $like.attr("fan_id");
       $.get('/addlikerelationship/', {
           'star_id' : star_id,
           'fan_id': fan_id,
       }, function(data){
            if(data['status'] === 200){
                $("#AttentionHint").text("(已关注)") ;
            } else if(data['status'] === 400){
                $("#AttentionHint").text("(已经关注该博主啦！)") ;
            }
       })
   })

    $("#recommend").click(function () {
       var $like = $(this);
       var discussion_id = $like.attr("discussion_id");
       var fan_id = $like.attr("fan_id");
       $.get('/recommenddiscussion/', {
           'discussion_id' : discussion_id,
           'fan_id': fan_id,
       }, function(data){
            if(data['status'] === 200){
                $("#AttentionHint").text("(已点赞)") ;
            } else if(data['status'] === 400){
                $("#AttentionHint").text("(已经点过赞啦！)") ;
            }
       })
   })

    $("#mark").click(function () {
       var $like = $(this);
       var discussion_id = $like.attr("discussion_id");
       var fan_id = $like.attr("fan_id");
       $.get('/markdiscussion/', {
           'discussion_id' : discussion_id,
           'fan_id': fan_id,
       }, function(data){
            if(data['status'] === 200){
                $("#AttentionHint").text("(已收藏)") ;
            } else if(data['status'] === 400){
                $("#AttentionHint").text("(已经收藏过啦！)") ;
            }
       })
   })
});