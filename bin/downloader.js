! function() {

    const loadedScripts = {};
    const REGEX = /^\w+:\/\/.*/;
    const downloader = cc.assetManager.downloader;

    function base64toBlob(base64, type) {
        var bstr = atob(base64, type),
            n = bstr.length,
            u8arr = new Uint8Array(n);
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], {
            type: type,
        })
    }

    function base64toArray(base64) {
        var bstr = atob(base64),
            n = bstr.length,
            u8arr = new Uint8Array(n);
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        return u8arr;
    }


    function arrayBufferHandler(url, options, callback, img) {

        var img = new Image();

        function loadCallback() {
            img.removeEventListener('load', loadCallback);
            img.removeEventListener('error', errorCallback);

            callback(null, img);
        }

        function errorCallback() {
            img.removeEventListener('load', loadCallback);
            img.removeEventListener('error', errorCallback);

            callback(new Error('Load image (' + url + ') failed'));
        }

        img.addEventListener('load', loadCallback);
        img.addEventListener('error', errorCallback);
        img.src = `data:image/${cc.path.extname(url).substring(1)};base64,${window.resMap[url]}`;
    };

    function downloadText(url, options, onComplete) {
        let data = window.resMap[url];
        onComplete(null, data);
    };


    function downloadArrayBuffer(url, options, onComplete) {
        let str = window.resMap[url];
        let data = base64toArray(str);
        onComplete(null, data);
    };

    function downloadBlobHandler(url, options, onComplete) {
        let data = window.resMap[url];
        onComplete(null, base64toBlob(data, `image/${cc.path.extname(url).substring(1)}`));
    }


    function downloadWebAudio(url, options, onComplete) {
        var context = new(window.AudioContext || window.webkitAudioContext)();

        var data = window.resMap[url];
        data = base64toArray(data);

        context["decodeAudioData"](data.buffer, function(buffer) {
            onComplete(null, buffer);
        }, function(e) {
            onComplete(e, null);
        });
    }

    function loadScript(url) {
        let source = window.resMap[url];
        var d = document,
            s = document.createElement('script');
        s.type = 'text/javascript';
        s.text = source;
        d.body.appendChild(s);
    }

    function downloadJson(url, options, onComplete) {
        let data = window.resMap[url];
        data = JSON.parse(data);
        onComplete(null, data);
    };

    function downloadBundleHandler(nameOrUrl, options, onComplete) {
        let bundleName = cc.path.basename(nameOrUrl);
        var version = options.version || cc.assetManager.downloader.bundleVers[bundleName];
        let suffix = version ? version + '.' : '';
        let url = `assets/${bundleName}`;

        let js = `assets/${bundleName}/index.${suffix}js`;
        if (!loadedScripts[js]) {
            loadScript(js);
            loadedScripts[js] = true;
        }

        options.__cacheBundleRoot__ = bundleName;
        var config = `${url}/config.${suffix}json`;
        downloadJson(config, options, function(err, data) {
            if (err) {
                onComplete && onComplete(err);
                return;
            }
            data.base = url + '/';
            onComplete && onComplete(null, data);
        });
    };

    function getFontFamily(fontHandle) {
        var ttfIndex = fontHandle.lastIndexOf(".ttf");
        if (ttfIndex === -1) {
            ttfIndex = fontHandle.lastIndexOf(".tmp");
        }
        if (ttfIndex === -1) return fontHandle;

        var slashPos = fontHandle.lastIndexOf("/");
        var fontFamilyName;
        if (slashPos === -1) {
            fontFamilyName = fontHandle.substring(0, ttfIndex) + "_LABEL";
        } else {
            fontFamilyName = fontHandle.substring(slashPos + 1, ttfIndex) + "_LABEL";
        }
        return fontFamilyName;
    }

    function downloadFont(url, options, onComplete) {
        let fontFamilyName = getFontFamily(url);
        let data = "url(data:application/x-font-woff;charset=utf-8;base64,PASTE-BASE64-HERE) format(\"woff\")";
        data = data.replace("PASTE-BASE64-HERE", window.resMap[url]);

        let fontFace = new FontFace(fontFamilyName, data);
        document.fonts.add(fontFace);

        fontFace.load();
        fontFace.loaded.then(function() {
            onComplete(null, fontFamilyName);
        }, function() {
            cc.warnID(4933, fontFamilyName);
            onComplete(null, fontFamilyName);
        });
    }

    function downloadVideo(url, options, onComplete) {
        onComplete(null);
    }

    cc.assetManager.downloader.register('bundle', downloadBundleHandler);

    cc.assetManager.downloader.register('.png', arrayBufferHandler);
    cc.assetManager.downloader.register('.jpg', arrayBufferHandler);
    cc.assetManager.downloader.register('.jpeg', arrayBufferHandler);
    cc.assetManager.downloader.register('.gif', downloadBlobHandler);

    cc.assetManager.downloader.register('.ttf', downloadFont);
    cc.assetManager.downloader.register('.plist', downloadText);
    cc.assetManager.downloader.register('.json', downloadJson);
    cc.assetManager.downloader.register('.bin', downloadArrayBuffer);

    cc.assetManager.downloader.register('.mp3', downloadWebAudio);
    cc.assetManager.downloader.register('.ogg', downloadWebAudio);
    cc.assetManager.downloader.register('.wav', downloadWebAudio);

    cc.assetManager.downloader.register('.mp4', downloadVideo);
}();