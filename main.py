from flask import Flask, render_template, request, session, redirect, url_for
from profile import Profile
from helpers import id_lookup, load_json
from httprequest import get_all_players
from quests import get_all_objectives
from hideout import get_all_hideout
app = Flask(__name__)
#my_profile = Profile(load_json('profiles/674e8d5e000124d3a4adc638.json'))

#print(get_objectives('59674cd986f7744ab26e32f2', my_profile.profile_id))

#print(quests.get_all_objectives(my_profile.profile_id))

app.secret_key = 'your_secret_key_here'  # Required for sessions

@app.route("/")
def player_selection():
    players = get_all_players()
    return render_template("players.html", players=players)

@app.route("/select_player", methods=["POST"])
def select_player():
    player_id = request.form.get("player_id")
    session['player_id'] = player_id  # Store player_id in session
    return redirect(url_for("profile", pid=player_id))

@app.route("/quests/<pid>")
def profile(pid):
    if 'player_id' not in session or session['player_id'] != pid:
        return redirect(url_for("player_selection"))  # Redirect if player_id is not in session
    quests = get_all_objectives(pid)
    players = get_all_players()  # Fetch players
    return render_template("quests.html", quests=quests, player_id=pid, players=players)

@app.route("/stats/<pid>")
def stats(pid):
    if 'player_id' not in session or session['player_id'] != pid:
        return redirect(url_for("player_selection"))  # Redirect if player_id is not in session
    stats = get_all_stats(pid)
    players = get_all_players()  # Fetch players
    return render_template("stats.html", stats=stats, player_id=pid, players=players)

@app.route("/hideout/<pid>")
def hideout(pid):
    if 'player_id' not in session or session['player_id'] != pid:
        return redirect(url_for("player_selection"))  # Redirect if player_id is not in session
    hideout = get_all_hideout(pid)
    players = get_all_players()  # Fetch players
    return render_template("hideout.html", hideout=hideout, player_id=pid, players=players)

if __name__ == "__main__":
    app.run(debug=True)