function clickgood(num){   
	createXMLRequest();                       
	var url="http://192.168.1.113:8866/users/good/?newsid="+num;
	xmlHttp.open("GET",url);
	xmlHttp.onreadystatechange=function(){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			if(xmlHttp.responseText==1){
				var count=document.getElementById('good'+num);
				count.innerHTML=parseInt(count.innerHTML)+1;
			} else if(xmlHttp.responseText==2){
				count.innerHTML+=0;
			}
		} else {
			count.innerHTML+=0;
		}
	};
	xmlHttp.send(); 
}
