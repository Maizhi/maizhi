function clickgood(topic){   
	createXMLRequest();                       
	var url="http://192.168.1.120:8866/groups/topic/good/?id="+topic;
	xmlHttp.open("GET",url);
	var count=document.getElementById('good'+topic);
	xmlHttp.onreadystatechange=function(){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			if(xmlHttp.responseText==1){
				count.innerHTML=parseInt(count.innerHTML)+1;
			} else if(xmlHttp.responseText==2){
				count.innerHTML=count.innerHTML;
			}
		}
	};
	xmlHttp.send(); 
}
