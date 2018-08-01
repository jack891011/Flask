function my()
{
x=document.getElementById("de");  // 找到元素
x.style.color="blue"
x.innerHTML="3366";    // 改变内容
}

function my1() {
x=document.getElementById("de")
x.style.color="red"
x.innerHTML="QQzone";}

function f1(a,b)
{
	alert("从"+a+"到"+b+"的距离为:50KM");
}
function f2()
{
	x=document.getElementById("idc");
	x.innerHTML="加载中...";
	document.getElementById('idc').style.color="blue";
	
}

function f3()
{var l=[5,4,3,2,1];
for (x in l)
	{
		document.write(l[x]+"</br>");
		
	}

	
}