var xmlHttp; 

function createXMLRequest(){
	if(window.ActiveXObject){
		xmlHttp=new ActiveXObject("Microsoft.XMLHttp");
	} else if(window.XMLHttpRequest){
		xmlHttp=new XMLHttpRequest();
	}
}

function queryNews(){
	var news=document.getElementById("news").value;
	var result="news="+news+"&img="+imgs;
    return	result;
}


function push(){   
	createXMLRequest();                       
	var url="http://192.168.1.120:8866/users/publish/";
	var news=document.getElementById("news").value;
	xmlHttp.open("POST","http://192.168.1.120:8866/users/publish/");
	xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	xmlHttp.onreadystatechange=handleStateChange;
	if(imgs){
		imgs=imgs.replace(/\+/g,"*")
		xmlHttp.send('news='+news+'&img='+imgs); 
	} else {
		xmlHttp.send('news='+news); 
	}
	document.getElementById('list').innerHTML="";
	document.getElementById('file').value="";
	add_pic()
}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !="") {
		var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function handleStateChange(e){
	var rtn=document.getElementById("log");
	if(xmlHttp.readyState==4 && xmlHttp.status==200){
		if(xmlHttp.responseText==1){
			document.getElementById('news').value="";
			e.preventDefault();
    		$.scojs_message('您的新鲜事发布成功！', $.scojs_message.TYPE_OK);
		} else if(xmlHttp.responseText==0) {
			e.preventDefault();
    		$.scojs_message('服务器出错啦～ ：）', $.scojs_message.TYPE_ERROR);
		}
	} else {
		e.preventDefault();
    	$.scojs_message('服务器有小怪兽在捣乱～我们正在尽力捕捉～ ：）', $.scojs_message.TYPE_ERROR);
	}
}



/*
var comment_time=null;
function comment(a)
{
	if(comment_time!=null){
		clearTimeout(comment_time);
	}
	comment_time=setTimeout(function(){
		$("#comment"+a).toggle("slow");
	},200);



}*/
