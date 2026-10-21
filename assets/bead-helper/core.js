(function(root){
  'use strict';
  var hexes=['#ffffff','#f8f3df','#e8d9ba','#cdb28a','#9b7554','#684c3e','#353035','#171d22','#d9dce0','#a7adb4','#707b86','#465463','#ffc9ca','#f69aaf','#ed6f92','#d84970','#a92c53','#f4c4a7','#f4a879','#ec8050','#d25635','#b23d32','#f9e6a0','#f7ce59','#edac35','#cc852b','#dce8a7','#b9d276','#8eb657','#588e49','#31634a','#244936','#bee4d6','#87cbbb','#4da99d','#2b7e83','#c1e1ef','#8bc3df','#529bc6','#3373a5','#305280','#dcd1ed','#b8a3d4','#9578ba','#715497','#edc6de','#d697c4','#aa619a'];
  function rgb(hex){return [parseInt(hex.slice(1,3),16),parseInt(hex.slice(3,5),16),parseInt(hex.slice(5,7),16)];}
  function lab(c){var a=c.map(function(v){v/=255;return v>.04045?Math.pow((v+.055)/1.055,2.4):v/12.92;});var x=(a[0]*.4124564+a[1]*.3575761+a[2]*.1804375)/.95047,y=a[0]*.2126729+a[1]*.7151522+a[2]*.072175,z=(a[0]*.0193339+a[1]*.119192+a[2]*.9503041)/1.08883;var f=function(v){return v>.008856?Math.pow(v,1/3):7.787*v+16/116;};return [116*f(y)-16,500*(f(x)-f(y)),200*(f(y)-f(z))];}
  function distance(a,b){return (a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1])+(a[2]-b[2])*(a[2]-b[2]);}
  var palette=hexes.map(function(h,i){return {hex:h,rgb:rgb(h),lab:lab(rgb(h)),code:'P'+String(i+1).padStart(2,'0')};});
  function nearest(color,allowed){var best=allowed[0],d=Infinity;allowed.forEach(function(i){var next=distance(color,palette[i].lab);if(next<d){d=next;best=i;}});return best;}
  function quantize(data,w,h,limit,removeWhite){
    var length=w*h,empty=new Uint8Array(length),queue=[],head=0,all=palette.map(function(_,i){return i;});
    function white(i){return data[i*4+3]<100||(data[i*4]>240&&data[i*4+1]>240&&data[i*4+2]>240);}
    function push(i){if(!empty[i]&&white(i)){empty[i]=1;queue.push(i);}}
    if(removeWhite){for(var x=0;x<w;x++){push(x);push((h-1)*w+x);}for(var y=0;y<h;y++){push(y*w);push(y*w+w-1);}while(head<queue.length){var n=queue[head++],cx=n%w,cy=Math.floor(n/w);if(cx>0)push(n-1);if(cx<w-1)push(n+1);if(cy>0)push(n-w);if(cy<h-1)push(n+w);}}
    var colors=new Array(length),hist=new Array(palette.length).fill(0),cells=new Array(length).fill(-1);
    for(var i=0;i<length;i++){if(empty[i]||data[i*4+3]<100)continue;var alpha=data[i*4+3]/255;colors[i]=lab([0,1,2].map(function(k){return data[i*4+k]*alpha+255*(1-alpha);}));cells[i]=nearest(colors[i],all);hist[cells[i]]++;}
    var used=all.filter(function(i){return hist[i]>0;}),selected=used.slice();
    // Remove the color with the smallest total perceptual cost, preserving rare contrasting details.
    while(selected.length>limit){var drop=-1,minCost=Infinity;selected.forEach(function(idx){var cost=0;used.forEach(function(original){var old=Infinity,next=Infinity;selected.forEach(function(candidate){var d=distance(palette[original].lab,palette[candidate].lab);old=Math.min(old,d);if(candidate!==idx)next=Math.min(next,d);});cost+=hist[original]*(next-old);});if(cost<minCost){minCost=cost;drop=idx;}});selected.splice(selected.indexOf(drop),1);}
    var counts=new Array(palette.length).fill(0);for(i=0;i<length;i++){if(cells[i]<0)continue;cells[i]=nearest(colors[i],selected);counts[cells[i]]++;}
    return {width:w,height:h,cells:cells,counts:counts};
  }
  function valid(p){return !!p&&Number.isInteger(p.width)&&Number.isInteger(p.height)&&p.width>0&&p.width<=80&&p.height>0&&p.height<=80&&Array.isArray(p.cells)&&p.cells.length===p.width*p.height&&p.cells.every(function(i){return Number.isInteger(i)&&i>=-1&&i<palette.length;});}
  root.BeadCore={palette:palette,quantize:quantize,valid:valid};
})(typeof window!=='undefined'?window:this);
