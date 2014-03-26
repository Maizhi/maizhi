var xmlHttp; 

function createXMLRequest(){
	if(window.ActiveXObject){
		xmlHttp=new ActiveXObject("Microsoft.XMLHttp");
	} else if(window.XMLHttpRequest){
		xmlHttp=new XMLHttpRequest();
	}
}

function publish(group){   
	createXMLRequest();       
	var title=document.getElementById("title").value;
	var editor=document.getElementById("editor").innerHTML; 
	editor=editor.replace(/\+/g,"*")
	editor=editor.replace(/\;/g,"}")              
	xmlHttp.open("POST","http://192.168.1.120:8866/groups/topic/publish/");
	xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	xmlHttp.onreadystatechange=handleStateChange;
	xmlHttp.send('group='+group+"&title="+title+"&editor="+editor); 
}

function handleStateChange(e){
	if(xmlHttp.readyState==4 && xmlHttp.status==200){
		if(isNaN(xmlHttp.responseText)){
			e.preventDefault();
    		$.scojs_message('服务器出错啦～ ：）', $.scojs_message.TYPE_ERROR);
		} else {
			window.location="http://192.168.1.120:8866/groups/topic/"+xmlHttp.responseText;
		}
	} else {
		e.preventDefault();
    	$.scojs_message('服务器有小怪兽在捣乱～我们正在尽力捕捉～ ：）', $.scojs_message.TYPE_ERROR);
	}
}
