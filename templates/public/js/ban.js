function ban(user){
	createXMLRequest();               
	xmlHttp.open("GET","http://192.168.1.120:8866/groups/topic/ban/?id="+user);
	xmlHttp.onreadystatechange=function(e){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			if(xmlHttp.responseText==1){
				e.preventDefault();
		    	$.scojs_message('您封禁成功！', $.scojs_message.TYPE_OK);
		    } else if (xmlHttp.responseText==2) {
		    	e.preventDefault();
		    	$.scojs_message('您解封成功！', $.scojs_message.TYPE_OK);
		    }
	    } else {
	    	e.preventDefault();
    		$.scojs_message('服务器出错啦～ ：）', $.scojs_message.TYPE_ERROR);
	    }
	};
	xmlHttp.send(); 
}
