var xmlHttp; 

function createXMLRequest(){
	if(window.ActiveXObject){
		xmlHttp=new ActiveXObject("Microsoft.XMLHttp");
	} else if(window.XMLHttpRequest){
		xmlHttp=new XMLHttpRequest();
	}
}

function add(u_id){   
	createXMLRequest();                       
	var url="http://192.168.1.120:8866/users/add/?id="+u_id;
	xmlHttp.open("GET",url);
	var this_btn=document.getElementById('add'+u_id)
	var that_btn=document.getElementById('abord'+u_id)
	xmlHttp.onreadystatechange=function(){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			if(xmlHttp.responseText==1){
				this_btn.style.display='none';
				that_btn.style.display='inline';
			}
		}
	};
	xmlHttp.send(); 
}
