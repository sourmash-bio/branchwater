/*! For license information please see mgnify-sourmash-component.js.LICENSE.txt */
(()=>{"use strict";var t={};t.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"==typeof window)return window}}(),(()=>{var e;t.g.importScripts&&(e=t.g.location+"");var i=t.g.document;if(!e&&i&&(i.currentScript&&(e=i.currentScript.src),!e)){var s=i.getElementsByTagName("script");s.length&&(e=s[s.length-1].src)}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),t.p=e})();const e=window.ShadowRoot&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol();class s{constructor(t,e){if(e!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t}get styleSheet(){return e&&void 0===this.t&&(this.t=new CSSStyleSheet,this.t.replaceSync(this.cssText)),this.t}toString(){return this.cssText}}const r=new Map,o=t=>{let e=r.get(t);return void 0===e&&r.set(t,e=new s(t,i)),e},n=e?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return(t=>o("string"==typeof t?t:t+""))(e)})(t):t;var l,a,h,d;const c={toAttribute(t,e){switch(e){case Boolean:t=t?"":null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},u=(t,e)=>e!==t&&(e==e||t==t),p={attribute:!0,type:String,converter:c,reflect:!1,hasChanged:u};class v extends HTMLElement{constructor(){super(),this.Πi=new Map,this.Πo=void 0,this.Πl=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this.Πh=null,this.u()}static addInitializer(t){var e;null!==(e=this.v)&&void 0!==e||(this.v=[]),this.v.push(t)}static get observedAttributes(){this.finalize();const t=[];return this.elementProperties.forEach(((e,i)=>{const s=this.Πp(i,e);void 0!==s&&(this.Πm.set(s,i),t.push(s))})),t}static createProperty(t,e=p){if(e.state&&(e.attribute=!1),this.finalize(),this.elementProperties.set(t,e),!e.noAccessor&&!this.prototype.hasOwnProperty(t)){const i="symbol"==typeof t?Symbol():"__"+t,s=this.getPropertyDescriptor(t,i,e);void 0!==s&&Object.defineProperty(this.prototype,t,s)}}static getPropertyDescriptor(t,e,i){return{get(){return this[e]},set(s){const r=this[t];this[e]=s,this.requestUpdate(t,r,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)||p}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const t=Object.getPrototypeOf(this);if(t.finalize(),this.elementProperties=new Map(t.elementProperties),this.Πm=new Map,this.hasOwnProperty("properties")){const t=this.properties,e=[...Object.getOwnPropertyNames(t),...Object.getOwnPropertySymbols(t)];for(const i of e)this.createProperty(i,t[i])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(n(t))}else void 0!==t&&e.push(n(t));return e}static Πp(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}u(){var t;this.Πg=new Promise((t=>this.enableUpdating=t)),this.L=new Map,this.Π_(),this.requestUpdate(),null===(t=this.constructor.v)||void 0===t||t.forEach((t=>t(this)))}addController(t){var e,i;(null!==(e=this.ΠU)&&void 0!==e?e:this.ΠU=[]).push(t),void 0!==this.renderRoot&&this.isConnected&&(null===(i=t.hostConnected)||void 0===i||i.call(t))}removeController(t){var e;null===(e=this.ΠU)||void 0===e||e.splice(this.ΠU.indexOf(t)>>>0,1)}Π_(){this.constructor.elementProperties.forEach(((t,e)=>{this.hasOwnProperty(e)&&(this.Πi.set(e,this[e]),delete this[e])}))}createRenderRoot(){var t;const i=null!==(t=this.shadowRoot)&&void 0!==t?t:this.attachShadow(this.constructor.shadowRootOptions);return((t,i)=>{e?t.adoptedStyleSheets=i.map((t=>t instanceof CSSStyleSheet?t:t.styleSheet)):i.forEach((e=>{const i=document.createElement("style");i.textContent=e.cssText,t.appendChild(i)}))})(i,this.constructor.elementStyles),i}connectedCallback(){var t;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(t=this.ΠU)||void 0===t||t.forEach((t=>{var e;return null===(e=t.hostConnected)||void 0===e?void 0:e.call(t)})),this.Πl&&(this.Πl(),this.Πo=this.Πl=void 0)}enableUpdating(t){}disconnectedCallback(){var t;null===(t=this.ΠU)||void 0===t||t.forEach((t=>{var e;return null===(e=t.hostDisconnected)||void 0===e?void 0:e.call(t)})),this.Πo=new Promise((t=>this.Πl=t))}attributeChangedCallback(t,e,i){this.K(t,i)}Πj(t,e,i=p){var s,r;const o=this.constructor.Πp(t,i);if(void 0!==o&&!0===i.reflect){const n=(null!==(r=null===(s=i.converter)||void 0===s?void 0:s.toAttribute)&&void 0!==r?r:c.toAttribute)(e,i.type);this.Πh=t,null==n?this.removeAttribute(o):this.setAttribute(o,n),this.Πh=null}}K(t,e){var i,s,r;const o=this.constructor,n=o.Πm.get(t);if(void 0!==n&&this.Πh!==n){const t=o.getPropertyOptions(n),l=t.converter,a=null!==(r=null!==(s=null===(i=l)||void 0===i?void 0:i.fromAttribute)&&void 0!==s?s:"function"==typeof l?l:null)&&void 0!==r?r:c.fromAttribute;this.Πh=n,this[n]=a(e,t.type),this.Πh=null}}requestUpdate(t,e,i){let s=!0;void 0!==t&&(((i=i||this.constructor.getPropertyOptions(t)).hasChanged||u)(this[t],e)?(this.L.has(t)||this.L.set(t,e),!0===i.reflect&&this.Πh!==t&&(void 0===this.Πk&&(this.Πk=new Map),this.Πk.set(t,i))):s=!1),!this.isUpdatePending&&s&&(this.Πg=this.Πq())}async Πq(){this.isUpdatePending=!0;try{for(await this.Πg;this.Πo;)await this.Πo}catch(t){Promise.reject(t)}const t=this.performUpdate();return null!=t&&await t,!this.isUpdatePending}performUpdate(){var t;if(!this.isUpdatePending)return;this.hasUpdated,this.Πi&&(this.Πi.forEach(((t,e)=>this[e]=t)),this.Πi=void 0);let e=!1;const i=this.L;try{e=this.shouldUpdate(i),e?(this.willUpdate(i),null===(t=this.ΠU)||void 0===t||t.forEach((t=>{var e;return null===(e=t.hostUpdate)||void 0===e?void 0:e.call(t)})),this.update(i)):this.Π$()}catch(t){throw e=!1,this.Π$(),t}e&&this.E(i)}willUpdate(t){}E(t){var e;null===(e=this.ΠU)||void 0===e||e.forEach((t=>{var e;return null===(e=t.hostUpdated)||void 0===e?void 0:e.call(t)})),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}Π$(){this.L=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this.Πg}shouldUpdate(t){return!0}update(t){void 0!==this.Πk&&(this.Πk.forEach(((t,e)=>this.Πj(e,this[e],t))),this.Πk=void 0),this.Π$()}updated(t){}firstUpdated(t){}}var m,f,y,g;v.finalized=!0,v.elementProperties=new Map,v.elementStyles=[],v.shadowRootOptions={mode:"open"},null===(a=(l=globalThis).reactiveElementPlatformSupport)||void 0===a||a.call(l,{ReactiveElement:v}),(null!==(h=(d=globalThis).reactiveElementVersions)&&void 0!==h?h:d.reactiveElementVersions=[]).push("1.0.0-rc.2");const b=globalThis.trustedTypes,w=b?b.createPolicy("lit-html",{createHTML:t=>t}):void 0,S=`lit$${(Math.random()+"").slice(9)}$`,k="?"+S,$=`<${k}>`,x=document,C=(t="")=>x.createComment(t),E=t=>null===t||"object"!=typeof t&&"function"!=typeof t,P=Array.isArray,U=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,A=/-->/g,H=/>/g,T=/>|[ 	\n\r](?:([^\s"'>=/]+)([ 	\n\r]*=[ 	\n\r]*(?:[^ 	\n\r"'`<>=]|("|')|))|$)/g,N=/'/g,_=/"/g,O=/^(?:script|style|textarea)$/i,R=t=>(e,...i)=>({_$litType$:t,strings:e,values:i}),B=R(1),z=(R(2),Symbol.for("lit-noChange")),F=Symbol.for("lit-nothing"),M=new WeakMap,j=x.createTreeWalker(x,129,null,!1);class L{constructor({strings:t,_$litType$:e},i){let s;this.parts=[];let r=0,o=0;const n=t.length-1,l=this.parts,[a,h]=((t,e)=>{const i=t.length-1,s=[];let r,o=2===e?"<svg>":"",n=U;for(let e=0;e<i;e++){const i=t[e];let l,a,h=-1,d=0;for(;d<i.length&&(n.lastIndex=d,a=n.exec(i),null!==a);)d=n.lastIndex,n===U?"!--"===a[1]?n=A:void 0!==a[1]?n=H:void 0!==a[2]?(O.test(a[2])&&(r=RegExp("</"+a[2],"g")),n=T):void 0!==a[3]&&(n=T):n===T?">"===a[0]?(n=null!=r?r:U,h=-1):void 0===a[1]?h=-2:(h=n.lastIndex-a[2].length,l=a[1],n=void 0===a[3]?T:'"'===a[3]?_:N):n===_||n===N?n=T:n===A||n===H?n=U:(n=T,r=void 0);const c=n===T&&t[e+1].startsWith("/>")?" ":"";o+=n===U?i+$:h>=0?(s.push(l),i.slice(0,h)+"$lit$"+i.slice(h)+S+c):i+S+(-2===h?(s.push(void 0),e):c)}const l=o+(t[i]||"<?>")+(2===e?"</svg>":"");return[void 0!==w?w.createHTML(l):l,s]})(t,e);if(this.el=L.createElement(a,i),j.currentNode=this.el.content,2===e){const t=this.el.content,e=t.firstChild;e.remove(),t.append(...e.childNodes)}for(;null!==(s=j.nextNode())&&l.length<n;){if(1===s.nodeType){if(s.hasAttributes()){const t=[];for(const e of s.getAttributeNames())if(e.endsWith("$lit$")||e.startsWith(S)){const i=h[o++];if(t.push(e),void 0!==i){const t=s.getAttribute(i.toLowerCase()+"$lit$").split(S),e=/([.?@])?(.*)/.exec(i);l.push({type:1,index:r,name:e[2],strings:t,ctor:"."===e[1]?V:"?"===e[1]?K:"@"===e[1]?J:W})}else l.push({type:6,index:r})}for(const e of t)s.removeAttribute(e)}if(O.test(s.tagName)){const t=s.textContent.split(S),e=t.length-1;if(e>0){s.textContent=b?b.emptyScript:"";for(let i=0;i<e;i++)s.append(t[i],C()),j.nextNode(),l.push({type:2,index:++r});s.append(t[e],C())}}}else if(8===s.nodeType)if(s.data===k)l.push({type:2,index:r});else{let t=-1;for(;-1!==(t=s.data.indexOf(S,t+1));)l.push({type:7,index:r}),t+=S.length-1}r++}}static createElement(t,e){const i=x.createElement("template");return i.innerHTML=t,i}}function I(t,e,i=t,s){var r,o,n,l;if(e===z)return e;let a=void 0!==s?null===(r=i.Σi)||void 0===r?void 0:r[s]:i.Σo;const h=E(e)?void 0:e._$litDirective$;return(null==a?void 0:a.constructor)!==h&&(null===(o=null==a?void 0:a.O)||void 0===o||o.call(a,!1),void 0===h?a=void 0:(a=new h(t),a.T(t,i,s)),void 0!==s?(null!==(n=(l=i).Σi)&&void 0!==n?n:l.Σi=[])[s]=a:i.Σo=a),void 0!==a&&(e=I(t,a.S(t,e.values),a,s)),e}class q{constructor(t,e){this.l=[],this.N=void 0,this.D=t,this.M=e}u(t){var e;const{el:{content:i},parts:s}=this.D,r=(null!==(e=null==t?void 0:t.creationScope)&&void 0!==e?e:x).importNode(i,!0);j.currentNode=r;let o=j.nextNode(),n=0,l=0,a=s[0];for(;void 0!==a;){if(n===a.index){let e;2===a.type?e=new D(o,o.nextSibling,this,t):1===a.type?e=new a.ctor(o,a.name,a.strings,this,t):6===a.type&&(e=new Z(o,this,t)),this.l.push(e),a=s[++l]}n!==(null==a?void 0:a.index)&&(o=j.nextNode(),n++)}return r}v(t){let e=0;for(const i of this.l)void 0!==i&&(void 0!==i.strings?(i.I(t,i,e),e+=i.strings.length-2):i.I(t[e])),e++}}class D{constructor(t,e,i,s){this.type=2,this.N=void 0,this.A=t,this.B=e,this.M=i,this.options=s}setConnected(t){var e;null===(e=this.P)||void 0===e||e.call(this,t)}get parentNode(){return this.A.parentNode}get startNode(){return this.A}get endNode(){return this.B}I(t,e=this){t=I(this,t,e),E(t)?t===F||null==t||""===t?(this.H!==F&&this.R(),this.H=F):t!==this.H&&t!==z&&this.m(t):void 0!==t._$litType$?this._(t):void 0!==t.nodeType?this.$(t):(t=>{var e;return P(t)||"function"==typeof(null===(e=t)||void 0===e?void 0:e[Symbol.iterator])})(t)?this.g(t):this.m(t)}k(t,e=this.B){return this.A.parentNode.insertBefore(t,e)}$(t){this.H!==t&&(this.R(),this.H=this.k(t))}m(t){const e=this.A.nextSibling;null!==e&&3===e.nodeType&&(null===this.B?null===e.nextSibling:e===this.B.previousSibling)?e.data=t:this.$(x.createTextNode(t)),this.H=t}_(t){var e;const{values:i,_$litType$:s}=t,r="number"==typeof s?this.C(t):(void 0===s.el&&(s.el=L.createElement(s.h,this.options)),s);if((null===(e=this.H)||void 0===e?void 0:e.D)===r)this.H.v(i);else{const t=new q(r,this),e=t.u(this.options);t.v(i),this.$(e),this.H=t}}C(t){let e=M.get(t.strings);return void 0===e&&M.set(t.strings,e=new L(t)),e}g(t){P(this.H)||(this.H=[],this.R());const e=this.H;let i,s=0;for(const r of t)s===e.length?e.push(i=new D(this.k(C()),this.k(C()),this,this.options)):i=e[s],i.I(r),s++;s<e.length&&(this.R(i&&i.B.nextSibling,s),e.length=s)}R(t=this.A.nextSibling,e){var i;for(null===(i=this.P)||void 0===i||i.call(this,!1,!0,e);t&&t!==this.B;){const e=t.nextSibling;t.remove(),t=e}}}class W{constructor(t,e,i,s,r){this.type=1,this.H=F,this.N=void 0,this.V=void 0,this.element=t,this.name=e,this.M=s,this.options=r,i.length>2||""!==i[0]||""!==i[1]?(this.H=Array(i.length-1).fill(F),this.strings=i):this.H=F}get tagName(){return this.element.tagName}I(t,e=this,i,s){const r=this.strings;let o=!1;if(void 0===r)t=I(this,t,e,0),o=!E(t)||t!==this.H&&t!==z,o&&(this.H=t);else{const s=t;let n,l;for(t=r[0],n=0;n<r.length-1;n++)l=I(this,s[i+n],e,n),l===z&&(l=this.H[n]),o||(o=!E(l)||l!==this.H[n]),l===F?t=F:t!==F&&(t+=(null!=l?l:"")+r[n+1]),this.H[n]=l}o&&!s&&this.W(t)}W(t){t===F?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=t?t:"")}}class V extends W{constructor(){super(...arguments),this.type=3}W(t){this.element[this.name]=t===F?void 0:t}}class K extends W{constructor(){super(...arguments),this.type=4}W(t){t&&t!==F?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name)}}class J extends W{constructor(){super(...arguments),this.type=5}I(t,e=this){var i;if((t=null!==(i=I(this,t,e,0))&&void 0!==i?i:F)===z)return;const s=this.H,r=t===F&&s!==F||t.capture!==s.capture||t.once!==s.once||t.passive!==s.passive,o=t!==F&&(s===F||r);r&&this.element.removeEventListener(this.name,this,s),o&&this.element.addEventListener(this.name,this,t),this.H=t}handleEvent(t){var e,i;"function"==typeof this.H?this.H.call(null!==(i=null===(e=this.options)||void 0===e?void 0:e.host)&&void 0!==i?i:this.element,t):this.H.handleEvent(t)}}class Z{constructor(t,e,i){this.element=t,this.type=6,this.N=void 0,this.V=void 0,this.M=e,this.options=i}I(t){I(this,t)}}var G,Q,X,Y,tt,et;null===(f=(m=globalThis).litHtmlPlatformSupport)||void 0===f||f.call(m,L,D),(null!==(y=(g=globalThis).litHtmlVersions)&&void 0!==y?y:g.litHtmlVersions=[]).push("2.0.0-rc.3"),(null!==(G=(et=globalThis).litElementVersions)&&void 0!==G?G:et.litElementVersions=[]).push("3.0.0-rc.2");class it extends v{constructor(){super(...arguments),this.renderOptions={host:this},this.Φt=void 0}createRenderRoot(){var t,e;const i=super.createRenderRoot();return null!==(t=(e=this.renderOptions).renderBefore)&&void 0!==t||(e.renderBefore=i.firstChild),i}update(t){const e=this.render();super.update(t),this.Φt=((t,e,i)=>{var s,r;const o=null!==(s=null==i?void 0:i.renderBefore)&&void 0!==s?s:e;let n=o._$litPart$;if(void 0===n){const t=null!==(r=null==i?void 0:i.renderBefore)&&void 0!==r?r:null;o._$litPart$=n=new D(e.insertBefore(C(),t),t,void 0,i)}return n.I(t),n})(e,this.renderRoot,this.renderOptions)}connectedCallback(){var t;super.connectedCallback(),null===(t=this.Φt)||void 0===t||t.setConnected(!0)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this.Φt)||void 0===t||t.setConnected(!1)}render(){return z}}it.finalized=!0,it._$litElement$=!0,null===(X=(Q=globalThis).litElementHydrateSupport)||void 0===X||X.call(Q,{LitElement:it}),null===(tt=(Y=globalThis).litElementPlatformSupport)||void 0===tt||tt.call(Y,{LitElement:it});const st=(t,e)=>"method"===e.kind&&e.descriptor&&!("value"in e.descriptor)?{...e,finisher(i){i.createProperty(e.key,t)}}:{kind:"field",key:Symbol(),placement:"own",descriptor:{},originalKey:e.key,initializer(){"function"==typeof e.initializer&&(this[e.key]=e.initializer.call(this))},finisher(i){i.createProperty(e.key,t)}};function rt(t){return(e,i)=>void 0!==i?((t,e,i)=>{e.constructor.createProperty(i,t)})(t,e,i):st(t,e)}const ot=Element.prototype;ot.msMatchesSelector||ot.webkitMatchesSelector;const nt=((t,...e)=>{const i=1===t.length?t[0]:e.reduce(((e,i,r)=>e+(t=>{if(t instanceof s)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[r+1]),t[0]);return o(i)})`.mgnify-sourmash-component {
  display: flex;
  flex-direction: column;
  font-family: Helvetica, Arial, FreeSans, Liberation Sans, sans-serif;
}
label.file {
  position: relative;
  display: inline-block;
  cursor: pointer;
  height: 2.5rem;
  box-sizing: border-box;
  color: #5a5a5a;
  border: 0.075rem solid #ddd;
  border-radius: 0 0.25rem 0.25rem 0;
}
.file-custom:after {
  content: attr(data-label);
  position: absolute;
  inset: -0.075rem -0.075rem -0.075rem 0px;
  padding: 0.5rem 1rem;
  line-height: 1.5;
}
.file-custom:before {
  position: absolute;
  top: -0.075rem;
  right: -0.075rem;
  bottom: -0.075rem;
  z-index: 6;
  display: block;
  content: 'Browse';
  padding: 0.5rem 1rem;
  line-height: 1.5;
  color: #555;
  background-color: #eee;
  border: 0.075rem solid #ddd;
  border-radius: 0 0.25rem 0.25rem 0;
}
input[type='file'] {
  min-width: 14rem;
  margin: 0;
  opacity: 0;
}
div.mode-selector {
  display: flex;
  flex-direction: row-reverse;
  margin-top: 0.4em;
}
div.mode-selector button {
  background-color: #eee;
  color: #555;
  padding: 0.5em;
  margin: 0;
  appearance: none;
  border: 0;
  border-radius: 0 0.25rem 0.25rem 0;
}
div.mode-selector button:nth-child(even) {
  border-radius: 0.25rem 0 0 0.25rem;
}
div.mode-selector button.selected {
  background-color: #444;
  color: #fefefe;
  font-weight: bold;
}

.mgnify-sourmash-component ul {
  list-style-type: none;
}
.mgnify-sourmash-component ul li {
  margin-bottom: 0.8em;
}
.mgnify-sourmash-component progress {
  display: block;
  min-width: 50vw;
  height: 0.4em;
}
`;var lt=function(t,e,i,s){var r,o=arguments.length,n=o<3?e:null===s?s=Object.getOwnPropertyDescriptor(e,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(t,e,i,s);else for(var l=t.length-1;l>=0;l--)(r=t[l])&&(n=(o<3?r(n):o>3?r(e,i,n):r(e,i))||n);return o>3&&n&&Object.defineProperty(e,i,n),n};const at=new function(){return new Worker(t.p+"mgnify-sourmash-component.worker.js")},ht=[".fa",".fasta",".fna"];let dt=class extends it{constructor(){super(),this.directory=!1,this.show_directory_checkbox=!1,this.show_signatures=!1,this.num=0,this.ksize=31,this.is_protein=!1,this.dayhoff=!1,this.hp=!1,this.seed=42,this.scaled=1e3,this.track_abundance=!1,this.selectedFiles=null,this.progress={},this.signatures={},this.errors={},at.addEventListener("message",(t=>{var e;switch(null===(e=null==t?void 0:t.data)||void 0===e?void 0:e.type){case"progress:read":this.progress[t.data.filename]=t.data.progress,this.requestUpdate();break;case"signature:error":this.errors[t.data.filename]=t.data.error,this.dispatchEvent(new CustomEvent("sketchedError",{bubbles:!0,detail:{filename:t.data.filename,error:t.data.error}})),this.requestUpdate();break;case"signature:generated":this.signatures[t.data.filename]=t.data.signature,this.progress[t.data.filename]=100,this.dispatchEvent(new CustomEvent("sketched",{bubbles:!0,detail:{filename:t.data.filename,signature:t.data.signature}})),this.haveCompletedAllSignatures()&&this.dispatchEvent(new CustomEvent("sketchedall",{bubbles:!0,detail:{signatures:this.signatures,errors:this.errors}})),this.requestUpdate()}}))}haveCompletedAllSignatures(){return Object.keys(this.progress).every((t=>t in this.signatures||t in this.errors))}setChecked(t){this.directory=t.target.checked}clear(){this.selectedFiles=null,this.progress={},this.signatures={},this.errors={},this.renderRoot.querySelector("#sourmash-selector").value=null,this.requestUpdate()}renderSelectedFiles(){var t;return((null===(t=this.selectedFiles)||void 0===t?void 0:t.length)||0)<1?"":B`
      <div>
        <h2>Selected Files:</h2>
        <ul>
          ${this.selectedFiles.map((t=>{var e;const i=(null===(e=this.progress)||void 0===e?void 0:e[t.name])||0,s=this.signatures[t.name],r=this.errors[t.name];let o=B``;return s&&(o=B`✅`),r&&(o=B`<span title=${r}>⚠️<code>${r}</code></span>`),B` <li>
              ${t.name} ${o}
              <progress
                id=${t.name}
                max="100"
                value=${(t=>null!=t?t:F)(i>100?void 0:i)}
              >
                ${i.toFixed(2)}%
              </progress>
              ${this.show_signatures&&(null==s?void 0:s.length)?B`
                    <details>
                      <summary>See signature</summary>
                      <pre>${s}</pre>
                    </details>
                  `:""}
            </li>`}))}
        </ul>
      </div>
    `}render(){var t,e;let i=this.directory?"Choose a directory...":"Choose Files...";return(null===(t=this.selectedFiles)||void 0===t?void 0:t.length)&&(i=`${null===(e=this.selectedFiles)||void 0===e?void 0:e.length} Files Selected`),B`
      <div class="mgnify-sourmash-component">
        <label
          >Select ${this.is_protein?"protein":"nucleotides"} FastA
          files:</label
        >
        <label class="file" for="sourmash-selector">
          <input
            type="file"
            id="sourmash-selector"
            name="sourmash-selector"
            accept=${ht.join(",")}
            @change=${this.handleFileChanges}
            ?webkitdirectory=${this.directory}
            ?multiple=${!this.directory}
          />
          <span class="file-custom" data-label=${i}></span>
        </label>
        ${this.show_directory_checkbox?B`
              <div class="mode-selector">
                <button
                  class=${this.directory?"":"selected"}
                  @click=${()=>this.directory=!1}
                >
                  Files
                </button>
                <button
                  class=${this.directory?"selected":""}
                  @click=${()=>this.directory=!0}
                >
                  Directory
                </button>
              </div>
            `:""}
        ${this.renderSelectedFiles()}
      </div>
    `}handleFileChanges(t){t.preventDefault(),this.selectedFiles=Array.from(t.currentTarget.files).filter((t=>{for(const e of ht)if(t.name.endsWith(e))return!0;return!1})),at.postMessage({files:this.selectedFiles,options:{num:this.num,ksize:this.ksize,is_protein:this.is_protein,dayhoff:this.dayhoff,hp:this.hp,seed:this.seed,scaled:this.scaled,track_abundance:this.track_abundance}}),this.dispatchEvent(new CustomEvent("change",{bubbles:!0,detail:{selectedFiles:this.selectedFiles}})),this.requestUpdate()}};dt.styles=[nt],lt([rt({type:Boolean,reflect:!0})],dt.prototype,"directory",void 0),lt([rt({type:Boolean})],dt.prototype,"show_directory_checkbox",void 0),lt([rt({type:Boolean})],dt.prototype,"show_signatures",void 0),lt([rt({type:Number})],dt.prototype,"num",void 0),lt([rt({type:Number})],dt.prototype,"ksize",void 0),lt([rt({type:Boolean})],dt.prototype,"is_protein",void 0),lt([rt({type:Boolean})],dt.prototype,"dayhoff",void 0),lt([rt({type:Boolean})],dt.prototype,"hp",void 0),lt([rt({type:Number})],dt.prototype,"seed",void 0),lt([rt({type:Number})],dt.prototype,"scaled",void 0),lt([rt({type:Boolean})],dt.prototype,"track_abundance",void 0),dt=lt([t=>"function"==typeof t?((t,e)=>(window.customElements.define("mgnify-sourmash-component",e),e))(0,t):((t,e)=>{const{kind:i,elements:s}=e;return{kind:i,elements:s,finisher(t){window.customElements.define("mgnify-sourmash-component",t)}}})(0,t)],dt)})();
//# sourceMappingURL=mgnify-sourmash-component.js.map