$(function() {
    $("#like").click(function () {
        var $like = $(this);
        var star_id = $like.attr("star_id");
        var fan_id = $like.attr("fan_id");
        $.get('/addlikerelationship/', {
            'star_id': star_id,
            'fan_id': fan_id,
        }, function (data) {
            if (data['status'] === 200) {
                $("#AttentionHint").text("(已关注)");
            } else if (data['status'] === 400) {
                $("#AttentionHint").text("(已经关注该博主啦！)");
            }
        })
    })

    $("#unlike").click(function () {
        var $like = $(this);
        var star_id = $like.attr("star_id");
        var fan_id = $like.attr("fan_id");
        $.get('/unlikerelationship/', {
            'star_id': star_id,
            'fan_id': fan_id,
        }, function (data) {
            if (data['status'] === 200) {
                $("#AttentionHint").text("(已取关)");
            } else if (data['status'] === 400) {
                $("#AttentionHint").text("(已经取关该博主啦！)");
            }
        })
    })
});
