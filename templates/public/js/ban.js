function ban(user){
	createXMLRequest();               
	xmlHttp.open("GET","http://192.168.1.113:8866/groups/topic/ban/?id="+user);
	xmlHttp.onreadystatechange=function(e){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			if(xmlHttp.responseText==1){
				e.preventDefault();
		    	$.scojs_message('您封禁成功！', $.scojs_message.TYPE_OK);
		    	//halert(getClassName('lock'+user))
		    	//getClassName('lock'+user).innerHTML='解封用户';
		    	$(".lock"+user).html('解封用户');
		    	$(".unlock"+user).html('解封用户');
		    } else if (xmlHttp.responseText==2) {
		    	e.preventDefault();
		    	$.scojs_message('您解封成功！', $.scojs_message.TYPE_OK);
		    	//getClassName('lock'+user).innerHTML='封禁用户';
		    	$(".unlock"+user).html('封禁用户');
		    	$(".lock"+user).html('封禁用户');
		    }
	    } else {
	    	e.preventDefault();
    		$.scojs_message('服务器出错啦～ ：）', $.scojs_message.TYPE_ERROR);
	    }
	};
	xmlHttp.send(); 
}

function getClassName(className){
	var nodes=document.getElementsByTagName("*");
	result=[];
	for(var i=0;i<nodes.length;i++){
		if(hasClassName(nodes[i],className)){
			result.push(nodes[i]);	
		}
	}
	return result;
}

function hasClassName(node,className){
	var names=node.className.split(/\s+/);
	for(var i=0;i<names.length;i++){
		if(names[i]==className)	{
			return true;
		} else {
			return false;
		}
	}
}
