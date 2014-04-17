function dt(topic){
	createXMLRequest();               
	xmlHttp.open("GET","http://192.168.1.120:8866/groups/topic/dt/?id="+topic);
	xmlHttp.onreadystatechange=function(e){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			e.preventDefault();
	    	$.scojs_message('删除成功！', $.scojs_message.TYPE_OK);
	    } else {
	    	e.preventDefault();
    		$.scojs_message('服务器出错啦～ ：）', $.scojs_message.TYPE_ERROR);
	    }
	};
	xmlHttp.send(); 
}
