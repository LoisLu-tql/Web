window.onload = function(){
    var blogs = document.getElementsByClassName("blog") ;
    for(var i = 0 ; i < blogs.length ; i++){
        console.log(blogs[i]) ;
        blogs[i].onclick = function () {
            location.href = '/article/' + this.getAttribute("blog_id") ;
        }
    }
};