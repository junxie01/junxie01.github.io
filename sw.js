/**
 * 自动引入模板，在原有 sw-precache 插件默认模板基础上做的二次开发
 *
 * 因为是自定导入的模板，项目一旦生成，不支持随 sw-precache 的版本自动升级。
 * 可以到 Lavas 官网下载 basic 模板内获取最新模板进行替换
 *
 */

/* eslint-disable */

'use strict';

var precacheConfig = [["/2006/06/11/2006061115/index.html","9cb8291f17a174c3af5e06952192fcd1"],["/2006/11/24/2006112420/index.html","ee7e8e568e7580797b4429bc8887bcc9"],["/2007/04/14/2007041411/index.html","94f866793b5afc402305dc527df4d028"],["/2007/12/13/2007121321/index.html","7a23c4a2ae31b8c9105fb938f2382137"],["/2008/07/27/2008072721/index.html","c5c62af7057f0620ecc6714e06917a82"],["/2009/02/17/2009021713/index.html","e1ab8db6564a1936d65fce5dd6ba11e7"],["/2009/04/10/2009041021/index.html","38240787bef73f6025a354c97ea8dcaf"],["/2009/08/12/2009081221/index.html","c32800d24b976e98dd0bb7916762c772"],["/2009/08/12/200908122116/index.html","4cd431c7f118503f02bedd3f3f7cb443"],["/2009/08/18/2009081813/index.html","80f9e65d161f6ca05798f752137c5b59"],["/2009/10/30/2009103019/index.html","194ff564c093c726b475df47310cc5e1"],["/2009/11/20/2009112021/index.html","3410e384563a1d523b7da7e512b57e5d"],["/2009/12/14/2009121418/index.html","f0706f50ba549fa8e844e4e56f8c9a2a"],["/2009/12/19/2009121913/index.html","76710a6e2d9d837302d6ffd1da01ebc7"],["/2009/12/23/2009122319/index.html","9be34eb70cdce0c6a8c423ccbfc69c9b"],["/2010/01/01/2010010110/index.html","8009d942d01a6d83a2ea69e689cc082d"],["/2010/01/04/2010010420/index.html","364146563b9e60607fc135f535daefc3"],["/2010/01/12/2010011223/index.html","66cf45109710c1021b782f33665e47e3"],["/2010/02/06/2010020613/index.html","d401946ebe94d7a2a518147369ab9681"],["/2010/04/30/2010043013/index.html","d9463965f44c5fa17086ff204a60e337"],["/2010/08/10/2010081013/index.html","ecc6634d2586e9d1adafd6115ce15d1b"],["/2010/10/11/2010101113/index.html","f9c6d4553aa51353aca3928a2e5218cc"],["/2010/10/21/2010102114/index.html","0b5f56400c3467446da5cb4dc37708ac"],["/2010/11/12/2010111213/index.html","e2ae1bedfd618124531a084102a9e4c1"],["/2011/01/13/2011011303/index.html","90167fc0120b91f321166cd187fb5d42"],["/2011/02/18/2011021823/index.html","b790004b9d05f15b86266efb803b7fbc"],["/2011/02/19/2011021214/index.html","cb1912db5b8869b67da9d076475d6f14"],["/2011/02/22/2011022214/index.html","ed6df17427dbf2a1d108b53ee8a5bca2"],["/2011/02/26/2011022622/index.html","dd2deb6559989f90dec069d7bc3be666"],["/2012/02/09/alive/index.html","fcfb126e90f3464f0dbf6e8df7320c61"],["/2012/04/01/2012040119/index.html","c9ae80401bd6eb0ba7ae858c9ecf1435"],["/2013/12/09/2013120921/index.html","9c353ff86efb90e4cfa4b049d81acd70"],["/2013/12/24/2013122401/index.html","2e2b58e665c9a814b28cafc5aa32865f"],["/2015/07/08/2015070811/index.html","eb2afb192990f9c5c49ad4b2f19b3e29"],["/2015/11/01/2015110108/index.html","2f7b701d58ffffb2fe9fffa71259ce8d"],["/2015/11/01/201511010818/index.html","5ddafb189aac31948403ee144ce2df89"],["/2015/11/01/201511010820/index.html","4025bebcc00d32b23f02dbcc922230da"],["/2020/05/26/hello-world/index.html","b4a90a796cd89d5fbacfbe6620d35584"],["/2020/05/30/reply-to-review/index.html","9274077856e6afc09d66e467565a13aa"],["/2020/05/31/donation/donate.png","67d4490de259d094d11c5a1a428b5bc4"],["/2020/05/31/donation/index.html","815db28215f18e6fde9b8a0909e966f3"],["/2020/05/31/how-to-backup/index.html","05f8c7ee58c9b95a3768ebcd13107c01"],["/2020/05/31/no-passwd-for-deploy/index.html","24de325e7d95603f7919a2ad4a0aa430"],["/2020/05/31/picture-view/index.html","3646ee2f5fc5b034bd1a72c5625954a5"],["/2020/05/31/word-count/index.html","bab0d095176bac9ad5d1a07623e43826"],["/2020/06/03/20200603/index.html","198c25d75dcdc041d81275fd04c51e40"],["/2020/06/03/2020060323/index.html","9ffe853f73c97fde2c98dc2df5b1a709"],["/2020/06/04/2020060401/index.html","71e924007aa4a27a5a08059f566dffc7"],["/2020/06/05/2020060500/index.html","bf0a92f6d28ea21763102634d47ec9af"],["/2020/06/05/2020060513/index.html","95076f5fc3f1c2c5a86c1ac1dce44125"],["/2020/06/10/what-did-I-do-to-this-blog/index.html","d0c500322ab9fd7f188492bf2ee665c6"],["/2020/06/12/learn-sed/index.html","4f1754e713754db209fc127fe793907a"],["/about/index.html","02b978ce4117cf6ab9771f4257ad07a2"],["/archives/2006/06/index.html","449e88e303af4aa9946bde6bd1137387"],["/archives/2006/11/index.html","0373be7c24220c2e37afa9fee41b502e"],["/archives/2006/index.html","0ff56d2d78bda82792ba5a720171b202"],["/archives/2007/04/index.html","3977a9eec8cbb2b573160304f7322b90"],["/archives/2007/12/index.html","2d6589a4c14ba5fcc8b2bfb2bf55ab42"],["/archives/2007/index.html","aab5672e9cfe8d2e75c595bccbd072b6"],["/archives/2008/07/index.html","81473579f0af7cbe0db36f5b8fc7e56e"],["/archives/2008/index.html","fc133c78d06cebade96ae33d10250303"],["/archives/2009/02/index.html","100c3481e9b57b345b666a7268c48e6b"],["/archives/2009/04/index.html","6fa78ce8af56f063bc8c45fa5a494998"],["/archives/2009/08/index.html","2fa9ea0003c6350d783376d1230a4e55"],["/archives/2009/10/index.html","04e73d7039f40337d7e1a0921188efd5"],["/archives/2009/11/index.html","e6609df4234d217284e337be8930bb46"],["/archives/2009/12/index.html","d80f248010476cbe031599bf9f13c969"],["/archives/2009/index.html","1dcb28d9b7f2d318d63a057c70d5fb92"],["/archives/2010/01/index.html","a9374cf15f67e9467f20682a6efa9a80"],["/archives/2010/02/index.html","2638bb9faf58efd56aa292c4726fe2a8"],["/archives/2010/04/index.html","35865b9a52ccc716319af9dcc0699f69"],["/archives/2010/08/index.html","535387e4be6085f8c370da563a6bd03a"],["/archives/2010/10/index.html","d01d7f22c3c5c99f08a17cf4ea7c65c6"],["/archives/2010/11/index.html","02104fda67805277ee0ec6cda0505d83"],["/archives/2010/index.html","fca84fc5ba4a60d2bc7e0d6a173c6bba"],["/archives/2011/01/index.html","4071a59e99f84627e4b3822d36a12611"],["/archives/2011/02/index.html","d13b1a26249f1086ddebf0c0adf98da7"],["/archives/2011/index.html","1aabef1f13db158348abf67a0c50d29e"],["/archives/2012/02/index.html","52a1391414db017a0c8491d30c7a9789"],["/archives/2012/04/index.html","b44f41f73e6aa68465e729fe333db142"],["/archives/2012/index.html","9020924af080707d385049d2a9de2920"],["/archives/2013/12/index.html","c83fc543b9639a43f1c098b27711da0c"],["/archives/2013/index.html","e6ad34f572f267df81206c6aa9b812f2"],["/archives/2015/07/index.html","4e509a2d6b45cbead02fba7b81dad87c"],["/archives/2015/11/index.html","67e4d78b1e8784889616afd43d297c20"],["/archives/2015/index.html","938abc45ab26c90b462e293e156f66a5"],["/archives/2020/05/index.html","1ee1412732fa31ed4543af7c5e3aa658"],["/archives/2020/06/index.html","fd98696c99d1c11f8c7a0ddf083842d4"],["/archives/2020/index.html","a5bec40e2d87e568289125397c8f88a5"],["/archives/2020/page/2/index.html","592df5a0f4441e8658556421a0576b10"],["/archives/index.html","0dc43df3531d8ee857a4f2fa3ce02161"],["/archives/page/2/index.html","3bd89d7097d081ccf3fb72f3bfc11c79"],["/archives/page/3/index.html","a9a922a4f0eb1d7db607dcb132ad7305"],["/archives/page/4/index.html","9a1d5b293ba48b4acb83946637098e54"],["/archives/page/5/index.html","6ad15dde82b1fd9a65b35232c34e4f6c"],["/archives/page/6/index.html","91a935f53f7605af00cb3868762c8900"],["/bundle.js","461350bf2dbc841f4a7bce05e17dd3c1"],["/categories/Linux/index.html","8c6af55efea3a17cbc919232d33a5dfb"],["/categories/index.html","46d5164f07a5b07307638b5fea67cba3"],["/categories/web/index.html","2f3ae1c4db8c544e1dc5a696af601d0a"],["/categories/work/index.html","806f16ff7a988a295b09040d06d59ed7"],["/categories/乱笔/index.html","02f37b5cf0d28d8ae89e4d9ce2cf3044"],["/categories/日记/index.html","c0dcce56dce5a9e523f9f87bcb998bc0"],["/categories/杂/index.html","54c7e92f31aa709b018d33c35d6e6891"],["/categories/网易迁移/index.html","8510b56233934b37c4fd4f48617434c2"],["/categories/网易迁移/page/2/index.html","111c48e7a27fe3cc9adc060d34521c29"],["/categories/网易迁移/page/3/index.html","8d66c6fe3cb16cb7569d8b75258aeabd"],["/categories/网易迁移/page/4/index.html","3f2d74e0f8e4375e8eef4af6033ae2d1"],["/categories/网站/index.html","90aa654f18a1bcfc6b4556c2dac2493e"],["/css/main.css","e5b46668a789b9cb11f95a929af466a4"],["/images/algolia_logo.svg","fd40b88ac5370a5353a50b8175c1f367"],["/images/alipay.jpg","e15d3e9d21f4b0ffdf7d1a565a581085"],["/images/apple-touch-icon-next.png","fce961f0bd3cd769bf9c605ae6749bc0"],["/images/avatar.gif","7a2fe6b906600a9354cece6d9ced2992"],["/images/cc-by-nc-nd.svg","1c681acc4a150e7236254c464bb5a797"],["/images/cc-by-nc-sa.svg","12b4b29e8453be5b7828b524d3feabce"],["/images/cc-by-nc.svg","dd9cfe99ed839a4a548114f988d653f4"],["/images/cc-by-nd.svg","2d80546af20128215dc1e23ef42d06c2"],["/images/cc-by-sa.svg","c696b3db81cbbfba32f66c1dc88b909a"],["/images/cc-by.svg","6c4f8422b3725cb9f26b6c00e95fc88b"],["/images/cc-zero.svg","79deee77a07fcb79ff680ac0125eacb9"],["/images/favicon-16x16-next.png","b8975923a585dbaa8519a6068e364947"],["/images/favicon-32x32-next.png","5a029563fe3214c96f68b46556670ea1"],["/images/j-icon-16x16.png","f4d2b9b74d91b70436f8f2c58f70fd53"],["/images/j-icon-32x32.png","7b86e466c4d0c5c7cfc163ca863e5917"],["/images/logo.svg","ddad9027e42111ccd5b466bc18188970"],["/images/wechat_channel.jpg","454d02a3f2d12ef5030437cc3b0ad3ee"],["/images/wechatpay.jpg","8f03594c01fdd3d6e84b9729b28fc3f6"],["/index.html","843e1442025da594a28e952a47cc8791"],["/js/algolia-search.js","d20ec0b4393509b0cdf3258e93d3b11d"],["/js/bookmark.js","a620f0daf2d31576b84e88d0adf0db03"],["/js/local-search.js","3607cdfc2ac57992db02aa090b3cc167"],["/js/motion.js","e8073e03493feb145528c4bdbe613d70"],["/js/next-boot.js","473091bdcc0a3d626c9e119765cd5917"],["/js/schemes/muse.js","160b26ee0326bfba83d6d51988716b08"],["/js/schemes/pisces.js","e383b31dff5fe3117bfb69c0bfb6b33d"],["/js/tagcanvas.js","222f58419252597da4e4b17828824a8f"],["/js/tagcloud.js","aa119b685cd221bf44121e2b8959a279"],["/js/utils.js","e31afcd9b2ac933c3316665937a42b5f"],["/lib/anime.min.js","864a144dbbc956381a47679ec57ab06c"],["/lib/bookmark/README.html","aef4115567a205eedcb9259b609c0298"],["/lib/bookmark/bookmark.min.js","b3d0b76ba186e3a97fd400366a75a4d3"],["/lib/bookmark/index.js","c6a12179b90281058158b012d8a42b06"],["/lib/canvas-nest/README.html","2eb7fb7c12fb28c4e4c052455f4667e6"],["/lib/canvas-nest/canvas-nest-nomobile.min.js","876c47c6a2edc066781c264adf33aec2"],["/lib/canvas-nest/canvas-nest.min.js","36e103d2a05bc706bac40f9ab8881eb7"],["/lib/canvas-nesttom.styl/README.html","2eb7fb7c12fb28c4e4c052455f4667e6"],["/lib/canvas-nesttom.styl/canvas-nest-nomobile.min.js","876c47c6a2edc066781c264adf33aec2"],["/lib/canvas-nesttom.styl/canvas-nest.min.js","36e103d2a05bc706bac40f9ab8881eb7"],["/lib/canvas-ribbon/README.html","d28d8b014eade7b9f0d897e2971583c4"],["/lib/canvas-ribbon/canvas-ribbon.js","952c131e3099dbf7aad0c350355fea0a"],["/lib/fancybox/README.html","12cc8645df339339c5c9c1fa65fcfcd7"],["/lib/fancybox/source/jquery.fancybox.css","caf7c408bb13e802cc3566b94f6c6d8d"],["/lib/fancybox/source/jquery.fancybox.min.css","a2d42584292f64c5827e8b67b1b38726"],["/lib/fancybox/source/jquery.fancybox.min.js","49a6b4d019a934bcf83f0c397eba82d8"],["/lib/fancybox/source/jquery.fancybox.pack.js","b63c7cca1b5e4bd57bd854c444b895c9"],["/lib/font-awesome/css/all.min.css","76cb46c10b6c0293433b371bae2414b2"],["/lib/needsharebutton/README.html","429218f46c22e9aabadfb8a653cd4c2d"],["/lib/needsharebutton/needsharebutton.css","839f806cf996f87b47ca7b8a5a0bfa8f"],["/lib/needsharebutton/needsharebutton.js","1595f4ed0515d2e58b4214b255120304"],["/lib/three/README.html","4009f2198ea44d2c7dee4ffc168c3379"],["/lib/three/canvas_lines.min.js","449a891ad2320817baf609937772f034"],["/lib/three/canvas_sphere.min.js","c441ae63aa5351d63fc2578d87a3deab"],["/lib/three/gulpfile.js","961e92c80d9124f5a338f28d5fb2801f"],["/lib/three/lib/CanvasRenderer.js","90caa1488a37a14eebc22fc37396077a"],["/lib/three/lib/Projector.js","0552b0aca46b57eaec735f14481957d6"],["/lib/three/src/canvas_lines.js","dff9ed0dc04d30410cbdfe13ef918df8"],["/lib/three/src/canvas_sphere.js","7592090aec7351741ca71dd64a8406e9"],["/lib/three/src/three-waves.js","91b77818afd32653a8aca2de8bc5f12d"],["/lib/three/three-waves.min.js","31adf5b1a4966cd3f4215239bc3ed991"],["/lib/three/three.min.js","3298078bce82bdb1afadf5b1a280915e"],["/lib/velocity/velocity.min.js","c1b8d079c7049879838d78e0b389965e"],["/lib/velocity/velocity.ui.min.js","444faf512fb24d50a5dec747cbbe39bd"],["/page/2/index.html","fa7b689599ea65f93b00d01ce9aebfd7"],["/page/3/index.html","8928e7cb1c5f124d260143ebe20c8d27"],["/page/4/index.html","f7a255733d59421f88fbd4e36bb3aa77"],["/page/5/index.html","b5d0e4f8ed3d9c688af63c3a878b7c1c"],["/page/6/index.html","2a4c6ecefb5f8b80401bcdcb24627965"],["/style.css","76cb46c10b6c0293433b371bae2414b2"],["/sw-register.js","bb096683da2c46450e478083b754a32b"],["/tags/Linux/index.html","2674c5fcd2a836dbccb151670fef48d0"],["/tags/hexo/index.html","ec1fe2e6da45b167ba279bc00236a931"],["/tags/index.html","98477d6ebcacf221e761ac0747204a0a"],["/tags/next/index.html","aedc394dcbaf7951ca5257200d68fd35"],["/tags/paper/index.html","170c1cd8f940f57a759b77f6ba25bcfe"],["/tags/sed/index.html","a53ed55375ba4a1cbce80fc9c2ffcd3c"],["/tags/wa/index.html","cd609d3ec409fb79ca4a09af6e35832e"],["/tags/web/index.html","045272cb501607bba566347672f2c3be"],["/tags/一个人/index.html","219772d902fe649c6bbd6c58d9cd218e"],["/tags/乱笔/index.html","2afefbac20dc0deb99898d5a3e70858c"],["/tags/儿子/index.html","43eee6670465dce20c55b374b8710efc"],["/tags/博客/index.html","ce25dfc10e67e4cfab57103e7b862238"],["/tags/历史/index.html","e5f2b78af19124a7fa880ea826604110"],["/tags/反演/index.html","1983ee256e57d3015f6f2d4ea1b9b503"],["/tags/命题作文/index.html","f84e249d85f94d20f1c902b96bdec614"],["/tags/外公/index.html","e7720950e0fd1a322330742919a8a29b"],["/tags/外婆/index.html","3ac0258844d5edb509aa1069607b0ae7"],["/tags/好友/index.html","a5bb46cdd7fdc87762868ce655a05853"],["/tags/妖怪/index.html","869dcd9445d63e7c5d3a86565d80cebd"],["/tags/宁波/index.html","1144c0c0b72d563c0bbd692f0a3ef078"],["/tags/安息/index.html","55e1311fbd4d80826e5a95a3369ba7e5"],["/tags/憎恨/index.html","5a6ca12c22c39be1f17edc8c3786fd76"],["/tags/成都/index.html","05543075cf69d1739921c6d1d8d238d6"],["/tags/打牌/index.html","b384ec7425f5245c3098456f4de0895a"],["/tags/无题/index.html","d7216b808bbe86d55df49ed471b5e11a"],["/tags/日记/index.html","17257e86419502c6bbbab0444c15dba1"],["/tags/日记/page/2/index.html","83a5fe9f5c031b20314630f2d82bf07c"],["/tags/末日记/index.html","62a1a8b8d0a8f23d5c7fdd7e884a3e2e"],["/tags/杂/index.html","73c1dbe9f32066f1b1a41f3c9a564488"],["/tags/某日记/index.html","2a7e92cc551b8801c782efd80253bb12"],["/tags/活着/index.html","8eb5cd4208d0d3e0b1e3de2116403f8b"],["/tags/爱情/index.html","328006593e57ae7442291161f81d81f4"],["/tags/猫/index.html","17691af1a2050bcd0f3fd079b3a68e56"],["/tags/电影/index.html","bb2d3abdd93bb3b0b7a28f72713462b1"],["/tags/盆地/index.html","1356ed3c9dba5c7f1492776ea476b9b2"],["/tags/看透/index.html","7987cb791448cf45e882bd0ccb73dea6"],["/tags/纠葛/index.html","6d7498a4c663e5f31798b67b257e09fe"],["/tags/网易/index.html","7581f465b8cf5f6054c402336a50c8aa"],["/tags/茶铺/index.html","562939fb23baea27cc561ed22d66d5c1"],["/tags/血色浪漫/index.html","ff5eb1e1e1e08ca8506650f30185cac5"],["/tags/诡异/index.html","242528773771157d0da107f8d637bb95"],["/tags/读后感/index.html","da48ad7aa7a61cbb5b4904033c9bd2c9"],["/tags/躯壳/index.html","6428d5b8d5df3a1fbbcc952a1ae33ec0"],["/tags/这是啥/index.html","1ee0ebc88b5a64c240a1716e1c0d76c9"],["/tags/迷雾/index.html","c8c16780642415c9eb36e90c10eba982"],["/tags/逝者/index.html","4a6d8c38f99fb32cf86803540dd284a2"],["/tags/阿甘/index.html","cc079675d4b0ce237cfc695b77a0e5c4"],["/tags/霸王别姬/index.html","3ab6b8df189b2b1acae523272c23c909"],["/tags/饭后感/index.html","d0a8421c6d1356862108036eed4cb64c"]];
var cacheName = 'sw-precache-v3--' + (self.registration ? self.registration.scope : '');
var firstRegister = 1; // 默认1是首次安装SW， 0是SW更新


var ignoreUrlParametersMatching = [/^utm_/];


var addDirectoryIndex = function (originalUrl, index) {
    var url = new URL(originalUrl);
    if (url.pathname.slice(-1) === '/') {
        url.pathname += index;
    }
    return url.toString();
};

var cleanResponse = function (originalResponse) {
    // 如果没有重定向响应，不需干啥
    if (!originalResponse.redirected) {
        return Promise.resolve(originalResponse);
    }

    // Firefox 50 及以下不知处 Response.body 流, 所以我们需要读取整个body以blob形式返回。
    var bodyPromise = 'body' in originalResponse ?
        Promise.resolve(originalResponse.body) :
        originalResponse.blob();

    return bodyPromise.then(function (body) {
        // new Response() 可同时支持 stream or Blob.
        return new Response(body, {
            headers: originalResponse.headers,
            status: originalResponse.status,
            statusText: originalResponse.statusText
        });
    });
};

var createCacheKey = function (originalUrl, paramName, paramValue,
    dontCacheBustUrlsMatching) {

    // 创建一个新的URL对象，避免影响原始URL
    var url = new URL(originalUrl);

    // 如果 dontCacheBustUrlsMatching 值没有设置，或是没有匹配到，将值拼接到url.serach后
    if (!dontCacheBustUrlsMatching ||
        !(url.pathname.match(dontCacheBustUrlsMatching))) {
        url.search += (url.search ? '&' : '') +
            encodeURIComponent(paramName) + '=' + encodeURIComponent(paramValue);
    }

    return url.toString();
};

var isPathWhitelisted = function (whitelist, absoluteUrlString) {
    // 如果 whitelist 是空数组，则认为全部都在白名单内
    if (whitelist.length === 0) {
        return true;
    }

    // 否则逐个匹配正则匹配并返回
    var path = (new URL(absoluteUrlString)).pathname;
    return whitelist.some(function (whitelistedPathRegex) {
        return path.match(whitelistedPathRegex);
    });
};

var stripIgnoredUrlParameters = function (originalUrl,
    ignoreUrlParametersMatching) {
    var url = new URL(originalUrl);
    // 移除 hash; 查看 https://github.com/GoogleChrome/sw-precache/issues/290
    url.hash = '';

    url.search = url.search.slice(1) // 是否包含 '?'
        .split('&') // 分割成数组 'key=value' 的形式
        .map(function (kv) {
            return kv.split('='); // 分割每个 'key=value' 字符串成 [key, value] 形式
        })
        .filter(function (kv) {
            return ignoreUrlParametersMatching.every(function (ignoredRegex) {
                return !ignoredRegex.test(kv[0]); // 如果 key 没有匹配到任何忽略参数正则，就 Return true
            });
        })
        .map(function (kv) {
            return kv.join('='); // 重新把 [key, value] 格式转换为 'key=value' 字符串
        })
        .join('&'); // 将所有参数 'key=value' 以 '&' 拼接

    return url.toString();
};


var addDirectoryIndex = function (originalUrl, index) {
    var url = new URL(originalUrl);
    if (url.pathname.slice(-1) === '/') {
        url.pathname += index;
    }
    return url.toString();
};

var hashParamName = '_sw-precache';
var urlsToCacheKeys = new Map(
    precacheConfig.map(function (item) {
        var relativeUrl = item[0];
        var hash = item[1];
        var absoluteUrl = new URL(relativeUrl, self.location);
        var cacheKey = createCacheKey(absoluteUrl, hashParamName, hash, false);
        return [absoluteUrl.toString(), cacheKey];
    })
);

function setOfCachedUrls(cache) {
    return cache.keys().then(function (requests) {
        // 如果原cacheName中没有缓存任何收，就默认是首次安装，否则认为是SW更新
        if (requests && requests.length > 0) {
            firstRegister = 0; // SW更新
        }
        return requests.map(function (request) {
            return request.url;
        });
    }).then(function (urls) {
        return new Set(urls);
    });
}

self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(cacheName).then(function (cache) {
            return setOfCachedUrls(cache).then(function (cachedUrls) {
                return Promise.all(
                    Array.from(urlsToCacheKeys.values()).map(function (cacheKey) {
                        // 如果缓存中没有匹配到cacheKey，添加进去
                        if (!cachedUrls.has(cacheKey)) {
                            var request = new Request(cacheKey, { credentials: 'same-origin' });
                            return fetch(request).then(function (response) {
                                // 只要返回200才能继续，否则直接抛错
                                if (!response.ok) {
                                    throw new Error('Request for ' + cacheKey + ' returned a ' +
                                        'response with status ' + response.status);
                                }

                                return cleanResponse(response).then(function (responseToCache) {
                                    return cache.put(cacheKey, responseToCache);
                                });
                            });
                        }
                    })
                );
            });
        })
            .then(function () {
            
            // 强制 SW 状态 installing -> activate
            return self.skipWaiting();
            
        })
    );
});

self.addEventListener('activate', function (event) {
    var setOfExpectedUrls = new Set(urlsToCacheKeys.values());

    event.waitUntil(
        caches.open(cacheName).then(function (cache) {
            return cache.keys().then(function (existingRequests) {
                return Promise.all(
                    existingRequests.map(function (existingRequest) {
                        // 删除原缓存中相同键值内容
                        if (!setOfExpectedUrls.has(existingRequest.url)) {
                            return cache.delete(existingRequest);
                        }
                    })
                );
            });
        }).then(function () {
            
            return self.clients.claim();
            
        }).then(function () {
                // 如果是首次安装 SW 时, 不发送更新消息（是否是首次安装，通过指定cacheName 中是否有缓存信息判断）
                // 如果不是首次安装，则是内容有更新，需要通知页面重载更新
                if (!firstRegister) {
                    return self.clients.matchAll()
                        .then(function (clients) {
                            if (clients && clients.length) {
                                clients.forEach(function (client) {
                                    client.postMessage('sw.update');
                                })
                            }
                        })
                }
            })
    );
});



    self.addEventListener('fetch', function (event) {
        if (event.request.method === 'GET') {

            // 是否应该 event.respondWith()，需要我们逐步的判断
            // 而且也方便了后期做特殊的特殊
            var shouldRespond;


            // 首先去除已配置的忽略参数及hash
            // 查看缓存简直中是否包含该请求，包含就将shouldRespond 设为true
            var url = stripIgnoredUrlParameters(event.request.url, ignoreUrlParametersMatching);
            shouldRespond = urlsToCacheKeys.has(url);

            // 如果 shouldRespond 是 false, 我们在url后默认增加 'index.html'
            // (或者是你在配置文件中自行配置的 directoryIndex 参数值)，继续查找缓存列表
            var directoryIndex = 'index.html';
            if (!shouldRespond && directoryIndex) {
                url = addDirectoryIndex(url, directoryIndex);
                shouldRespond = urlsToCacheKeys.has(url);
            }

            // 如果 shouldRespond 仍是 false，检查是否是navigation
            // request， 如果是的话，判断是否能与 navigateFallbackWhitelist 正则列表匹配
            var navigateFallback = '';
            if (!shouldRespond &&
                navigateFallback &&
                (event.request.mode === 'navigate') &&
                isPathWhitelisted([], event.request.url)
            ) {
                url = new URL(navigateFallback, self.location).toString();
                shouldRespond = urlsToCacheKeys.has(url);
            }

            // 如果 shouldRespond 被置为 true
            // 则 event.respondWith()匹配缓存返回结果，匹配不成就直接请求.
            if (shouldRespond) {
                event.respondWith(
                    caches.open(cacheName).then(function (cache) {
                        return cache.match(urlsToCacheKeys.get(url)).then(function (response) {
                            if (response) {
                                return response;
                            }
                            throw Error('The cached response that was expected is missing.');
                        });
                    }).catch(function (e) {
                        // 如果捕获到异常错误，直接返回 fetch() 请求资源
                        console.warn('Couldn\'t serve response for "%s" from cache: %O', event.request.url, e);
                        return fetch(event.request);
                    })
                );
            }
        }
    });









/* eslint-enable */
