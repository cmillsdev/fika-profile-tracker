from flask import Flask, render_template, jsonify
from profile import Profile
from helpers import id_lookup, load_json
from httprequest import get_all_players
from quests import get_all_objectives
from hideout import get_all_hideout
app = Flask(__name__)
#my_profile = Profile(load_json('profiles/674e8d5e000124d3a4adc638.json'))

#print(get_objectives('59674cd986f7744ab26e32f2', my_profile.profile_id))

#print(quests.get_all_objectives(my_profile.profile_id))
@app.route("/")
def player_selection():
    players = get_all_players()
    return render_template("players.html", players=players)

@app.route("/quests/<pid>")
def profile(pid):
    quests = get_all_objectives(pid)
    return render_template("quests.html", quests=quests)

@app.route("/stats/<pid>")
def stats(pid):
    stats = get_all_stats(pid)
    return render_template("stats.html", stats=stats)

@app.route("/hideout/<pid>")
def hideout(pid):
    hideout = get_all_hideout(pid)
    return render_template("hideout.html", hideout=hideout)

if __name__ == "__main__":
    app.run(debug=True)