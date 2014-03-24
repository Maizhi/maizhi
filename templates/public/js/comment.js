function comment(id){
	createXMLRequest();                       
	var content=document.getElementById("content"+id).value;
	var url="http://192.168.1.120:8866/users/comment/?content="+content;
	xmlHttp.open("GET",url);
	xmlHttp.onreadystatechange=function(){
		
	};
	xmlHttp.send(); 
}