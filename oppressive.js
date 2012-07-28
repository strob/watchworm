var OP = {};

// A poor-man's access to relational data.
OP.Objection = function(id, spec) {
    this._id = id;
    for(var k in spec) {
        this[k] = spec[k];
    }
};
OP.Objection.prototype.get = function(k) {
    return OP.Subjectification.obj[this[k]];
};
OP.Objection.prototype.getAll = function(ks) {
    return ks.map(function(k) { return this.get(k); });
};

// Load all object data on startup; anything too large for that can be
// asynchronously loaded.
OP.Subjectification = {
    obj: {},
    all: function(dtype) {
        var out = [];
        for(var key in OP.Subjectification.obj) {
            if(OP.Subjectification.obj[key] instanceof dtype) {
                out.push(OP.Subjectification.obj[key]);
            }
        }
        return out;
    },
    load: function(jsonClassMap, cb) {
        var nrem = 0;
        for(var jsonPath in jsonClassMap) {
            nrem += 1;
            (function(cls) {
                OP.UTIL.loadJson(jsonPath, function(res) {
                    for(var key in res) {
                        OP.Subjectification.obj[key] = new cls(key, res[key]);
                    }
                    nrem -= 1;
                    if(nrem === 0) {
                        cb();
                    }
                });
            })(jsonClassMap[jsonPath])
        }
    }
};

OP.UTIL = {};
OP.UTIL.load = function(uri, cb) {
    var req = new XMLHttpRequest();
    req.open("GET", uri, true);

    req.onreadystatechange = function() { 
        if(req.readyState == 4) {
            if(req.status == 200) {
                cb(req.responseText);
            }
            else {
                console.log("error loading " + uri, req.status);
            }
        }
    };
    req.send();
};
OP.UTIL.loadJson = function (uri, cb) {
    OP.UTIL.load(uri, function(txt) { cb(JSON.parse(txt)); });
};
