function shareTo(id){
	createXMLRequest();                       
	imgurl=document.getElementById('larger'+id).src;
	img=imgurl.split('/');
	var sharemsg=document.getElementById("sharemsg"+id).value;
	var sharemsgeurl="http://192.168.1.120:8866/users/share/?sharemsg="+sharemsg+"&img="+img[5]+"&id="+id;
	xmlHttp.open('GET',sharemsgeurl);
	xmlHttp.onreadystatechange=rtn(id);
	xmlHttp.send(); 
}

function rtn(id){
	if(xmlHttp.readyState==4 && xmlHttp.status==200){
		$("#shareThis"+id).modal('hide');
		count=document.getElementById('share'+id);
		window.location.reload();
		count.innerHTML=parseInt(count.innerHTML)+1;
	} else {
		$("#shareThis"+id).modal('hide');
		count=document.getElementById('share'+id);
		count.innerHTML=parseInt(count.innerHTML)+1;
		window.location.reload();
	}
}
