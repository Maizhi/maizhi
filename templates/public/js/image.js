
var xmlHttp; 

function createXMLRequest(){
	if(window.XMLHttpRequest){
		xmlHttp=new XMLHttpRequest();
	} else {
		xmlHttp=new ActiveXObject("Microsoft.XMLHttp");
	}
}

onmessage=function(event){
	createXMLRequest();
	var url="http://192.168.1.113:8866/users/getimg/?imgid="+event.data;
	xmlHttp.open("GET",url);
	xmlHttp.onreadystatechange=function(){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			postMessage(xmlHttp.responseText)
		}
	};
	xmlHttp.send(); 
}
