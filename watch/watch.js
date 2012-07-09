Worm = new Meteor.Collection("worm");
Recording = new Meteor.Collection("recording");
Request = new Meteor.Collection("request");

if (Meteor.is_client) {
    Template.watchworm.recordings = function() {
        return Recording.find();
    }

    Template.watchworm.selected_recording = function () {
        var rec = Recording.findOne(Session.get("selected_recording"));
        return rec;
    };

    Template.recordingtab.events = {
        'click' : function () {
            Session.set("selected_recording", this._id);
        }
    }

    Template.recording.worms = function () {
        return Worm.find({recording: this._id});
    };

    Template.recording.events = {
        'click input': function() {
            Request.insert({unprocessed: true, recording: this._id})
        }
    }
}

if (Meteor.is_server) {

    Meteor.startup(function () {
        // prepopulate recordings
        if (Recording.find().count() === 0) {
            ["ck410.mov",
             "CK423 d1 q1.avi",
             "CK423 d1 q2.avi",
             "CK565 d1 q1.avi",
             "CK565 d1 q2.avi",
             "n2.avi",
             "worm capture 2.avi",
             "worm capture 3.avi",
             "worm capture 51.avi"].forEach(function(name) {
                 Recording.insert({filename: name});
             });
        }
    });

}
