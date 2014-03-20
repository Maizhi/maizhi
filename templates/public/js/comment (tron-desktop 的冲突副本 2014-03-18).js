function comment(id){
	createXMLRequest();                       
	var url="http://192.168.1.113:8866/users/publish/";
	var news=document.getElementById("news").value;
	xmlHttp.open("POST","http://192.168.1.113:8866/users/publish/");
	xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	xmlHttp.onreadystatechange=handleStateChange;
	imgs=imgs.replace(/\+/g,"*")
	xmlHttp.send('news='+news+'&img='+imgs); 
}