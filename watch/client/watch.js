Recording = new Meteor.Collection("recording");
Preview = new Meteor.Collection("preview");
Worm = new Meteor.Collection("worm");

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
        var mot =Math.floor(worm.avgSpeed);
        var $hole = $('<div>')
            .offset({left: worm.bb[0],
                     top:  worm.bb[1]})
            .css({position: 'absolute'})
            .html(mot)
            .width(worm.bb[2])
            .height(worm.bb[3])
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

var RW = new RecordingWorms();
RW.contextuallyDraw();
