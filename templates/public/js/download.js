var xmlHttp; 

function createXMLRequest(){
	if(window.ActiveXObject){
		xmlHttp=new ActiveXObject("Microsoft.XMLHttp");
	} else if(window.XMLHttpRequest){
		xmlHttp=new XMLHttpRequest();
	}
}

function downloads(file){   
	createXMLRequest();                
	xmlHttp.open("GET","http://192.168.1.120:8866/groups/the/download/down/?id="+file);
	xmlHttp.onreadystatechange=function(file){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			document.getElementById('down_con'+file).innerHTML+=1;
		}
	};
	xmlHttp.send(null); 
}
