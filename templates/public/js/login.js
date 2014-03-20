var xmlHttp; 

function createXMLRequest(){
	if(window.ActiveXObject){
		xmlHttp=new ActiveXObject("Microsoft.XMLHttp");
	} else if(window.XMLHttpRequest){
		xmlHttp=new XMLHttpRequest();
	}
}

function query(){
	var name=document.getElementById("name").value;
	var email=document.getElementById("email").value;
	var password=document.getElementById("password").value;
	var result="name="+name+"&email="+email+"&password="+password;
    return	result;
}

function query2(){
	var email2=document.getElementById("email2").value;
	var password2=document.getElementById("password2").value;
	var result="&email2="+email2+"&password2="+password2;
	localStorage.setItem('EDU_auth',email2+','+password2)
    return	result;
}

function regi(){   
	createXMLRequest();                       
	var url="http://192.168.1.113:8866/register/?";
	url+=query();
	xmlHttp.open("GET",url);
	xmlHttp.onreadystatechange=handleStateChange;
	xmlHttp.send(); 
}

function handleStateChange(){
	var rtn=document.getElementById("log");
	if(xmlHttp.readyState==4 && xmlHttp.status==200){
		if(isNaN(xmlHttp.responseText)){
			rtn.innerHTML=xmlHttp.responseText;
			rtn.style.color='orange'
		} else {
			window.location="http://192.168.1.113:8866/addmajor/";
		}
	}
}

function handleStateChange2(){
	var rtn=document.getElementById("login");
	if(xmlHttp.readyState==4 && xmlHttp.status==200){
		if(isNaN(xmlHttp.responseText)){
			rtn.innerHTML=xmlHttp.responseText;
			rtn.style.color='orange'
		} else {
			window.location="http://192.168.1.113:8866/users/";
		}
	}
}

function localLogin(email,pwd){
	var result="email2="+email+"&password2="+pwd;
	createXMLRequest();
	var url="http://192.168.1.113:8866/login/?";
	url+=result;
	xmlHttp.open("GET",url)
	xmlHttp.onreadystatechange=function(){
		var rtn=document.getElementById("login");
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			if(isNaN(xmlHttp.responseText)){
				rtn.innerHTML=xmlHttp.responseText;
				rtn.style.color='orange'
			} else {
				window.location="http://192.168.1.113:8866/users/";
			}
		}
	};
	xmlHttp.send(); 
}

function login(){   
	createXMLRequest();                       
	var url="http://192.168.1.113:8866/login/?";
	url+=query2();
	xmlHttp.open("GET",url);
	xmlHttp.onreadystatechange=handleStateChange2;
	xmlHttp.send(); 
}
