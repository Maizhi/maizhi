function comment_topic(topic){   
	createXMLRequest();               
	var content=document.getElementById('comment').value 
	xmlHttp.open("GET","http://192.168.1.120:8866/groups/topic/comment/?id="+topic+"&content="+content);
	xmlHttp.onreadystatechange=result;
	xmlHttp.send(); 
}

function result(e){
	if(xmlHttp.readyState==4 && xmlHttp.status==200){
		if(isNaN(xmlHttp.responseText)){
			e.preventDefault();
    		$.scojs_message('服务器出错啦～ ：）', $.scojs_message.TYPE_ERROR);
		} else {
			e.preventDefault();
    		$.scojs_message('您回复成功！', $.scojs_message.TYPE_OK);
		}
	} else {
		e.preventDefault();
    	$.scojs_message('服务器有小怪兽在捣乱～我们正在尽力捕捉～ ：）', $.scojs_message.TYPE_ERROR);
	}
}
