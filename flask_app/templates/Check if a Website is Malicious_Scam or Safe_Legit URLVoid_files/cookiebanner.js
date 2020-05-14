/*! (C) Cookie Banner v1.0.0 - MIT License - http://cookiebanner.eu/ */
!function(e){"use strict";function t(e,t){var i=!1,o=!0,n=e.document,s=n.documentElement,a=n.addEventListener?"addEventListener":"attachEvent",r=n.addEventListener?"removeEventListener":"detachEvent",c=n.addEventListener?"":"on",l=function(o){"readystatechange"==o.type&&"complete"!=n.readyState||(("load"==o.type?e:n)[r](c+o.type,l,!1),!i&&(i=!0)&&t.call(e,o.type||o))},p=function(){try{s.doScroll("left")}catch(e){return void setTimeout(p,50)}l("poll")};if("complete"==n.readyState)t.call(e,"lazy");else{if(n.createEventObject&&s.doScroll){try{o=!e.frameElement}catch(e){}o&&p()}n[a](c+"DOMContentLoaded",l,!1),n[a](c+"readystatechange",l,!1),e[a](c+"load",l,!1)}}var i=e,o=i.document,n="cbinstance",s={get:function(e){return decodeURIComponent(o.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*"+encodeURIComponent(e).replace(/[\-\.\+\*]/g,"\\$&")+"\\s*\\=\\s*([^;]*).*$)|^.*$"),"$1"))||null},set:function(e,t,i,n,s,a){if(!e||/^(?:expires|max\-age|path|domain|secure)$/i.test(e))return!1;var r="";if(i)switch(i.constructor){case Number:r=i===1/0?"; expires=Fri, 31 Dec 9999 23:59:59 GMT":"; max-age="+i;break;case String:r="; expires="+i;break;case Date:r="; expires="+i.toUTCString()}return o.cookie=encodeURIComponent(e)+"="+encodeURIComponent(t)+r+(s?"; domain="+s:"")+(n?"; path="+n:"")+(a?"; secure":""),!0},has:function(e){return new RegExp("(?:^|;\\s*)"+encodeURIComponent(e).replace(/[\-\.\+\*]/g,"\\$&")+"\\s*\\=").test(o.cookie)},remove:function(e,t,i){return!(!e||!this.has(e))&&(o.cookie=encodeURIComponent(e)+"=; expires=Thu, 01 Jan 1970 00:00:00 GMT"+(i?"; domain="+i:"")+(t?"; path="+t:""),!0)}},a={merge:function(){var e,t={},i=0,o=arguments.length;if(0===o)return t;for(;i<o;i++)for(e in arguments[i])Object.prototype.hasOwnProperty.call(arguments[i],e)&&(t[e]=arguments[i][e]);return t},str2bool:function(e){switch(e=""+e,e.toLowerCase()){case"false":case"no":case"0":case"":return!1;default:return!0}},fade_in:function(e){e.style.opacity<1&&(e.style.opacity=(parseFloat(e.style.opacity)+.05).toFixed(2),i.setTimeout(function(){a.fade_in(e)},50))},get_data_attribs:function(e){var t={};if(Object.prototype.hasOwnProperty.call(e,"dataset"))t=e.dataset;else{var i,o=e.attributes;for(i in o)if(Object.prototype.hasOwnProperty.call(o,i)){var n=o[i];if(/^data-/.test(n.name)){var s=a.camelize(n.name.substr(5));t[s]=n.value}}}return t},normalize_keys:function(e){var t={};for(var i in e)if(Object.prototype.hasOwnProperty.call(e,i)){var o=a.camelize(i);t[o]=e[o]?e[o]:e[i]}return t},camelize:function(e){for(var t="-",i=e.indexOf(t);i!=-1;){var o=i===e.length-1,n=o?"":e[i+1],s=n.toUpperCase(),a=o?t:t+n;e=e.replace(a,s),i=e.indexOf(t)}return e},find_script_by_id:function(e){for(var t=o.getElementsByTagName("script"),i=0,n=t.length;i<n;i++)if(e===t[i].id)return t[i];return null}},r=a.find_script_by_id("cookiebanner"),c=e.Cookiebanner=function(e){this.init(e)};c.prototype={cookiejar:s,init:function(t){this.inserted=!1,this.closed=!1,this.test_mode=!1;var i="We use cookies to enhance your experience. By continuing to visit this site you agree to our use of cookies.",o="Learn more";if(this.default_options={cookie:"cookiebanner-accepted",closeText:"&#10006;",closeStyle:"float:right;padding-left:5px;",cookiePath:"/",cookieDomain:null,cookieSecure:!1,debug:!1,expires:1/0,zindex:255,mask:!1,maskOpacity:.5,maskBackground:"#000",height:"auto",minHeight:"21px",bg:"#000",fg:"#ddd",link:"#aaa",position:"bottom",message:i,linkmsg:o,moreinfo:"http://aboutcookies.org",moreinfoTarget:"_blank",moreinfoDecoration:"none",moreinfoFontWeight:"normal",effect:null,fontSize:"14px",fontFamily:"arial, sans-serif",instance:n,textAlign:"center",acceptOnScroll:!1,acceptOnClick:!1,acceptOnTimeout:null,acceptOnFirstVisit:!1},this.options=this.default_options,this.script_el=r,this.script_el){var s=a.get_data_attribs(this.script_el);this.options=a.merge(this.options,s)}t&&(t=a.normalize_keys(t),this.options=a.merge(this.options,t)),n=this.options.instance,this.options.zindex=parseInt(this.options.zindex,10),this.options.mask=a.str2bool(this.options.mask),"string"==typeof this.options.expires&&"function"==typeof e[this.options.expires]&&(this.options.expires=e[this.options.expires]),"function"==typeof this.options.expires&&(this.options.expires=this.options.expires()),this.script_el&&this.run()},log:function(){"undefined"!=typeof console&&console.log.apply(console,arguments)},run:function(){if(!this.agreed()){var e=this;t(i,function(){e.insert()})}},build_viewport_mask:function(){var e=null;if(!0===this.options.mask){var t=this.options.maskOpacity,i=this.options.maskBackground,n='<div id="cookiebanner-mask" style="position:fixed;top:0;left:0;width:100%;height:100%;background:'+i+";zoom:1;filter:alpha(opacity="+100*t+");opacity:"+t+";z-index:"+this.options.zindex+';"></div>',s=o.createElement("div");s.innerHTML=n,e=s.firstChild}return e},agree:function(){return this.cookiejar.set(this.options.cookie,1,this.options.expires,this.options.cookiePath,""!==this.options.cookieDomain?this.options.cookieDomain:"",!!this.options.cookieSecure),!0},agreed:function(){return this.cookiejar.has(this.options.cookie)},close:function(){return this.inserted&&(this.closed||(this.element&&this.element.parentNode.removeChild(this.element),this.element_mask&&this.element_mask.parentNode.removeChild(this.element_mask),this.closed=!0)),this.closed},agree_and_close:function(){return this.agree(),this.close()},cleanup:function(){return this.close(),this.unload()},unload:function(){return this.script_el&&this.script_el.parentNode.removeChild(this.script_el),e[n]=void 0,!0},insert:function(){function e(e,t,i){var o=e.addEventListener?"addEventListener":"attachEvent",n=e.addEventListener?"":"on";e[o](n+t,i,!1)}this.element_mask=this.build_viewport_mask();var t=this.options.zindex;this.element_mask&&(t+=1);var i=o.createElement("div");i.className="cookiebanner",i.style.position="fixed",i.style.left=0,i.style.right=0,i.style.height=this.options.height,i.style.minHeight=this.options.minHeight,i.style.zIndex=t,i.style.background=this.options.bg,i.style.color=this.options.fg,i.style.lineHeight=i.style.minHeight,i.style.padding="5px 16px",i.style.fontFamily=this.options.fontFamily,i.style.fontSize=this.options.fontSize,i.style.textAlign=this.options.textAlign,"top"===this.options.position?i.style.top=0:i.style.bottom=0,i.innerHTML='<div class="cookiebanner-close" style="'+this.options.closeStyle+'">'+this.options.closeText+"</div><span>"+this.options.message+(this.options.linkmsg?" <a>"+this.options.linkmsg+"</a>":"")+"</span>",this.element=i;var n=i.getElementsByTagName("a")[0];n.href=this.options.moreinfo,n.target=this.options.moreinfoTarget,n.style.textDecoration=this.options.moreinfoDecoration,n.style.color=this.options.link,n.style.fontWeight=this.options.moreinfoFontWeight;var s=i.getElementsByTagName("div")[0];s.style.cursor="pointer";var r=this;e(s,"click",function(){r.agree_and_close()}),this.element_mask&&(e(this.element_mask,"click",function(){r.agree_and_close()}),o.body.appendChild(this.element_mask)),this.options.acceptOnScroll&&e(window,"scroll",function(){r.agree_and_close()}),this.options.acceptOnClick&&e(window,"click",function(){r.agree_and_close()}),this.options.acceptOnTimeout&&!isNaN(parseFloat(this.options.acceptOnTimeout))&&isFinite(this.options.acceptOnTimeout)&&setTimeout(function(){r.agree_and_close()},this.options.acceptOnTimeout),this.options.acceptOnFirstVisit&&r.agree(),o.body.appendChild(this.element),this.inserted=!0,"fade"===this.options.effect?(this.element.style.opacity=0,a.fade_in(this.element)):this.element.style.opacity=1}},r&&(e[n]||(e[n]=new c))}(window);
