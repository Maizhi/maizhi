function connected(id){
	createXMLRequest();                       
	var message=document.getElementById("message"+id).value;
	var messageurl="http://192.168.1.120:8866/users/message/?message="+message+"&to="+id;
	xmlHttp.open('get',messageurl);
	xmlHttp.onreadystatechange=response(id);
	xmlHttp.send(); 
}

function response(id){
	if(xmlHttp.readyState==4 && xmlHttp.status==200){
<<<<<<< HEAD
		$('#myModal'+id).modal('hide');
		
	} else {
		$('#myModal'+id).modal('hide');
	}
=======
		result=document.getElementById('messageresult'+id);
		result.innerHTML=xmlHttp.responseText;
		result.style.color='orange';
		$("#myModal"+id).modal('hide');
	};
>>>>>>> 3eb4f14e2f51d1bc534b6bae85233d2f1fb63614
}
