from flask import Flask, render_template, jsonify
from profile import Profile
from helpers import id_lookup, load_json
from httprequest import get_all_players
from quests import get_all_objectives

app = Flask(__name__)
#my_profile = Profile(load_json('profiles/674e8d5e000124d3a4adc638.json'))

#print(get_objectives('59674cd986f7744ab26e32f2', my_profile.profile_id))

#print(quests.get_all_objectives(my_profile.profile_id))
@app.route("/")
def player_selection():
    players = get_all_players()
    return render_template("players.html", players=players)

@app.route("/profile/<pid>")
def profile(pid):
    quests = get_all_objectives(pid)
    return render_template("profile.html", quests=quests)

if __name__ == "__main__":
    app.run(debug=True)