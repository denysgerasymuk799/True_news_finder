var skroller;!function(v,b,y){"use strict";var w=v(document),_=v(b),x=v("body"),n=new MobileDetect(b.navigator.userAgent),C={menuscroll:v("#menu-scroll"),init:function(){var t,e=this;for(t in e)if(e.hasOwnProperty(t)){var i=e[t];void 0!==i.selector&&void 0!==i.init&&0<v(i.selector).length&&i.init()}},fixedHeader:{selector:".subheader.fixed",init:function(){var t=this,e=v(t.selector);_.scroll(function(){t.scroll(e)})},scroll:function(t){var e=_.scrollTop(),i="header--slide",o="header--unslide",n=t.find(".quick_search");400<e?(t.hasClass(o)&&t.removeClass(o),t.hasClass(i)||setTimeout(function(){t.addClass(i)},10)):e<400&&0<e?t.hasClass(i)&&(t.removeClass(i),t.addClass(o),n.removeClass("active")):(t.removeClass(i),t.removeClass(o),n.removeClass("active"))}},search:{selector:".quick_toggle",init:function(){v(this.selector).each(function(t){var e=v(this),i=e.parents(".quick_search");e.on("click",function(t){return i.toggleClass("active"),!1})})}},responsiveNav:{selector:"#wrapper",init:function(){var t=v(this.selector),e=v(".click-capture"),i=v("#mobile-menu"),o=i.find('.mobile-menu li:has(".sub-menu")>a span');v(".mobile-toggle-holder").on("click",function(){return t.removeClass("open-menu").addClass("open-menu"),!1}),e.add(i.find(".thb-close")).on("click",function(){t.removeClass("open-menu")}),o.on("click",function(t){var e=v(this).parents("a"),i=e.next(".sub-menu");e.hasClass("active")?(e.removeClass("active"),i.slideUp("200",function(){setTimeout(function(){C.menuscroll.update()},10)})):(e.addClass("active"),i.slideDown("200",function(){setTimeout(function(){C.menuscroll.update()},10)})),t.stopPropagation(),t.preventDefault()})}},categoryMenu:{selector:".sf-menu:not(.secondary)",init:function(){v(this.selector).find(".menu-item-has-children").each(function(){var t=v(this),e=t.find(">.sub-menu,>.thb_mega_menu_holder"),i=t.find(".thb_mega_menu li"),o=t.find(".category-children>.row");i.first().addClass("active"),t.hoverIntent(function(){TweenLite.to(e,.5,{autoAlpha:1,ease:Quart.easeOut,onStart:function(){e.css("display","block")},onComplete:function(){C.circle_perc.control()}})},function(){TweenLite.to(e,.5,{autoAlpha:0,ease:Quart.easeOut,onComplete:function(){e.css("display","none")}})}),i.mouseover(function(){var t=v(this),e=t.index();i.removeClass("active"),t.addClass("active"),o.hide(),o.filter(":nth-child("+(e+1)+")").css({display:"flex"}),C.circle_perc.control()})})}},secondaryMenu:{selector:".secondary-holder",init:function(){var t=v(this.selector),e=t.find(".sf-menu"),i=-1;v(">li",e).each(function(){i=i>v(this).outerWidth()?i:v(this).outerWidth()}),e.css({display:"none",width:2*i+70}),t.hoverIntent(function(){TweenLite.to(e,.5,{autoAlpha:1,ease:Quart.easeOut,onStart:function(){e.css("display","flex")}})},function(){TweenLite.to(e,.5,{autoAlpha:0,ease:Quart.easeOut,onComplete:function(){e.css("display","none")}})})}},loginForm:{selector:"#thb-login",init:function(){var n=v(this.selector),e=v("#thb_login_form",n),a=v("#thb_registration_form",n),s=v("#thb_lost_form",n),t=v("ul",n),i=v("a",t),o=v(".lost_password",n),r=v(".back",n);i.on("click",function(){var t=v(this);return t.hasClass("active")||(i.removeClass("active"),t.addClass("active"),v(".thb-form-container",n).toggleClass("register-active")),!1}),o.on("click",function(){return t.addClass("lost"),v(".thb-form-container",n).removeClass("register-active"),v(".thb-form-container",n).addClass("lost-active"),!1}),r.on("click",function(){return t.removeClass("lost"),v(".thb-form-container",n).removeClass("lost-active"),!1}),s.on("submit",function(t){t.preventDefault();var i=v(this).find("button"),o=i.text();i.text(themeajax.l10n.loading).addClass("loading"),v.post(themeajax.url,s.serialize(),function(t){var e=v.parseJSON(t);v(".thb-errors.lost-errors").html(e.message),i.text(o).removeClass("loading")})}),e.on("submit",function(t){t.preventDefault();var i=v(this).find("button"),o=i.text();i.text(themeajax.l10n.loading).addClass("loading"),v.post(themeajax.url,e.serialize(),function(t){var e=v.parseJSON(t);v(".thb-errors.login-errors").html(e.message),!1===e.error?(n.addClass("loading"),b.location.reload(!0),i.hide()):i.text(o).removeClass("loading")})}),a.on("submit",function(t){t.preventDefault();var i=v(this).find("button"),o=i.text();i.text(themeajax.l10n.loading).addClass("loading"),v.post(themeajax.url,a.serialize(),function(t){var e=v.parseJSON(t);v(".thb-errors.register-errors").html(e.message),!1===e.error?i.hide():i.text(o).removeClass("loading")})})}},magnificSingle:{selector:'[rel="magnific"]',init:function(){v(this.selector).each(function(){v(this).magnificPopup({type:"image",closeOnContentClick:!0,fixedContentPos:!0,closeBtnInside:!1,mainClass:"mfp-zoom-in",removalDelay:250,overflowY:"scroll",image:{verticalFit:!0,titleSrc:function(t){return t.el.attr("title")}},callbacks:{imageLoadComplete:function(){var t=this;y.delay(function(){t.wrap.addClass("mfp-image-loaded")},10)},beforeOpen:function(){this.st.image.markup=this.st.image.markup.replace("mfp-figure","mfp-figure mfp-with-anim")}}})})}},magnificImage:{selector:".thb-lightbox-on .blog-post",init:function(){v(this.selector).each(function(){v(this).magnificPopup({delegate:'[rel="mfp"]',type:"image",closeOnContentClick:!0,fixedContentPos:!0,mainClass:"mfp-zoom-in",removalDelay:250,closeBtnInside:!1,overflowY:"scroll",gallery:{enabled:!0,navigateByImgClick:!1,preload:[0,1]},image:{verticalFit:!0,titleSrc:function(t){return t.el.attr("title")}},callbacks:{imageLoadComplete:function(){var t=this;y.delay(function(){t.wrap.addClass("mfp-image-loaded")},10)},beforeOpen:function(){this.st.image.markup=this.st.image.markup.replace("mfp-figure","mfp-figure mfp-with-anim")},open:function(){v.magnificPopup.instance.next=function(){var t=this;t.wrap.removeClass("mfp-image-loaded"),setTimeout(function(){v.magnificPopup.proto.next.call(t)},125)},v.magnificPopup.instance.prev=function(){var t=this;this.wrap.removeClass("mfp-image-loaded"),setTimeout(function(){v.magnificPopup.proto.prev.call(t)},125)}}}})})}},magnificInline:{selector:'[rel="inline"]',init:function(){v(this.selector).each(function(){v(this).magnificPopup({type:"inline",midClick:!0,mainClass:"mfp-fade thb-inline-lightbox",removalDelay:250,closeOnContentClick:!1,fixedContentPos:!0,closeBtnInside:!0,overflowY:"scroll"})})}},carousel:{selector:".slick",init:function(t){(t||v(this.selector)).each(function(){var i=v(this),t=i.data("columns"),e=!0===i.data("navigation"),o=!1!==i.data("autoplay"),n=!0===i.data("pagination"),a=i.data("speed")?i.data("speed"):1e3,s=!!i.data("center")&&i.data("center"),r=!!i.data("disablepadding")&&i.data("disablepadding"),l=!!i.data("vertical")&&i.data("vertical"),c=!0===i.data("fade"),d=i.hasClass("center-arrows"),u=i.data("asnavfor"),f={dots:n,arrows:e,infinite:!0,speed:a,centerMode:s,slidesToShow:t,slidesToScroll:1,rtl:x.hasClass("rtl"),rows:0,autoplay:o,centerPadding:r?0:"50px",autoplaySpeed:6e3,pauseOnHover:!0,focusOnSelect:!0,adaptiveHeight:!0,vertical:l,verticalSwiping:l,accessibility:!1,fade:c,cssEase:"ease-in-out",prevArrow:'<button type="button" class="slick-nav slick-prev"><i class="fa fa-angle-left"></i></button>',nextArrow:'<button type="button" class="slick-nav slick-next"><i class="fa fa-angle-right"></i></button>',responsive:[{breakpoint:1025,settings:{slidesToShow:t<3?t:l?t-1:3,centerPadding:r?0:"40px"}},{breakpoint:780,settings:{slidesToShow:t<2?t:l?t-1:2,centerPadding:r?0:"30px"}},{breakpoint:640,settings:{slidesToShow:t<2?t:l?t-1:1,centerPadding:r?0:"15px"}}]};u&&v(u).is(":visible")&&(f.asNavFor=u),(i.hasClass("product-images")||i.data("fade"))&&(f.fade=!0),i.hasClass("carousel-slider")&&(f.responsive=[{breakpoint:1025,settings:{slidesToShow:t<3?t:l?t-1:3}},{breakpoint:780,settings:{slidesToShow:t<2?t:l?t-1:2}},{breakpoint:640,settings:{slidesToShow:t<2?t:l?t-1:1}}]),i.on("init",function(){C.circle_perc.control(),d&&_.trigger("resize.position_arrows")}),d&&_.on("resize.position_arrows",function(){var t=i.find(".post-gallery").length?i.find(".post-gallery"):i.find(".thb-placeholder"),e=Math.round(t.outerHeight()/2);i.find(".slick-nav").css({top:e})}),i.on("afterChange",function(t,e,i,o){C.circle_perc.control()}),i.hasClass("post-slider-style4")&&(f.dotsClass="post-title-bullets",f.customPaging=function(t,e){var i=v(t.$slides[e]),o=i.find(".post-category").text(),n=i.find("h1").text();return v('<button type="button" class="post" />').html("<span>0"+(e+1)+'</span><aside class="post-category single_category_title">'+o+"</aside><h6>"+n+"</h6>")},f.responsive[0].settings.dots=!1,f.responsive[1].settings.dots=!1,f.responsive[2].settings.dots=!1,i.parents(".full-width-row").length&&i.on("setPosition",function(){var t=i.find(".slick-active .row.max_width"),e=_.width()-(t.offset().left+t.outerWidth())+15;i.find(".post-title-bullets").css("right",e+"px")})),i.hasClass("video-thumbnail-slider")&&(f.responsive[2].settings.slidesToShow=2),i.slick(f),i.find(".wp-post-image").on("lazyloaded",function(){d&&_.trigger("resize.position_arrows")}),i.parents(".vc_tta-container").length&&v(document).on("click.vc.tabs.data-api",function(){i.slick("refresh")})})}},cookieBar:{selector:".thb-cookie-bar",init:function(){var t=v(this.selector),e=v(".button",t);"hide"!==Cookies.get("thb-goodlife-cookiebar")&&TweenMax.to(t,.5,{opacity:"1",y:"0%"}),e.on("click",function(){return Cookies.set("thb-goodlife-cookiebar","hide",{expires:30}),TweenMax.to(t,.5,{opacity:"0",y:"100%"}),!1})}},paginationStyle2:{selector:".pagination-style2",init:function(){v(this.selector).each(function(){var t=v(this),o=2,n=v(t.data("loadmore")),e=t.data("rand"),a=n.text(),i="thb_postajax_"+e,s=b[i].loop,r=b[i].style,l=b[i].columns,c=b[i].excerpts,d=b[i].count;0<n.length&&n.on("click",function(){return n.text(themeajax.l10n.loading),v.post(themeajax.url,{action:"thb_posts",count:d,loop:s,page:o,columns:l,style:r,excerpts:c},function(t){o++;var e=v.parseHTML(v.trim(t)),i=e?e.length:0;""===t||"undefined"===t||"No More Posts"===t||"No $args array created"===t?(t="",n.text(themeajax.l10n.nomore).removeClass("loading").off("click")):(v(e).insertBefore(n.parents(".masonry_loader")).hide(),v(e).show(),TweenMax.set(v(e),{opacity:0,y:20}),TweenMax.staggerTo(v(e),.25,{y:0,opacity:1,ease:Quart.easeOut},.15),i<d?n.text(themeajax.l10n.nomore).removeClass("loading"):n.text(a).removeClass("loading"))}),!1})})}},paginationStyle3:{selector:".pagination-style3",init:function(){v(this.selector).each(function(){var o=v(this),n=!1,a=2,t="thb_postajax_"+o.data("rand"),s=b[t].count,e=b[t].style,i=b[t].columns,r=b[t].excerpts,l=y.debounce(function(){!1===n&&_.scrollTop()+_.height()+150>=o.offset().top+o.outerHeight()&&v.ajax(themeajax.url,{method:"POST",data:{action:"thb_posts",count:s,style:e,excerpts:r,page:a,columns:i},beforeSend:function(){o.addClass("thb-loading-bottom"),n=!0},success:function(t){n=!1,a++;var e=v.parseHTML(v.trim(t)),i=e?e.length:0;""===t||"undefined"===t||"No More Posts"===t||"No $args array created"===t?_.off("scroll",l):(o.removeClass("thb-loading-bottom"),v(e).appendTo(o).hide(),v(e).show(),C.circle_perc.init(),TweenMax.set(v(e),{opacity:0,y:20}),TweenMax.staggerTo(v(e),.25,{y:0,opacity:1,ease:Quart.easeOut,onComplete:function(){s<=i&&_.on("scroll",l)}},.15))}})},30);_.scroll(l)})}},galleryArrows:{selector:".blog-post.format-gallery",init:function(t){var e=t||v(this.selector);w.on("keyup",function(t){37===t.keyCode&&e.find(".slick-prev",".gallery-pagination").length&&e.find(".slick-prev",".gallery-pagination")[0].click(),39===t.keyCode&&e.find(".slick-next",".gallery-pagination").length&&e.find(".slick-next",".gallery-pagination")[0].click()})}},articleScroll:{selector:"#infinite-article",org_post_url:b.location.href,org_post_title:document.title,org_shares:!1,init:function(){var t=this,f=v(t.selector),e=f.data("infinite"),i=f.data("infinite-count"),o=f.find(".blog-post:first-child"),h=(o.find(".share-main"),o.data("id")),p=h,g=!1,n=v("#footer").outerHeight()+v("#subfooter").outerHeight(),m=0,a=y.debounce(function(){t.location_change()},10),s=y.debounce(function(){(!i||m<parseInt(i,10))&&_.scrollTop()>=w.height()-_.height()-n-200&&!1===g&&(f.addClass("thb-loading-bottom"),h===p&&v.ajax(themeajax.url,{method:"POST",data:{action:"thb_infinite_ajax",post_id:p},beforeSend:function(){g=!(h=null)},success:function(t){m++,g=!1;var e,i,o,n,a,s=v.parseHTML(t),r=v(s).find(".adsbygoogle, .adworx_ad"),l=v(s).find(".twitter-tweet, .twitter-timeline"),c=v(s).find(".instagram-media");if(f.removeClass("thb-loading-bottom"),s){var d=v(s).find(".blog-post");if(h=d.data("id"),p=h,v(s).appendTo(f),C.circle_perc.init(),C.carousel.init(v(s).find(".slick")),C.fixedPosition.init(v(s).find(".fixed-me")),C.magnificImage.init(),C.parallax_bg.init(),C.topReviews.init(),C.shareArticleDetail.init(),C.animation.init(),void 0!==b.instgrm)b.instgrm.Embeds.process();else if(c.length&&void 0===b.instgrm){var u=document.createElement("script");u.src="//platform.instagram.com/en_US/embeds.js",u.onload=function(){b.instgrm.Embeds.process()},x.append(u)}void 0!==b.twttr?twttr.widgets.load(document.getElementById("infinite-article")):l.length&&void 0===b.twttr&&(b.twttr=(e=document,i="twitter-wjs",n=e.getElementsByTagName("script")[0],a=b.twttr||{},e.getElementById(i)||((o=e.createElement("script")).id=i,o.src="https://platform.twitter.com/widgets.js",n.parentNode.insertBefore(o,n),a._e=[],a.ready=function(t){a._e.push(t)}),a)),d.hasClass("format-gallery")&&(w.off("keyup"),C.galleryArrows.init(d)),void 0!==b.googletag&&googletag.pubads().refresh(),void 0!==b.addthis&&addthis.toolbox(),void 0!==b.atnt&&b.atnt(),void 0!==b.adsbygoogle&&r.length&&r.each(function(){(adsbygoogle=b.adsbygoogle||[]).push({})}),"undefined"!=typeof FB&&FB.init({status:!0,cookie:!0,xfbml:!0}),v(document.body).trigger("thb_after_infinite_load")}else h=null}}))},100);"on"===e?(_.scroll(a),_.scroll(s)):_.scroll(y.debounce(function(){t.borderWidth(v(".post-detail-row").offset().top,v(".post-detail-row").outerHeight(!0))},10))},location_change:function(){var t,e,i,o=this,c=(v(o.selector),_.scrollTop()),d=c+_.height(),u=[];if(v(".post-detail-row").each(function(){var t,e=v(this),i=e.find(".blog-post"),o=i.data("id"),n=e.offset().top-(v(".subheader.fixed").outerHeight()+v("#wpadminbar").outerHeight()),a=e.outerHeight(!0),s=i.data("url"),r=e.find(".post-title h1").text(),l=e.find(".share-main");t=n+a,n<c&&d<t?u.push({id:o,top:n,bottom:t,post_url:s,post_title:r,alength:a,shares:l}):c<n&&n<d?u.push({id:o,top:n,bottom:t,post_url:s,post_title:r,alength:a,shares:l}):c<t&&t<d&&u.push({id:o,top:n,bottom:t,post_url:s,post_title:r,alength:a,shares:l})}),0===u.length)e=o.org_post_url,t=o.org_post_title,i=o.org_shares;else if(1===u.length){var n=u.pop();e=n.post_url,t=n.post_title,i=n.shares,o.borderWidth(n.top,n.alength)}else e=u[0].post_url,t=u[0].post_title,i=u[0].shares,o.borderWidth(u[0].top,u[0].alength);o.updateURL(e,t,i)},updateURL:function(t,e,i){b.location.href!==t&&(""!==t&&(history.replaceState(null,null,t),document.title=e,v("#page-title").html(e),i&&(v(".subheader.fixed").find(".share-article-vertical").html(i.html()),C.shareArticleDetail.init())),this.updateGA(t))},updateGA:function(t){if("undefined"!=typeof _gaq)_gaq.push(["_trackPageview",t]);else if("undefined"!=typeof ga){var e=/.+?\:\/\/.+?(\/.+?)(?:#|\?|$)/.exec(t)[1];ga("send","pageview",e)}},borderWidth:function(t,e){var i=(_.scrollTop()-t)/e;TweenMax.set(v(".progress",".subheader.fixed"),{scaleX:i})}},postGridAjaxify:{selector:".ajaxify-pagination",init:function(){var s=v(this.selector);s.data("initialized",!0);var r=b.History,l=b.document;if(!r.enabled)return!1;var i=r.getRootUrl();v.fn.ajaxify=y.debounce(function(){var t=v(this);return t.find(".page-numbers").on("click",function(t){var e=v(this),i=e.attr("href"),o=e.attr("title")||null;return!(2!==t.which&&!t.metaKey)||(r.pushState(null,o,i),t.preventDefault(),!1)}),t},50),s.ajaxify(),_.bind("statechange",function(){var n=r.getState().url,a=n.replace(i,""),t=v("#wpadminbar"),e=t?t.outerHeight():0;s.addClass("thb-loading"),jQuery("html, body").animate({scrollTop:s.offset().top-e-30},800),v.post(n,function(t){var e=v.parseHTML(t),i=v(e).filter("title").text(),o=v(e).find(".ajaxify-pagination").html();if(!o)return l.location.href=n,!1;s.stop(!0,!0),s.html(o).ajaxify().animate({opacity:1},500,"linear",function(){l.title=i,s.removeClass("thb-loading"),C.circle_perc.control(),v(l.body).trigger("sticky_kit:recalc")}),void 0!==b.pageTracker&&b.pageTracker._trackPageview(a),void 0!==b.reinvigorate&&void 0!==b.reinvigorate.ajax_track&&reinvigorate.ajax_track(n)})})}},circle_perc:{selector:".circle_perc",init:function(){var t=this,e=v(t.selector);t.control(e),_.scroll(function(){t.control(e)})},control:function(t){var i=-1;(t||v(this.selector)).filter(":in-viewport").each(function(){var t=v(this),e=t.data("dashoffset");setTimeout(function(){TweenLite.to(t,1,{attr:{"stroke-dashoffset":e}})},200*++i)})}},newsletter:{selector:".newsletter-form",init:function(){v(this.selector).each(function(){var i=v(this);i.on("submit",function(){return v.post(themeajax.url,{action:"thb_subscribe_emails",email:i.find(".widget_subscribe").val()},function(t){var e=v.parseHTML(v.trim(t));i.next(".result").html(e).fadeIn(200).delay(3e3).fadeOut(200)}),!1})})}},animation:{selector:".animation",init:function(){var t=this,e=v(t.selector);v(".animation.bottom-to-top-3d, .animation.top-to-bottom-3d").parent(":not(.slick-track)").addClass("perspective-wrap"),_.on("scroll.thb-animation",function(){t.control(e,!0)}).trigger("scroll.thb-animation")},container:function(t){var e=v(this.selector,t);this.control(e,!1)},control:function(t,e){var i=0;(e?t.filter(":in-viewport"):t).each(function(){var t=v(this);!0!==t.data("thb-animated")&&(t.data("thb-animated",!0),TweenMax.to(t,.5,{autoAlpha:1,x:0,y:0,z:0,rotationZ:"0deg",rotationX:"0deg",rotationY:"0deg",delay:.15*i})),i++})}},topReviews:{selector:".widget_topreviews .progress, .post-review .progress span",init:function(){var t=this,e=v(t.selector);t.control(e),_.scroll(function(){t.control(e)})},control:function(t){var i=-1;t.filter(":in-viewport").each(function(){var t=v(this),e=t.data("width");setTimeout(function(){TweenLite.to(t,1,{width:e+"%"})},200*++i)})}},comments:{selector:".expanded-comments-off #comment-toggle",init:function(){v(this.selector).on("click",function(){return v(this).toggleClass("active"),v(this).next(".comment-content-container").slideToggle(),!1})}},videoPlaylist:{selector:".video_playlist",init:function(){var t=v(this.selector);t.each(function(){var o=v(this),n=o.find(".video-side");o.find(".video_play");t.on("click",".video_play",function(){var t=v(this),e=t.data("video-url"),i=t.data("post-id");return t.hasClass("video-active")||(o.find(".video_play").removeClass("video-active"),o.find('.video_play[data-video-url="'+e+'"]').addClass("video-active"),n.addClass("thb-loading"),v.post(themeajax.url,{action:"thb-parse-embed",post_ID:i,shortcode:"[embed]"+e+"[/embed]"},function(t){t.success&&n.html(t.data.body),n.removeClass("thb-loading")})),!1})})}},postListing:{selector:".thb_listing",init:function(){v(this.selector).each(function(){var t=v(this),e=t.data("type"),n=t.data("count"),a=t.find("a"),s=t.parents(".widget_title").next("ul"),r=new TimelineMax;a.on("click",function(){var i=v(this),t=i.data("time"),o=s.find("li,p");o.length;return s.addClass("thb-loading"),v.post(themeajax.url,{action:"thb_listing",count:n,type:e,time:t},function(t){var e=v.parseHTML(v.trim(t));e.length;TweenLite.set(e,{x:30,opacity:0}),a.removeClass("active"),i.addClass("active"),r.staggerTo(o,1,{x:-30,opacity:0,onStart:function(){s.removeClass("thb-loading")},onComplete:function(){s.html(e)}},.1).staggerTo(e,.5,{x:0,opacity:1},.2)}),!1})})}},shareArticleDetail:{selector:".share-article, .share-article-vertical",init:function(){v(this.selector).find(".social:not(.whatsapp)").on("click",function(){var t=screen.width/2-320,e=screen.height/2-220-100;return b.open(v(this).attr("href"),"mywin","left="+t+",top="+e+",width=640,height=440,toolbar=0"),!1})}},custom_scroll:{selector:".custom_scroll",init:function(){v(this.selector).each(function(){var t=v(this),e=new PerfectScrollbar(t[0],{suppressScrollX:!0});"menu-scroll"===t.attr("id")&&(C.menuscroll=e)})}},categoryDropdown:{selector:".thb-sibling-categories",init:function(){var s=this;v(s.selector).each(function(){var t=v(this),e=t.find("li:not(.thb-pull-down)"),i=t.find("li.thb-pull-down"),o=t.find(".thb-pull-down .sub-menu"),n=[],a=t.parents(".category-element-holder").find(".category-element-content");i.find(">a").on("click",function(){return!1}),e.each(function(){n.push({el:v(this),width:v(this).outerWidth(!0),added:!1})}),e.remove(),s.start(t,n,o,i,a)})},start:function(r,t,l,c,o){var d=t;function e(){for(var t=r.outerWidth(),e=c.outerWidth(!0)+15,i=y.filter(d,{added:!1}),o=y.filter(d,{added:!0}),n=0;n<i.length;n++)e+=i[n].width;t<=e?y.last(i)&&(y.last(i).added=!0):(!y.first(o)||y.first(o).width+e<t)&&y.first(o)&&(y.first(o).added=!1);for(var a=0;a<i.length;a++)i[a].el.insertBefore(c);for(var s=0;s<o.length;s++)l.prepend(o[s].el);0===o.length?c.hide():c.css({display:"inline-block"})}y.each(d,function(t,e,i){t.el.find("[data-ajax-cat]").on("click",function(){return o.addClass("thb-loading-center"),v.post(themeajax.url,{action:"thb_ajax_cat",catid:v(this).data("ajax-cat"),style:o.data("style"),count:o.data("count")},function(t){o.removeClass("thb-loading-center");var e=v.parseHTML(v.trim(t));""===t||"undefined"===t||"No More Posts"===t||"No $args array created"===t?t="":(o.html(v(e)),C.circle_perc.control())}),!1})}),r.addClass("active");for(var i=0;i<d.length+1;i++)e();_.on("resize",function(){e()})}},parallax_bg:{selector:"body",active:0,init:function(){0<v('div[role="main"]').find(".parallax_bg").length&&(b.skroller=skrollr.init({forceHeight:!1,easing:"outCubic",mobileCheck:function(){return!1}}))}},fixedPosition:{selector:".fixed-me",init:function(t){var e=t||v(this.selector),i=v("#wpadminbar"),o=i?i.outerHeight():0;n.mobile()||e.each(function(){var t=v(this),e=27+(v(".subheader.fixed").length?50:0);t.stick_in_parent({offset_top:e+o,inner_scrolling:!1})}),v(".post-gallery.vertical").waitForImages(function(){v(document.body).trigger("sticky_kit:recalc")}),_.resize(y.debounce(function(){v(document.body).trigger("sticky_kit:detach")},30))}},toTop:{selector:"#scroll_totop",init:function(){var t=this;v(t.selector).on("click",function(){return TweenMax.to(_,1,{scrollTo:{y:0,autoKill:!1},ease:Quart.easeOut}),!1}),_.scroll(y.debounce(function(){t.control()},50))},control:function(){var t=v(this.selector);300<_.scrollTop()?TweenMax.to(t,.2,{autoAlpha:1,ease:Quart.easeOut}):TweenMax.to(t,.2,{autoAlpha:0,ease:Quart.easeOut})}},wpml:{selector:"#thb_language_selector_mobile",init:function(){v(this.selector).on("change",function(){var t=v(this).val();return t&&(b.location=t),!1})}},variations:{selector:"form.variations_form",init:function(){var t=v(this.selector),i=v("#product-images"),o=v("#product-thumbnails"),e=v(".first img",i).attr("src"),n=v(".first img",o).attr("src");t.on("show_variation",function(t,e){e.hasOwnProperty("image")&&e.image.src&&(v(".first img",i).attr("src",e.image.src).attr("srcset",""),v(".first img",o).attr("src",e.image.thumb_src).attr("srcset",""),i.hasClass("slick-initialized")&&i.slick("slickGoTo",0))}).on("reset_image",function(){v(".first img",i).attr("src",e).attr("srcset",""),v(".first img",o).attr("src",n).attr("srcset","")})}},quantity:{selector:".quantity",init:function(){v(this.selector);v("div.quantity:not(.buttons_added), td.quantity:not(.buttons_added)").addClass("buttons_added").append('<input type="button" value="+" class="plus" />').prepend('<input type="button" value="-" class="minus" />').end().find('input[type="number"]').attr("type","text"),w.on("click",".plus, .minus",function(){var t=v(this).closest(".quantity").find(".qty"),e=parseFloat(t.val()),i=parseFloat(t.attr("max")),o=parseFloat(t.attr("min")),n=t.attr("step");e&&""!==e&&"NaN"!==e||(e=0),""!==i&&"NaN"!==i||(i=""),""!==o&&"NaN"!==o||(o=0),"any"!==n&&""!==n&&void 0!==n&&"NaN"!==parseFloat(n)||(n=1),v(this).is(".plus")?i&&(i===e||i<e)?t.val(i):t.val(e+parseFloat(n)):o&&(o===e||e<o)?t.val(o):0<e&&t.val(e-parseFloat(n)),t.trigger("change")})}},contact:{selector:".contact_map",init:function(){var g=this;v(g.selector).each(function(){var u,t=v(this),e=t.data("map-zoom"),i=t.data("map-style"),o=t.data("map-type"),n=t.data("pan-control"),a=t.data("zoom-control"),s=t.data("maptype-control"),r=t.data("scale-control"),l=t.data("streetview-control"),f=t.find(".thb-location"),h=new google.maps.LatLngBounds,c={center:{lat:-34.397,lng:150.644},styles:i,zoom:e,draggable:!("ontouchend"in document),scrollwheel:!1,panControl:n,zoomControl:a,mapTypeControl:s,scaleControl:r,streetViewControl:l,mapTypeId:o},p=new google.maps.Map(t[0],c);p.addListener("tilesloaded",function(){u||(f.each(function(t){var e=v(this).data("option"),i=e.latitude,o=e.longitude,n=new google.maps.LatLng(i,o),a=e.marker_image,s=e.marker_size,r=e.retina_marker,l=e.marker_title,c=e.marker_description,d=new Image;h.extend(n),d.src=a,v(d).on("load",function(){g.setMarkers(t,f.length,p,i,o,a,s,l,c,r)}),u=!0}),0<e?(p.setCenter(h.getCenter()),p.setZoom(e)):(p.setCenter(h.getCenter()),p.fitBounds(h)))}),_.on("resize",y.debounce(function(){p.setCenter(h.getCenter())},50))})},setMarkers:function(t,e,a,s,r,l,c,d,u,f){setTimeout(function(t){var e=l.toLowerCase().split(".");e=e[e.length-1],(v.inArray(e,["svg"])||f)&&(l=new google.maps.MarkerImage(l,null,null,null,new google.maps.Size(c[0]/2,c[1]/2)));var i=new google.maps.Marker({position:new google.maps.LatLng(s,r),map:a,animation:google.maps.Animation.DROP,icon:l,optimized:!1}),o="<h3>"+d+"</h3><div>"+u+"</div>",n=new google.maps.InfoWindow({content:o});i.addListener("click",function(){n.open(a,i)})},250*t,t)}},themeSwitcher:{selector:"#theme-switcher",init:function(){var t=v(this.selector);t.find(".style-toggle").on("click",function(){return t.add(v(this)).toggleClass("active"),!1})}}};w.ready(function(){v("#vc_inline-anchor").length?_.on("vc_reload",function(){C.init()}):C.init()})}(jQuery,this,_);