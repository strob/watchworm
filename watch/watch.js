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

// if (Meteor.is_server) {
//     Meteor.startup(function () {
//     });
// }
