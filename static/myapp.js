// scan前準備
$(".scan").on("click", function(){
    window.location.href = "/scan";
});

$(window).on("load", function(){
    // "/" をデコードする
    // "/" はURIで特殊な意味合いをもつので、デコードするべきではないかもしれない
    var url = decodeURIComponent($(location).attr("href"));
    var arr = url.split("=");
    if(arr.length <= 0) return;

    var code = arr[1];
    $("#code").val(code);
});