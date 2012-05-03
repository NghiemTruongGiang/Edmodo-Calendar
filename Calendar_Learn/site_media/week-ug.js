var c=2;
var a= 0;
var t;
var timer_is_on=0;
var today=new Date();
var h=today.getHours();
var m=today.getMinutes();
var sum = 60 * h + m;
var k = 50;

function timedCount(){
	document.getElementById('txt').value=a;
	a = a + 1;
    k = k + c * a;
	t=setTimeout("timedCount()",10000);
	window.scrollTo(k,k);
}

function doTimer(){
	if (!timer_is_on){
		timer_is_on=1;
		window.scrollTo(50 ,30);
  		timedCount();
  	}
}
<input type="button" value="Start count!" onClick="doTimer()">
<input type="text" id="txt">