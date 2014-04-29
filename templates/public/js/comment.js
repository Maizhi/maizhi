
function comment_t(id){
	createXMLRequest();                       
	var content=document.getElementById("comment_tarea"+id).value;
	var url="http://192.168.1.120:8866/users/comment/?content="+content+"&news_id="+id;
	xmlHttp.open("GET",url);
	xmlHttp.onreadystatechange=function(){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
				$('#comment_tarea'+id).val('');
				//$("#comment"+id).css("display","none");
				
				re_news_array=xmlHttp.responseText.split(',');
				//alert(re_news_array[0]+'----'+re_news_array[4]+'----'+re_news_array[1]);
				var str1='<div class="pull-left comment_img"><a href="http://192.168.1.120:8866/users/home/';
				var str2='"><img src="http://mzhead.qiniudn.com/';
				var str3='" class="img-circle" width="100%"></a></div><div class="pull-left comment_content"><div><div class="pull-left"><a href="http://192.168.1.120:8866/users/home/';
				var str4='"><b>';
				var str5='</b></a></div><div class="pull-right comment_time">刚刚更新</div><div class="clearfix"></div></div><div class="comment_concontent">';
				var str6='</div><div class="pull-right"><span class="span_news"><a href="javascript:void(0)" onclick="cogood(';
				var str7=')"><i class="icon-thumbs-up"></i> <span id="cogood';
				var str8='">';
				var str9='</span></a></span><span class="span_news"><a href="javascript:void(0)" onclick="cocomment(';
				var str10=',\''+re_news_array[4]+'\','+re_news_array[8]+',';
				var str11=');"><i class="icon-comment"></i> <span id="cocomment_span';
				var str12='">';
				var str13='</a></span></span></div></div><div class="clearfix"></div>';
				var strFinal=str1+re_news_array[3]+str2+re_news_array[5]+str3+re_news_array[3]+str4+re_news_array[4]+str5+re_news_array[2]+str6+re_news_array[0]+str7+re_news_array[0]+str8+re_news_array[6]+str9+re_news_array[0]+str10+re_news_array[1]+str11+re_news_array[0]+str12+re_news_array[7]+str13;
				$("#first_commend"+id).html(strFinal);
				$("#see_more_re"+re_news_array[1]).html('<a href="javascript:void(0)" onclick="get_more_re('+re_news_array[1]+');">查看更多评论</a>');
				$("#review"+id).html(parseInt($("#review"+id).html())+1);
		}		
	};
	xmlHttp.send(); 
}

 




function cocomment(re_id,name,to,news_id)
{
	//$("#cocomment"+id).toggle();
	$("#comment_tarea"+news_id).val("回复"+name+":");
	$("#coAndcocomment"+news_id).html('<button type="button" class="btn btn-info comment_act_btn" onclick="cocomment_t('+news_id+','+re_id+','+to+');">评论</button>');
	$("#see_more_re"+news_id).html('<a href="javascript:void(0)" onclick="get_more_re('+news_id+');">查看更多评论</a>');
	$(window).scrollTop($("#redirect"+news_id).offset().top-200);
	//alert($(window).scrollTop());
	//alert($("#redirect"+news_id).offset().top);
}

function cocomment_t(news_id,re_id,to)
{//alert(news_id+'---'+re_id+'---'+to);
	createXMLRequest();                       
	var content=document.getElementById("comment_tarea"+news_id).value;
	var url="http://192.168.1.120:8866/users/cocomment/?content="+content+"&news_id="+news_id+"&re_id="+re_id+"&to="+to;
	xmlHttp.open("GET",url);
	xmlHttp.onreadystatechange=function(){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
				$('#comment_tarea'+news_id).val('');
				//$("#comment"+id).css("display","none");
				
				re_news_array=xmlHttp.responseText.split(',');
				//alert(re_news_array[0]+'----'+re_news_array[4]+'----'+re_news_array[1]);
				var str1='<div class="pull-left comment_img"><a href="http://192.168.1.120:8866/users/home/';
				var str2='"><img src="http://mzhead.qiniudn.com/';
				var str3='" class="img-circle" width="100%"></a></div><div class="pull-left comment_content"><div><div class="pull-left"><a href="http://192.168.1.109:8866/users/home/';
				var str4='"><b>';
				var str5='</b></a></div><div class="pull-right comment_time">刚刚更新</div><div class="clearfix"></div></div><div class="comment_concontent">';
				var str6='</div><div class="pull-right"><span class="span_news"><a href="javascript:void(0)" onclick="cogood(';
				var str7=')"><i class="icon-thumbs-up"></i> <span id="cogood';
				var str8='">';
				var str9='</span></a></span><span class="span_news"><a href="javascript:void(0)" onclick="cocomment(';
				var str10=',\''+re_news_array[4]+'\','+re_news_array[8]+',';
				var str11=');"><i class="icon-comment"></i> <span id="cocomment_span';
				var str12='">';
				var str13='</a></span></span></div></div><div class="clearfix"></div>';
				var strFinal=str1+re_news_array[3]+str2+re_news_array[5]+str3+re_news_array[3]+str4+re_news_array[4]+str5+re_news_array[2]+str6+re_news_array[0]+str7+re_news_array[0]+str8+re_news_array[6]+str9+re_news_array[0]+str10+re_news_array[1]+str11+re_news_array[0]+str12+re_news_array[7]+str13;
				$("#first_commend"+news_id).html(strFinal);
				
				$("#review"+news_id).html(parseInt($("#review"+news_id).html())+1);
		}		
	};
	xmlHttp.send(); 
}


function get_more_re(news_id)
{
	createXMLRequest();                       
	var content=document.getElementById("comment_tarea"+news_id).value;
	var url="http://192.168.1.120:8866/users/get_more_re/?&news_id="+news_id;
	xmlHttp.open("GET",url);
	xmlHttp.onreadystatechange=function(){
		if(xmlHttp.readyState==4 && xmlHttp.status==200){
				//alert(xmlHttp.responseText);
				re_news_big_array=xmlHttp.responseText.split('*');
				var strFinal='';
				$.each(re_news_big_array, function(i,val){      
					    re_news_array=val.split(',');
					    if(re_news_array[7]!=undefined)
					    {
						    var str1='<div class="comment_a_style"><div class="pull-left comment_img"><a href="http://192.168.1.120:8866/users/home/';
							var str2='"><img src="http://mzhead.qiniudn.com/';
							var str3='" class="img-circle" width="100%"></a></div><div class="pull-left comment_content"><div><div class="pull-left"><a href="http://192.168.1.109:8866/users/home/';
							var str4='"><b>';
							var str5='</b></a></div><div class="pull-right comment_time">'+re_news_array[9]+'</div><div class="clearfix"></div></div><div class="comment_concontent">';
							var str6='</div><div class="pull-right"><span class="span_news"><a href="javascript:void(0)" onclick="cogood(';
							var str7=')"><i class="icon-thumbs-up"></i> <span id="cogood';
							var str8='">';
							var str9='</span></a></span><span class="span_news"><a href="javascript:void(0)" onclick="cocomment(';
							var str10=',\''+re_news_array[4]+'\','+re_news_array[8]+',';
							var str11=');"><i class="icon-comment"></i> <span id="cocomment_span';
							var str12='">';
							var str13='</a></span></span></div></div><div class="clearfix"></div></div>';
							strFinal=strFinal+str1+re_news_array[3]+str2+re_news_array[5]+str3+re_news_array[3]+str4+re_news_array[4]+str5+re_news_array[2]+str6+re_news_array[0]+str7+re_news_array[0]+str8+re_news_array[6]+str9+re_news_array[0]+str10+re_news_array[1]+str11+re_news_array[0]+str12+re_news_array[7]+str13;
							 
						}
				
				  });  
				$("#first_commend"+news_id).html(strFinal);
				$("#see_more_re"+news_id).html('<a href="#larger_a'+news_id+'" onclick="no_re('+news_id+');">收起评论</a>');

		}		
	};
	xmlHttp.send(); 
}



//href="#larger_a'+news_id+'"
function no_re(news_id)
{
	$("#comment"+news_id).css("display","none");
}
