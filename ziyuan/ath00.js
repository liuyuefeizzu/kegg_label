
function show(n){ var box=document.getElementsByClassName('box');
for(var i=0;i<box.length;i++){box[i].style.display='none';}
document.getElementById(n).style.display="block";}


function hide(n) {document.getElementById(n).style.display="none"}
