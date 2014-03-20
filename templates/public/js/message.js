function connect(id){
	createXMLRequest();                       
	var message=document.getElementById("message").value;
	var url="http://192.168.1.120:8866/users/message/?message="+message+"&to"+id;
	xmlHttp.open("GET",url);
	xmlHttp.onreadystatechange=function(){
	if(xmlHttp.readyState==4 && xmlHttp.status==200){
		result=document.getElementById('messageresult')
		result.innerHTML=xmlHttp.responseText;
		result.style.color='orange'
	};
	xmlHttp.send(); 
}