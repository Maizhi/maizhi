function connected(id){
	createXMLRequest();                       
	var message=document.getElementById("message"+id).value;
	var messageurl="http://192.168.1.113:8866/users/message/?message="+message+"&to="+id;
	xmlHttp.open('get',messageurl);
	xmlHttp.onreadystatechange=response;
	xmlHttp.send(); 
}

function response(){
	if(xmlHttp.readyState==4 && xmlHttp.status==200){
		result=document.getElementById('messageresult'+id);
		result.innerHTML=xmlHttp.responseText;
		result.style.color='orange';
	} else {
		alert(xmlHttp.readyState+"-------"+xmlHttp.status)
	};
}