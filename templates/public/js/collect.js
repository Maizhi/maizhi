var xmlHttp; 

function createXMLRequest(){
	if(window.ActiveXObject){
		xmlHttp=new ActiveXObject("Microsoft.XMLHttp");
	} else if(window.XMLHttpRequest){
		xmlHttp=new XMLHttpRequest();
	}
}

function collect(topic,status){   
	createXMLRequest();                
	xmlHttp.open("GET","http://192.168.1.120:8866/groups/topic/collect/?id="+topic);
	xmlHttp.onreadystatechange=handleStateChange(status);
	xmlHttp.send(); 
}

function handleStateChange(status){
	if(xmlHttp.readyState==4 && xmlHttp.status==200){
		if(status==1){
			document.getElementById('collect').style.display='block';
			document.getElementById('abord').style.display='none';

		} else if(status==2){
			document.getElementById('collect').style.display='none';
			document.getElementById('abord').style.display='block';
		}
	} else {
		if(status==1){
			document.getElementById('collect').style.display='block';
			document.getElementById('abord').style.display='none';

		} else if(status==2){
			document.getElementById('collect').style.display='none';
			document.getElementById('abord').style.display='block';
		}
	}
}
