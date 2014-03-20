function connected(id){
	createXMLRequest();                       
	var message=document.getElementById("message"+id).value;
	var messageurl="http://192.168.1.113:8866/users/message/?message="+message+"&to="+id;
	xmlHttp.open('get',messageurl);
	xmlHttp.onreadystatechange=response(id);
	xmlHttp.send(); 
}

function response(id){
	if(xmlHttp.readyState==4 && xmlHttp.status==200){
		$('#myModal'+id).modal('hide');
	};
}