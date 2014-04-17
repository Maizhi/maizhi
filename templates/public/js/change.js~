var xmlHttp; 

function createXMLRequest(){
	if(window.ActiveXObject){
		xmlHttp=new ActiveXObject("Microsoft.XMLHttp");
	} else if(window.XMLHttpRequest){
		xmlHttp=new XMLHttpRequest();
	}
}

function change(id){   
	createXMLRequest();     
	var intro=document.getElementById('intro').value;  
	var url="http://192.168.1.120:8866/groups/change/?id="+id+"&intro="+intro;
	xmlHttp.open("GET",url);
	xmlHttp.onreadystatechange=function(){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			if(xmlHttp.responseText==1){
				document.getElementById('groupintro').innerHTML=intro;
			}
		}
	};
	xmlHttp.send(); 
}
