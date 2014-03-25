var xmlHttp; 

function createXMLRequest(){
	if(window.ActiveXObject){
		xmlHttp=new ActiveXObject("Microsoft.XMLHttp");
	} else if(window.XMLHttpRequest){
		xmlHttp=new XMLHttpRequest();
	}
}

function join(id){   
	createXMLRequest();                       
	var url="http://192.168.1.120:8866/groups/join/?id="+id;
	xmlHttp.open("GET",url);
	xmlHttp.onreadystatechange=function(){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			if(xmlHttp.responseText==1){
				document.getElementById('join'+id).checked=false;
			}
		}
	};
	xmlHttp.send(); 
}
