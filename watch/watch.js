Worm = new Meteor.Collection("worm");
Recording = new Meteor.Collection("recording");
Request = new Meteor.Collection("request");

if (Meteor.is_client) {

    function select_worm_bb() {
        // XXX: awful!
        // XXX: extend jquery with a worm-box object (?)

        $("#preview").mousedown(function(ev) {
            ev.preventDefault();

            var x = ev.pageX - $(this).offset().left;
            var y = ev.pageY - $(this).offset().top;

            $(this).data("down", [x, y]);

            $("#preview").mouseup(function(ev) {
                var x = ev.pageX - $(this).offset().left;
                var y = ev.pageY - $(this).offset().top;


                var x0 = Math.min($(this).data("down")[0], x);
                var x1 = Math.max($(this).data("down")[0], x);
                var y0 = Math.min($(this).data("down")[1], y);
                var y1 = Math.max($(this).data("down")[1], y);

                // Make a new Request to find a worm.
                Request.insert({bb: [x0, y0, x1-x0, y1-y0],
                                recording: Session.get("selected_recording"),
                                unprocessed: true});

                $("#preview").unbind("mouseup");
            });

            $("#preview").unbind("mousedown");
        });
    }

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

    Template.recordingtab.selected = function () {
        return Session.equals("selected_recording", this._id) ? "selected" : '';
    };


    Template.recording.worms = function () {
        return Worm.find({recording: this._id});
    };

    Template.recording.events = {
        'click #addnew': function() {
            select_worm_bb();
        },
    }
}

// if (Meteor.is_server) {
//     Meteor.startup(function () {
//     });
// }
