function comment_topic(topic){   
	createXMLRequest();               
	var content=document.getElementById('comment').value;
	xmlHttp.open("GET","http://192.168.1.109:8866/groups/topic/comment/?id="+topic+"&content="+content);
	xmlHttp.onreadystatechange=function(e){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			re_array=xmlHttp.responseText.split(',');
			var str1='<div id="ajax_comment"></div><div style="margin-top:20px;"><div class="commentDiv1 pull-left"><img src="../avatar/'+re_array[1]+'" class="img-circle" width="100%"/></div>';
	        var str2='<div class="pull-left commentDiv2"><div class="topdirection_left pull-left"></div><div class="commentDiv21 pull-left">';
	        var str3='<div><div class="pull-left time">'+re_array[2]+'</div><div class="pull-right time">刚刚更新</div><div class="clearfix"></div></div>';
	        var str4='<div>'+content+'</div><div style="text-align:right;">';
	        var str5='<span class="span_news"><a href="javascript:void(0)" onclick="clickgood('+re_array[0]+')"><i class="icon-thumbs-up"></i> <span id="good'+re_array[0]+'">'+re_array[4]+'</span></a></span>';
	        var str6='<span class="span_news"><a href="javascript:void(0)" onclick="topic_cocomment('+re_array[0]+',\''+re_array[2]+'\');"><i class="icon-comment"></i> <span id="rerecomment_con'+re_array[0]+'">'+re_array[3]+'</span></a></span></div></div><div class="clearfix"></div></div><div class="clearfix"></div></div>';
	        var strr=str1+str2+str3+str4+str5+str6;

			if(isNaN(re_array[0])){
				e.preventDefault();
	    		$.scojs_message('服务器出错啦～ ：）', $.scojs_message.TYPE_ERROR);
			} else {
				$("#ajax_comment").html(strr);
				$("#ajax_comment").removeAttr("id");
				$("#comment").val('');
				$("#group_comment").hide();
				$("#reviewOfTopic_con"+topic).html(parseInt($("#reviewOfTopic_con"+topic).html())+1);
				//alert($("#rerecomment_con"+re_array[0]).html());
				//$("#rerecomment_con"+re_array[0]).html(parseInt($("#rerecomment_con"+re_array[0]).html())+1);
				e.preventDefault();
	    		$.scojs_message('您回复成功！', $.scojs_message.TYPE_OK);
			}
		} else {
			e.preventDefault();
	    	$.scojs_message('服务器有小怪兽在捣乱～我们正在尽力捕捉～ ：）', $.scojs_message.TYPE_ERROR);
		}
	};
	xmlHttp.send(); 
}



function cccomment_topic(topic){   
	createXMLRequest();    
	var re_id=$("#rere_hidden").val();
	var content=document.getElementById('cccomment').value;
	xmlHttp.open("GET","http://192.168.1.109:8866/groups/topic/cccomment/?id="+re_id+"&content="+content);
	xmlHttp.onreadystatechange=function(e){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
			re_array=xmlHttp.responseText.split(',');
			var str1='<div id="ajax_comment"></div><div style="margin-top:20px;"><div class="commentDiv1 pull-left"><img src="../avatar/'+re_array[1]+'" class="img-circle" width="100%"/></div>';
	        var str2='<div class="pull-left commentDiv2"><div class="topdirection_left pull-left"></div><div class="commentDiv21 pull-left">';
	        var str3='<div><div class="pull-left time">'+re_array[2]+'</div><div class="pull-right time">刚刚更新</div><div class="clearfix"></div></div>';
	        var str4='<div>'+content+'</div><div style="text-align:right;">';
	        var str5='<span class="span_news"><a href="javascript:void(0)" onclick="clickgood('+re_array[0]+')"><i class="icon-thumbs-up"></i> <span id="good'+re_array[0]+'">'+re_array[4]+'</span></a></span>';
	        var str6='<span class="span_news"><a href="javascript:void(0)" onclick="topic_cocomment('+re_array[0]+',\''+re_array[2]+'\');"><i class="icon-comment"></i> <span id="rerecomment_con'+re_array[0]+'">'+re_array[3]+'</span></a></span></div></div><div class="clearfix"></div></div><div class="clearfix"></div></div>';
	        var strr=str1+str2+str3+str4+str5+str6;

			if(isNaN(re_array[0])){
				e.preventDefault(); 
	    		$.scojs_message('服务器出错啦～ ：）', $.scojs_message.TYPE_ERROR);
			} else {
				$("#ajax_comment").html(strr);
				$("#ajax_comment").removeAttr("id");
				$("#cccomment").val('');
				$("#group_cccomment").hide();
				$("#reviewOfTopic_con"+topic).html(parseInt($("#reviewOfTopic_con"+topic).html())+1);
				$("#rerecomment_con"+re_id).html(parseInt($("#rerecomment_con"+re_id).html())+1);
				e.preventDefault();
	    		$.scojs_message('您回复成功！', $.scojs_message.TYPE_OK);
	    		alert(re_id);
			}
			
		} /*else {
			e.preventDefault();
	    	$.scojs_message('服务器有小怪兽在捣乱～我们正在尽力捕捉～ ：）', $.scojs_message.TYPE_ERROR);
		}*/
	};
	xmlHttp.send(); 
}









