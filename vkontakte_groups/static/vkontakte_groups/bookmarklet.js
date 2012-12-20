(function(){

    // the minimum version of jQuery we want
    var v = "1.7.1";

    // check prior inclusion and version
    if (window.jQuery === undefined || window.jQuery.fn.jquery < v) {
        var done = false;
        var script = document.createElement("script");
        script.src = "http://ajax.googleapis.com/ajax/libs/jquery/" + v + "/jquery.min.js";
        script.onload = script.onreadystatechange = function(){
            if (!done && (!this.readyState || this.readyState == "loaded" || this.readyState == "complete")) {
                done = true;
                initMyBookmarklet();
            }
        };
        document.getElementsByTagName("head")[0].appendChild(script);
    } else {
        initMyBookmarklet();
    }

    function initMyBookmarklet() {
        (window.myBookmarklet = function() {
            function win2utf8(s) {
                var tr = new Array(1026,1027,8218,1107,8222,8230,8224,8225,8364,8240,1033,8249,1034,1036,1035,1039,1106,8216,8217,8220,8221,8226,8211,8212,152,8482,1113,8250,1114,1116,1115,1119,160,1038,1118,1032,164,1168,166,167,1025,169,1028,171,172,173,174,1031,176,177,1030,1110,1169,181,182,183,1105,8470,1108,187,1112,1029,1109,1111,1040,1041,1042,1043,1044,1045,1046,1047,1048,1049,1050,1051,1052,1053,1054,1055,1056,1057,1058,1059,1060,1061,1062,1063,1064,1065,1066,1067,1068,1069,1070,1071,1072,1073,1074,1075,1076,1077,1078,1079,1080,1081,1082,1083,1084,1085,1086,1087,1088,1089,1090,1091,1092,1093,1094,1095,1096,1097,1098,1099,1100,1101,1102,1103);
                s = encodeURI(s);
                var test = /%([0-9ABCDEF]{2})/g;    //Initialize pattern.
                return(s.replace(test, function($0,$1,$2) {
                    return( (parseInt($1,16) >= 128 ) ? String.fromCharCode(tr[(parseInt($1,16)-128)]) : String.fromCharCode(parseInt($1,16)));
                }));
            }
            $("body").append('\
                <div id="bookmarklet">\
                    <form id="bookmarkletForm" action="http://socialcommunications.ru/groups/statistic/import/" method="post"> \
                        <input type="hidden" name="url" value="'+ document.location.href +'" /> \
                        <textarea name="body">'+ win2utf8($('body').html()) +'</textarea>\
                    </form>\
                </div>');
            $('#bookmarkletForm').submit();
        })();
    }
})();