!function(e,t){var n=["scroll","touchmove"],o=["orientationchange","resize"],r=0,i=function(e,t,n){var o=e.getAttribute(t);o&&(e[n]=o,e.removeAttribute(t))},c=function(e){"PICTURE"==e.parentNode.tagName&&Array.prototype.slice.call(e.parentNode.querySelectorAll("source")).forEach(function(e){i(e,"data-srcset","srcset")}),i(e,"data-src","src"),i(e,"data-srcset","srcset"),e.classList.remove("lazy"),elements.splice(elements.indexOf(e),1)},s=function(e,t,n,o){t.forEach(function(t){o?e.removeEventListener(t,n):e.addEventListener(t,n)})},l=function(){elements.length||(s(t,n,l,1),s(e,o,l,1)),r||(r=1,setTimeout(function(){elements.forEach(function(t){t.getBoundingClientRect().top<=e.innerHeight&&t.getBoundingClientRect().bottom>=0&&"none"!=getComputedStyle(t).display&&c(t)}),r=0},200))};s(t,["DOMContentLoaded"],function(){if(elements=Array.prototype.slice.call(t.querySelectorAll("img.lazy")),elements.length){if("IntersectionObserver"in e&&"IntersectionObserverEntry"in e&&"intersectionRatio"in IntersectionObserverEntry.prototype)return ob=new IntersectionObserver(function(e,t){e.forEach(function(e){e.isIntersecting&&(c(e.target),elements.length||t.disconnect())})}),void elements.forEach(function(e){ob.observe(e)});l(),s(t,n,l),s(e,o,l)}})}(window,document);