Recording = new Meteor.Collection("recording");
Worm = new Meteor.Collection("worm");
Request = new Meteor.Collection("request");
Preview = new Meteor.Collection("preview");

var RecordingWorms = function() {
    // context-aware recording visualization
    this.$el = $('<div>');
};
RecordingWorms.prototype.contextuallyDraw = function() {
    var that = this;

    var ctx = new Meteor.deps.Context();
    ctx.on_invalidate(function() { that.contextuallyDraw(); });
    ctx.run(function() { that.draw(); })
};
RecordingWorms.prototype.draw = function() {
    var rec_id = Session.get("selected_recording");
    if(!rec_id)
        return;

    var prev = Preview.findOne({recording: rec_id});

    var $wrm = $("<div>")
        .css({position: "absolute"});
    var $img = $("<img>", {id:"preview"});
    if(prev) {
        $img.attr("src", prev.preview);
    }

    Worm.find({recording: rec_id}).forEach(function(worm) {
        var c0 = worm.circleFlow[0];
        var mot =Math.floor(worm.avgSpeed);
        var $hole = $('<div>')
            .offset({left: c0[0] - c0[2],
                     top:  c0[1] - c0[2]})
            .css({position: 'absolute'})
            .html(mot)
            .width(c0[2]*2)
            .height(c0[2]*2)
            .addClass('hole')
            .addClass(worm._id)
            .appendTo($wrm);
    });

    this.$el
        .empty()
        .append($wrm)
        .append($img)
        .appendTo($(document.body));

};

// function select_worm_bb() {
//     // XXX: awful!
//     // XXX: extend jquery with a worm-box object (?)

//     $("#preview").mousedown(function(ev) {
//         ev.preventDefault();

//         var x = ev.pageX - $(this).offset().left;
//         var y = ev.pageY - $(this).offset().top;

//         $(this).data("down", [x, y]);

//         $("#preview").mouseup(function(ev) {
//             var x = ev.pageX - $(this).offset().left;
//             var y = ev.pageY - $(this).offset().top;


//             var x0 = Math.min($(this).data("down")[0], x);
//             var x1 = Math.max($(this).data("down")[0], x);
//             var y0 = Math.min($(this).data("down")[1], y);
//             var y1 = Math.max($(this).data("down")[1], y);

//             // Make a new Request to find a worm.
//             Request.insert({bb: [x0, y0, x1-x0, y1-y0],
//                             recording: Session.get("selected_recording"),
//                             unprocessed: true});

//             $("#preview").unbind("mouseup");
//         });

//         $("#preview").unbind("mousedown");
//     });
// }

Template.watchworm.recordings = function() {
    return Recording.find();
}

Template.watchworm.selected_recording = function () {
    var rec = Recording.findOne({_id: Session.get("selected_recording")});
    return rec;
};

Template.recordingtab.events = {
    'click' : function () {
        Session.set("selected_recording", this._id);
    }
}

Template.recordingtab.selected = function () {
    return Session.equals("selected_recording", this._id) ? "selected" : '';
};


Template.recording.worms = function () {
    return Worm.find({recording: this._id});
};

Template.worm.events = {
    'mouseover': function() {
        $('.'+this._id).addClass('selected');
    },
    'mouseout': function() {
        $('.'+this._id).removeClass('selected');
    }


}

// Template.recording.events = {
//     'click #addnew': function() {
//         select_worm_bb();
//     }
// }

var RW = new RecordingWorms();
RW.contextuallyDraw();
